import docx
import nltk
import string
import os

from typing import Optional, List, Tuple, Iterator, Any
from dsutils import DataDir
from nltk import ngrams
from nltk import tokenize
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk.corpus import webtext
from nltk.corpus import stopwords
from nltk.corpus import machado


class Ex01(DataDir):

    def __init__(self):
        super().__init__()
        path = os.path.join(self.datadir,
                            'mix20_rand700_tokens_cleaned',
                            'tokens')
        self._corpus = CategorizedPlaintextCorpusReader(
            path, '.*.txt', cat_pattern=r'(\w+)/*'
        )

    @property
    def corpus(self) -> CategorizedPlaintextCorpusReader:
        return self._corpus

    def findid(self, fid: str,
               category: Optional[str] = None) -> List[str]:
        if category not in (None, 'neg', 'pos'):
            raise ValueError("'category' deve ser 'neg' ou 'pos'")

        fileids = self.corpus.fileids(category)
        return [fileid for fileid in fileids if fid in fileid]

    def words(self, fileid: str,
              category: Optional[str] = None) -> Iterator[str]:
        for fid in self.findid(fileid, category):
            for word in self.corpus.words(fid):
                yield word


class Ex02(DataDir):

    def __init__(self, docfile: str) -> None:
        super().__init__()
        docfile = self.datafilename(docfile)
        self._doc = docx.Document(docfile)

    @property
    def doc(self) -> docx.Document:
        return self._doc

    @property
    def words(self) -> Iterator[str]:
        for para in self.doc.paragraphs:
            for word in para.text.split():
                yield word

    @property
    def bigrams(self) -> Iterator[Tuple[str, str]]:
        return ngrams(list(self.words), 2)

    @property
    def trigrams(self) -> Iterator[Tuple[str, str, str]]:
        return ngrams(list(self.words), 3)

    def top_bigrams(self,
                    top: Optional[int] = 20) -> Iterator[Tuple[Any, int]]:
        for obj, freq in nltk.FreqDist(self.bigrams).most_common(top):
            yield obj, freq

    def top_trigrams(self,
                     top: Optional[int] = 20) -> Iterator[Tuple[Any, int]]:
        for obj, freq in nltk.FreqDist(self.trigrams).most_common(top):
            yield obj, freq


class Ex03(DataDir):

    def __init__(self, file: str) -> None:
        super().__init__()
        self.file = file
        self._words = None

        self._stopwords = stopwords.words('english') + [
            "[", "]", ".", ",", "?", "*", ":", "...", "!", "'", "'s",
            "#", "(", ")", "'m", "-", "'ve", "ft.", "n't", "y.o", "&", "..",
            "n/s", "s/d", "n/d", "s/s", "s/e", "''"] + list(string.punctuation)

    @property
    def stopwords(self) -> List[str]:
        return self._stopwords

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, file: str) -> None:
        if file not in ('singles.txt', 'pirates.txt'):
            raise ValueError("'file' deve ser singles ou pirates")
        self._file = file

    @property
    def words(self) -> List[str]:
        if not self._words:
            self._words = webtext.words(self.file)

        return self._words

    def word_freq(self, word: str) -> int:
        try:
            freq = nltk.FreqDist(self.words)[word]
        except KeyError:
            freq = 0

        return freq

    @property
    def tokens(self) -> Iterator[str]:
        for token in self.words:
            t = token.lower()
            if t not in self.stopwords and len(t) > 1:
                yield token.lower()

    def token_freq(self, token: str) -> int:
        try:
            freq = nltk.FreqDist(self.tokens)[token]
        except KeyError:
            freq = 0

        return freq

    @property
    def bigrams(self) -> Iterator[Tuple[str, str]]:
        return ngrams(list(self.tokens), 2)

    def quadrigrams(
            self,
            word: Optional[str] = None
    ) -> Iterator[Tuple[str, str, str, str]]:

        if not word:
            for gram in ngrams(list(self.tokens), 4):
                yield gram

        for gram in ngrams(list(self.tokens), 4):
            if word in gram:
                yield gram

    @property
    def top_bigrams(self):
        return nltk.FreqDist(self.bigrams).most_common(15)

    @property
    def top_quadrigrams(self):
        return nltk.FreqDist(self.quadrigrams()).most_common(20)



