from __future__ import annotations

import docx
import nltk
import string
import dsutils

from typing import Optional, Union

from nltk import ngrams
from nltk import tokenize
from nltk.corpus import webtext
from nltk.corpus import stopwords
from nltk.corpus import machado
from matplotlib import pyplot

BiGram = tuple[str, str]
TriGram = tuple[str, str, str]
QuadriGram = tuple[str, str, str, str]

BiGramFreq = tuple[BiGram, int]
TriGramFreq = tuple[TriGram, int]
QuadriGramFreq = tuple[QuadriGram, int]

NGramFreq = tuple[Union[BiGram, TriGram], int]


class Ex01:
    """Implementa a atividade descrita em :ref:`Apostila 1 Exercitando 01`
    """

    def __init__(self):
        path = dsutils.datadir.join('mix20_rand700_tokens_cleaned', 'tokens')
        self._corpus = nltk.corpus.CategorizedPlaintextCorpusReader(
            path, '.*.txt', cat_pattern=r'(\w+)/*'
        )

    @property
    def corpus(self) -> nltk.corpus.CategorizedPlaintextCorpusReader:
        """
        :return: O Corpus carregado dos arquivos na pasta de dados
        """
        return self._corpus

    def findid(self, fid: str, category: Optional[str] = None) -> list[str]:
        """ Encontra o fileid desejado no :attr:`corpus`

        :param fid: O id desejado
        :type fid: str

        :param category: A categoria desejada
        :type category: str

        :return: Lista de ids encontrado
        """
        if category not in (None, 'neg', 'pos'):
            raise ValueError("'category' deve ser 'neg' ou 'pos'")

        fileids = self.corpus.fileids(category)
        return [fileid for fileid in fileids if fid in fileid]

    def words(self, fileid: str, category: Optional[str] = None) -> iter[str]:
        """Iterador das palavras do corpus com ID ``fileid``

        :param fileid: ID desejado
        :type fileid: str

        :param category: Categoria desejada
        :type category: str

        :return: Iterador de string
        """
        for fid in self.findid(fileid, category):
            for word in self.corpus.words(fid):
                yield word


class Ex02:
    """Implementa a atividade descrita em :ref:`Apostila 1 Exercitando 02`
    """

    def __init__(self, docfile: str) -> None:
        self._doc = docx.Document(dsutils.datadir.join(docfile))

    @property
    def doc(self) -> docx.Document:
        """

        :return: Documento em formato docx
        """
        return self._doc

    @property
    def words(self) -> iter[str]:
        """

        :return: Iterador de string
        """
        for para in self.doc.paragraphs:
            for word in para.text.split():
                yield word

    @property
    def bigrams(self) -> iter[BiGram]:
        """

        :return: Iterador de tupla
        """
        return ngrams(list(self.words), 2)

    @property
    def trigrams(self) -> iter[TriGram]:
        """

        :return: Iterador de tupla
        """
        return ngrams(list(self.words), 3)

    def top_bigrams(self, top: Optional[int] = 20) -> iter[BiGramFreq]:
        """

        :param top:
        :type top: int

        :return: Iterador de tupla
        """
        for obj, freq in nltk.FreqDist(self.bigrams).most_common(top):
            yield obj, freq

    def top_trigrams(self, top: Optional[int] = 20) -> iter[TriGramFreq]:
        """

        :param top:
        :type top: int

        :return: Iterador de tupla
        """
        for obj, freq in nltk.FreqDist(self.trigrams).most_common(top):
            yield obj, freq


class Ex03:
    """Implementa a atividade descrita em :ref:`Apostila 1 Exercitando 03`
    """

    def __init__(self, file: str) -> None:
        self.file = file
        self._words = None

        self._stopwords = stopwords.words('english') + [
            "[", "]", ".", ",", "?", "*", ":", "...", "!", "'", "'s",
            "#", "(", ")", "'m", "-", "'ve", "ft.", "n't", "y.o", "&", "..",
            "n/s", "s/d", "n/d", "s/s", "s/e", "''"] + list(string.punctuation)

    @property
    def stopwords(self) -> list[str]:
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
    def words(self) -> list[str]:
        if not self._words:
            self._words = webtext.words(self.file)

        return self._words

    @property
    def tokens(self) -> iter[str]:
        for token in self.words:
            t = token.lower()
            if t not in self.stopwords and len(t) > 1:
                yield token.lower()

    @property
    def tokens_freq(self) -> nltk.FreqDist:
        return nltk.FreqDist(self.tokens)

    @property
    def words_freq(self) -> nltk.FreqDist:
        return nltk.FreqDist(self.words)

    def tokens_freq_plot(self) -> str:
        out = dsutils.datadir.join(self.file.split('.')[0] + '.png')

        fig = pyplot.figure(figsize=(10, 4))
        pyplot.ion()
        self.tokens_freq.plot(50, cumulative=False)
        fig.savefig(out, bbox_inches="tight")
        pyplot.ioff()

        return out

    @property
    def bigrams(self) -> iter[BiGram]:
        return ngrams(list(self.tokens), 2)

    def quadrigrams(self, word: Optional[str] = None) -> iter[QuadriGram]:
        if word is None:
            for gram in ngrams(list(self.tokens), 4):
                yield gram
        else:
            for gram in ngrams(list(self.tokens), 4):
                if word in gram:
                    yield gram

    @property
    def top_bigrams(self) -> list[BiGramFreq]:
        return nltk.FreqDist(self.bigrams).most_common(15)

    @property
    def top_life_quadrigrams(self) -> list[QuadriGramFreq]:
        return nltk.FreqDist(self.quadrigrams('life')).most_common(20)


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
