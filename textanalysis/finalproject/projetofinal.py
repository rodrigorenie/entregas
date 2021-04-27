# Rodrigo Renie de Braga Pinto
# Tarefa: Analisar textos.
# Os textos baixados podem estar relacionados com um interesse da equipe, mas
# devem ser baixadas, no mínimo, 50.000 (cinquenta mil sentenças). Para a
# análise, deve-se produzir:

import os
import re
import string
import logging
import time

import nltk
import spacy
import wordcloud
import collections
import matplotlib.pyplot
import functools

from spacy.symbols import PRON, VERB
from pysubparser import parser
from pysubparser.cleaners import brackets, formatting


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    # filename='dados/debug.log',
    # filemode='w'
)


def logged(func=None, *, level=logging.DEBUG, message=None):
    if func is None:
        return functools.partial(logged, level=level, message=message)

    name = func.__qualname__
    message = message if message else '{name}: Em execução'

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.log(level, message.format(name=name))
        return func(*args, **kwargs)

    return wrapper


def timed(func=None, *, level=logging.DEBUG, message=None):
    if func is None:
        return functools.partial(timed, level=level, message=message)

    name = func.__qualname__
    message = message if message else '{name}: Execução levou {run_time:.2f}s'

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        run_time = time.perf_counter()
        value = func(*args, **kwargs)
        run_time = time.perf_counter() - run_time
        logging.log(level, message.format(name=name, run_time=run_time))
        return value

    return wrapper


def parse_filename(filename):
    rex = re.search(r"[sS]([0-9]{2})[eE]([0-9]{2})", filename)
    try:
        season, episode = rex.group(1, 2)
    except Exception as e:
        logging.error('Erro ao detectar a temporada/episódio do arquivo "{}" ({})'.format(filename, e))
        season = episode = None
    finally:
        return season, episode


def nltk_tree_find(tree, label='PERSON'):
    if tree.label() == label:
        yield tree

    for subtree in tree:
        if type(subtree) == nltk.Tree:
            for match in nltk_tree_find(subtree, label):
                yield match


class Subtitles:

    def __init__(self, rootdir, encoding='latin-1'):
        self._subtitles = {}

        for dirpath, dirnames, filelist in os.walk(rootdir):
            filelist.sort()
            dirnames.sort()

            for filename in filelist:
                filename = os.path.join(dirpath, filename)
                season, episode = parse_filename(filename)

                data = parser.parse(filename, encoding=encoding)
                data = brackets.clean(data)
                data = formatting.clean(data)
                data = [line.text for line in data]
                self._subtitles[filename] = (season, episode, data)

    @property
    def subtitles(self):
        return [data for _, _, data in self._subtitles.values()]

    @property
    def subtitles_text(self):
        return ['\n'.join(data) for _, _, data in self._subtitles.values()]

    def __iter__(self):
        for _, _, data in self._subtitles.values():
            yield data

    def __str__(self):
        return '\n\n'.join(['\n'.join(subtitle) for subtitle in self]).replace('\x82', '')

    def __len__(self):
        return len(self._subtitles)


class ProjetoFinal:

    def __init__(self, text):
        self.text = text

        self._sentences = None
        self._sentences_len = None

        self._tokens = None
        self._tokens_len = None
        self._tokens_frequency = None
        self._tokens_pron_verb_frequency = None

        self._trigrams_frequency = None
        self._vocabulary = None

        self._pos = None
        self._ner = None
        self._ner_len = None
        self._ner_person_len = None
        self._ner_person_frequency = None
        self._ner_location_len = None
        self._ner_location_frequency = None

        self._wordcloud = None
        self._summary = None
        self._summary_tokens = None

    @staticmethod
    def plot(counter, limit=None, xlimit=None, title=None, filename=None):
        matplotlib.pyplot.rcParams['figure.figsize'] = (16.0, 10.0)
        matplotlib.pyplot.style.use('ggplot')

        barx, bary = [], []
        for x, y in counter.most_common(limit):
            barx.append(str(x))
            bary.append(y)
        _, ax = matplotlib.pyplot.subplots()
        ax.barh(barx, bary, align='center')

        for xi, xv in enumerate(bary):
            ax.text(xv + 1, xi - 0.20, str(xv), color='black')

        if xlimit:
            ax.set_xlim(0, xlimit)

        if title:
            ax.title.set_text(title)

        if filename:
            matplotlib.pyplot.savefig(filename, dpi=300, format='png', bbox_inches='tight')
        else:
            matplotlib.pyplot.show()