def ex03():
    data = {
        'singles.txt': {
            'tokens': [],
            'freq_tokens': None,
            'freq_tokens_top15': [],
            'freq_bigrams': None,
            'freq_bigrams_top15': [],
            'freq_quadrigrams_life': []
        },
        'pirates.txt': {
            'tokens': [],
            'freq_tokens': None,
            'freq_tokens_top15': [],
            'freq_bigrams': None,
            'freq_bigrams_top15': [],
            'freq_quadrigrams_life': []
        }
    }

    # Gera os stopwords e inclui palavras personalizadas
    sw = stopwords.words('english') + [
        "[", "]", ".", ",", "?", "*", ":", "...", "!", "'", "'s",
        "#", "(", ")", "'m", "-", "'ve", "ft.", "n't", "y.o", "&", "..",
        "n/s", "s/d", "n/d", "s/s", "s/e", "''"
    ]

    for file in data:
        text = webtext.raw(file)

        # Gera e filtra os tokens de cada arquivo
        data[file]['tokens'] = tokenize.word_tokenize(text)
        data[file]['tokens'] = [t.lower() for t in data[file]['tokens']
                                if t.lower() not in sw]

        # Gera os dados de frequência dos tokens
        data[file]['freq_tokens'] = nltk.FreqDist(data[file]['tokens'])

        # Gera os dados dos 15 tokens mais frequentes
        top15 = data[file]['freq_tokens'].most_common(15)
        data[file]['freq_tokens_top15'] = top15

        # Gera os dados de frequência dos bigramas
        bigram = ngrams(data[file]['tokens'], 2)
        data[file]['freq_bigrams'] = nltk.FreqDist(bigram)

        # Gera os dados dos 15 bigramas mais frequentes
        top15 = data[file]['freq_bigrams'].most_common(15)
        data[file]['freq_bigrams_top15'] = top15

        # Gera os dados de frequência dos quadrigramas com palavra "life"
        quadrigram = [ng for ng in ngrams(data[file]['tokens'], 4)
                      if 'life' in ng]
        data[file]['freq_quadrigrams_life'] = nltk.FreqDist(quadrigram)

        # Imprime frequência das palavras 'the' e 'that'
        print('\n{:20s} {:35s} {}'.format('Arquivo', 'Token', 'Frequência'))
        for word in ['the', 'that']:
            freq = data[file]['freq_tokens'][word]
            print('{:20s} {:35s} {:03}'.format(file, word, freq))

        # Imprime Top 15 Tokens
        print('\n{:20s} {:35s} {}'.format('Arquivo', 'Top 15 Tokens',
                                          'Frequência'))
        for token, freq in data[file]['freq_tokens_top15']:
            print('{:20s} {:35s} {:03}'.format(file, token, freq))

        # Imprime Top 15 Bigramas
        print('\n{:20s} {:35s} {}'.format(
            'Arquivo', 'Top 15 Bigrama', 'Frequência'))
        for bigram, freq in data[file]['freq_bigrams_top15']:
            print('{:20s} {:35s} {:03}'.format(file, str(bigram), freq))

        # Imprime Top 20 Quadrigramas com palavra "life"
        print('\n{:20s} {:50s} {}'.format(
            'Arquivo', 'Top 20 Quadrigrama', 'Frequência'))
        top20 = data[file]['freq_quadrigrams_life'].most_common(20)
        for quadrigram, freq in top20:
            print('{:20s} {:50s} {:03}'.format(file, str(quadrigram), freq))

    data['singles.txt']['freq_tokens'].plot(cumulative=False)
    data['pirates.txt']['freq_tokens'].plot(cumulative=True)


def ex04():
    # Execute print(machado.readme()) para conhecer melhor o corpus
    print(machado.readme())

    # Utilizando o corpus machado, elabore um programa que atenda aos
    # requisitos:

    # a. Quais são as categorias presentes no corpus?
    print('Categorias: {}'.format(machado.categories()))

    # b. Quais são os documentos dentro desse corpus?
    print('Documentos: {}'.format(machado.fileids()))

    # c. Imprima o conteúdo do arquivo do documento que contem a obra
    #    Memórias Postumas de Braz Cubas
    book_fileid = 'romance/marm05.txt'
    print(machado.raw(book_fileid))

    # d. Analise a frequência das palavras [‘olhos’,’estado’] em
    #    Memórias Postumas de Bras Cubas
    book_text = machado.raw(book_fileid)
    book_tokens = tokenize.word_tokenize(book_text)
    book_freq = nltk.FreqDist(book_tokens)

    for w in ['olhos', 'estado']:
        print('Frequência da palavra {:>8s} : {:03}'.format(w, book_freq[w]))

    # e. Quantas palavras há no texto? Use len(texto)
    print('Total de palavras: {}'.format(len(book_text)))

    # f. Quantas palavras distintas há na obra?
    print('Total de palavras distintas: {}'.format(len(book_freq)))

    # g. Qual é o vocabulário (palavras) presentes na obra?
    print('Vocabulário: {}'.format(book_freq.keys()))

    # h. Quais são os 15 termos mais repetidos no texto de Machado de Assis?
    print('\n{:25s} {}'.format('Top 15', 'Frequência'))
    for w, f in book_freq.most_common(15):
        print('{:25s} {:03}'.format(w, f))

    # i. Tabular a frequência de palavras
    print('\n')
    book_freq.tabulate(15, cumulative=False)

    # j. Gerar um gráfico com os 15 termos mais repetidos
    book_freq.plot(15, title='Top 15 words', cumulative=False)

    # k. Remova os termos indesejados  e repita as questões 'h' a 'j'
    book_stopwords = stopwords.words('portuguese')
    book_stopwords += ['\x97', '...', 'd.']
    book_stopwords += [p for p in string.punctuation]
    book_tokens = [t.lower() for t in book_tokens
                   if t.lower() not in book_stopwords]
    book_freq = nltk.FreqDist(book_tokens)

    print('\n{:25s} {}'.format('Top 15', 'Frequência'))
    for w, f in book_freq.most_common(15):
        print('{:25s} {:03}'.format(w, f))

    print('\n')
    book_freq.tabulate(15, cumulative=False)

    book_freq.plot(15, title='Top 15 words', cumulative=False)

    # l. Obter a lista de todos os trigramas do texto
    for trigram in ngrams(book_tokens, 3):
        print('{:35s}'.format(str(trigram)))

    # m. Obter a lista dos 15 bigramas que contenham a palavra 'olhos'
    olhos_bigram = [ng for ng in ngrams(book_tokens, 2) if 'olhos' in ng]
    olhos_freq = nltk.FreqDist(olhos_bigram)
    print('\n{:30s} {}'.format('Top 15 Olhos', 'Frequência'))
    for b, f in olhos_freq.most_common(15):
        print('{:30s} {:03}'.format(str(b), f))

    # n. Gerar o gráfico dos bigramas com a palavra 'olhos'
    olhos_freq.plot(15, cumulative=True)