class ProjetoFinalNLTK(ProjetoFinal):

    def __init__(self, text):
        super().__init__(text)
        self._stopwords = [punct for punct in string.punctuation]
        self._stopwords += ["''", '``', '--', '...', '... ...', "'", '-', '\n']
        self._stopwords += ["n't", "'re", "'m", "oh", "hey", "'ll", "'ve", "'s"]
        self._stopwords += nltk.corpus.stopwords.words('english')

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str):
            self._text = text

        elif isinstance(text, list):
            self._text = '\n\n'.join(text)

        else:
            raise TypeError("'text' must be string or a list of strings")

    def token_isstop(self, token):
        return token.lower() in self._stopwords

    @property
    def sentences(self):
        if self._sentences is None:
            self._sentences = []
            sentences = [sent.replace('\n', ' ') for sent in nltk.sent_tokenize(self._text)]

            for sent in sentences:
                tokens = nltk.word_tokenize(sent)
                if len(tokens) > 0:
                    self._sentences.append(tokens)

        return self._sentences

    @property
    def sentences_len(self):
        if self._sentences_len is None:
            self._sentences_len = len(self.sentences)

        return self._sentences_len

    @property
    def tokens(self):
        if self._tokens is None:
            self._tokens = [token for sent in self.sentences for token in sent]

        return self._tokens

    @property
    def tokens_len(self):
        if self._tokens_len is None:
            self._tokens_len = len(self.tokens)

        return self._tokens_len

    @property
    def tokens_frequency(self):
        if self._tokens_frequency is None:
            self._tokens_frequency = nltk.FreqDist([t for t in self.tokens if not self.token_isstop(t)])

        return self._tokens_frequency

    @property
    def trigrams(self):
        for index, token in enumerate(self.tokens):
            if not self.token_isstop(token) and index >= 2:
                t0 = self.tokens[index - 2]
                t1 = self.tokens[index - 1]
                if not self.token_isstop(t0) and not self.token_isstop(t1):
                    yield t0, t1, token

    @property
    def trigrams_frequency(self):
        if self._trigrams_frequency is None:
            self._trigrams_frequency = nltk.FreqDist([t for t in self.trigrams])

        return self._trigrams_frequency

    @property
    def vocabulary(self):
        if self._vocabulary is None:
            self._vocabulary = sorted(set([t.lower() for t in self.tokens if not self.token_isstop(t)]))

        return self._vocabulary

    @property
    def pos(self):
        if self._pos is None:
            self._pos = [nltk.pos_tag(sent) for sent in self.sentences]

        return self._pos

    @property
    def ner(self):
        if self._ner is None:
            self._ner = [nltk.ne_chunk(sent) for sent in self.pos]

        return self._ner

    @property
    def ner_len(self):
        if self._ner_len is None:
            self._ner_len = len(self.ner)

        return self._ner_len

    @property
    def ner_person(self):
        for ner in self.ner:
            for person in nltk_tree_find(ner, 'PERSON'):
                yield person

    @property
    def ner_person_len(self):
        if self._ner_person_len is None:
            self._ner_person_len = sum([1 for _ in self.ner_person])

        return self._ner_person_len

    @property
    def ner_person_frequency(self):
        if self._ner_person_frequency is None:
            textlist = [' '.join([text for text, _ in token.leaves()]) for token in self.ner_person]
            self._ner_person_frequency = nltk.FreqDist(textlist)

        return self._ner_person_frequency

    @property
    def ner_location(self):
        for ner in self.ner:
            for gpe in nltk_tree_find(ner, 'GPE'):
                yield gpe
            for location in nltk_tree_find(ner, 'LOCATION'):
                yield location

    @property
    def ner_location_len(self):
        if self._ner_location_len is None:
            self._ner_location_len = sum([1 for _ in self.ner_location])

        return self._ner_location_len

    @property
    def ner_location_frequency(self):
        if self._ner_location_frequency is None:
            textlist = [' '.join([text for text, _ in token.leaves()]) for token in self.ner_location]
            self._ner_location_frequency = nltk.FreqDist(textlist)

        return self._ner_location_frequency

    @property
    def wordcloud(self):
        if self._wordcloud is None:
            frequency = {}
            for token in self.tokens:
                if not self.token_isstop(token):
                    if token.lower() in frequency:
                        frequency[token.lower()] += 1
                    else:
                        frequency[token.lower()] = 1
            self._wordcloud = wordcloud.WordCloud(width=800, height=400,
                                                  relative_scaling=1.0).generate_from_frequencies(frequency)

        return self._wordcloud

    @property
    def tokens_pron_verb(self):
        check_next = False
        previous_token = None

        for pos_sent in self.pos:
            for token, tag in pos_sent:
                if check_next:
                    if tag in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):
                        yield previous_token, token

                    check_next = False
                    previous_token = None

                if tag in ('PRP', 'PRP$'):
                    previous_token = token
                    check_next = True

    @property
    def tokens_pron_verb_frequency(self):
        if self._tokens_pron_verb_frequency is None:
            textlist = [t for t in self.tokens_pron_verb]
            self._tokens_pron_verb_frequency = nltk.FreqDist(textlist)

        return self._tokens_pron_verb_frequency

    @property
    def summary(self):
        raise NotImplementedError


class ProjetoFinalSpacy(ProjetoFinal):

    def __init__(self, text, selectfor="efficiency"):
        super().__init__(text)
        self._doc = None
        self._nlp = None
        self._summary_doc = None

        if selectfor == 'efficiency':
            self._model = 'en_core_web_sm'
        elif selectfor == 'accuracy':
            self._model = 'en_core_web_trf'
        else:
            raise ValueError("'selectfor' should be 'accuracy' or 'efficiency'")

        self._bigram_pron_verb_frequency = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if isinstance(text, str) or isinstance(text, list):
            self._text = text
        else:
            raise TypeError("'text' must be string or a list of strings")

    @property
    def nlp(self):
        if self._nlp is None:
            self._nlp = spacy.load(self._model)

        return self._nlp

    @property
    @logged
    @timed
    def doc(self):
        if self._doc is None:
            if isinstance(self.text, str):
                self._doc = [self.nlp(self.text)]

            if isinstance(self.text, list):
                self._doc = list(self.nlp.pipe(self.text))

        return self._doc

    @property
    def sentences(self):
        for doc in self.doc:
            for sent in doc.sents:
                yield sent

    @property
    def sentences_len(self):
        if self._sentences_len is None:
            self._sentences_len = sum([1 for doc in self.doc for _ in doc.sents])

        return self._sentences_len

    @staticmethod
    def token_isstop(token):
        # return token.is_punct or token.is_space
        return token.is_stop or token.is_punct or token.is_space

    @property
    def tokens(self):
        for doc in self.doc:
            for token in doc:
                yield token

    @property
    @logged
    @timed
    def tokens_len(self):
        if self._tokens_len is None:
            self._tokens_len = sum([1 for _ in self.tokens])

        return self._tokens_len

    @property
    def tokens_frequency(self):
        if self._tokens_frequency is None:
            self._tokens_frequency = collections.Counter(
                [token.text for token in self.tokens if not self.token_isstop(token)])

        return self._tokens_frequency

    @property
    def trigrams(self):
        for token in self.tokens:
            if token.i >= 2 and not self.token_isstop(token):
                t0 = token.doc[token.i-2]
                t1 = token.doc[token.i-1]
                if not self.token_isstop(t0) and not self.token_isstop(t1):
                    yield t0, t1, token

    @property
    def trigrams_frequency(self):
        if self._trigrams_frequency is None:
            self._trigrams_frequency = collections.Counter(
                [(t1.text, t2.text, t3.text) for t1, t2, t3 in self.trigrams])

        return self._trigrams_frequency

    @property
    def vocabulary(self):
        if self._vocabulary is None:
            self._vocabulary = sorted(set(
                [token.text.lower() for token in self.tokens if not self.token_isstop(token)]))

        return self._vocabulary

    @property
    def pos(self):
        raise NotImplementedError

    @property
    def ner(self):
        for doc in self.doc:
            for ner in doc.ents:
                yield ner

    @property
    def ner_len(self):
        if self._ner_len is None:
            self._ner_len = sum([1 for _ in self.ner])

        return self._ner_len

    @property
    def ner_person(self):
        for ner in self.ner:
            if ner.label_ == 'PERSON':
                yield ner

    @property
    def ner_person_len(self):
        if self._ner_person_len is None:
            self._ner_person_len = sum([1 for _ in self.ner_person])

        return self._ner_person_len

    @property
    def ner_person_frequency(self):
        if self._ner_person_frequency is None:
            self._ner_person_frequency = collections.Counter([token.text for token in self.ner_person])

        return self._ner_person_frequency

    @property
    def ner_location(self):
        for ner in self.ner:
            if ner.label_ in ('GPE', 'LOC'):
                yield ner

    @property
    def ner_location_len(self):
        if self._ner_location_len is None:
            self._ner_location_len = sum([1 for _ in self.ner_location])

        return self._ner_location_len

    @property
    def ner_location_frequency(self):
        if self._ner_location_frequency is None:
            self._ner_location_frequency = collections.Counter([token.text for token in self.ner_location])

        return self._ner_location_frequency

    @property
    def wordcloud(self):
        if self._wordcloud is None:
            frequency = {}
            for token in self.tokens:
                if not self.token_isstop(token):
                    if token.text.lower() in frequency:
                        frequency[token.text.lower()] += 1
                    else:
                        frequency[token.text.lower()] = 1
            self._wordcloud = wordcloud.WordCloud(width=800,
                                                  height=400,
                                                  relative_scaling=1.0).generate_from_frequencies(frequency)

        return self._wordcloud

    @property
    def tokens_pron_verb(self):
        for token in self.tokens:
            if token.i >= 1:
                left = token.doc[token.i - 1]
                if left.pos == PRON and token.pos == VERB:
                    yield left, token

    @property
    def tokens_pron_verb_frequency(self):
        if self._bigram_pron_verb_frequency is None:
            self._bigram_pron_verb_frequency = collections.Counter(
                [(t1.text, t2.text) for t1, t2 in self.tokens_pron_verb])

        return self._bigram_pron_verb_frequency

    @property
    def summary(self):
        raise NotImplementedError

    @property
    def summary_doc(self):
        raise NotImplementedError

    @property
    def summary_tokens(self):
        raise NotImplementedError

    @property
    def summary_keywords(self):
        raise NotImplementedError
