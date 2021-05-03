import nltk
import string
import os

from dsutils import DataDir
from typing import Optional, Iterator, List, Tuple


class News(DataDir):
    """Implementa a atividade descrita em :ref`Atividade da Aula`.

    :param newsdir: Caminho da pasta de dados (veja a propriedade
        :attr:`newsdir` para mais detalhes)
    :type newsdir: Union[str, None]

    :param newsfile: Caminho relativo a pasta de dados do arquivo contendo a
        notícia a ser analisada (veja a propriedade :attr:`text` para mais
        detalhes)
    :type newsfile: str
    """

    def __init__(self, newsdir: Optional[str] = None,
                 newsfile: str = 'news.txt') -> None:
        super().__init__()

        self._newsfile = self.datafilename(newsfile)
        self._stopwords = list(string.punctuation)
        self._stopwords += nltk.corpus.stopwords.words('english')
        self._stopwords += ['a', 'the']

    @property
    def stopwords(self):
        return self._stopwords

    @property
    def newsfile(self) -> str:
        """Propriedade que define o nome do arquivo de notícia

        :return: Nome do arquivo de notícia
        """
        return self._newsfile

    @property
    def text(self) -> str:
        """Conteúdo do arquivo definido em :attr:`newsfile`

        Na primeira execução, abre o arquivo definido em :attr:`newsfile`
        como somente leitura, armazena e retorna seu conteúdo. Nas execuções
        seguintes, apenas retorna o valor armazenado.

        :return: conteúdo do arquivo definido em :attr:`newsfile`
        """
        with open(self.newsfile, 'r', encoding='utf8') as newsfile:
            text = newsfile.read()

        return text

    @property
    def sents(self) -> Iterator[List[str]]:
        """Gera a lista de sentenças tokenizada

        Gera um iterador sobre cada sentença encontrada em :attr:`text`. Ao
        tokenizar (utilizando as funções :func:`nltk.tokenize.sent_tokenize` e
        :func:`nltk.tokenize.word_tokenize`, a sentença se torna uma lista de
        tokens.

        :return: iterador de lista de sentenças tokenizadas
        """
        for sent in nltk.tokenize.sent_tokenize(self.text):
            sent = sent.replace('\n', ' ')
            sent = nltk.tokenize.word_tokenize(sent)
            yield sent

    @property
    def sents_clean(self) -> Iterator[List[str]]:
        """Gera a lista de sentenças tokenizadas sem *stopwords*.

        Mesma funcionalidade de :attr:`sents`, porém a sentença não contém
        tokens definidos em :attr:`stopwords`.

        :return: iterador de lista de sentenças tokenizadas
        """
        for sent in self.sents:
            for word in sent:
                if word.lower() in self.stopwords:
                    sent.remove(word)
            for word in sent:
                if word.lower() in self.stopwords:
                    sent.remove(word)
            yield sent

    @property
    def sents_len(self) -> int:
        """Quantidade de sentenças

        Retorna o tamanho da lista de sentenças gerado por :attr:`sents`.

        :return: quantidade de sentenças
        """
        return sum([1 for _ in self.sents])

    @property
    def sents_words_len(self) -> int:
        """Quantidade de tokens

        Contabiliza a quantidade de tokens de todas as sentenças.

        :return: quantidade de tokens em todas as sentaças
        """
        return sum([1 for _ in self.sents for _ in _])

    @property
    def sents_pos(self) -> Iterator[List[Tuple[str, str]]]:
        """Gera a lista de sentenças com tokens POS

        Realiza o tagueamento gramatical das sentenças retornadas por
        :attr:`sents` utilizando a função :func:`nltk.tag.pos_tag_sents`.

        :return: iterador de lista de tokens POS
        """
        for sent in nltk.tag.pos_tag_sents(self.sents):
            yield sent

    @property
    def sents_ner(self) -> Iterator[nltk.tree.Tree]:
        """Gera a lista de sentenças com tokens NER

        Realiza o reconhecimento de entidades nomeadas (NER) das sentenças
        retornadas por :attr:`sents` utilizando a função
        :func:`nltk.chunk.ne_chunk_sents`.

        :return: iterador de lista de tokens NER
        """
        for sent in nltk.chunk.ne_chunk_sents(self.sents_pos):
            yield sent

    def top_words(self, n: int = 10) -> Iterator[Tuple[str, int]]:
        """Gera as palavras mais frequentes

        Gera as palavras (neste caso, tokens) mais frequentes em :attr:`text`
        utilizando a classe :class:`nltk.probability.FreqDist`.

        :param n: número de palavras a retornar
        :type n: int
        :return: iterador de tupla (palavra, frequência)
        """
        freq = nltk.probability.FreqDist(_ for _ in self.sents_clean for _ in _)

        for word, top in freq.most_common(n):
            yield word, top

    def top_bigram(self, n: int = 10) -> Iterator[Tuple[str, int]]:
        """Gera os bigramas mais frequentes no texto utilizando

        Gera os bigramas de :attr:`text` utilzando a classe
        :class:`nltk.probability.FreqDist` no resultado da função
        :func:`nltk.util.ngrams`.

        :param n: número de bigramas a retornar
        :type n: int
        :return: iterador de tupla (palavra, frequência)
        """
        bigrams = nltk.ngrams([_ for _ in self.sents_clean for _ in _], 2)
        freq = nltk.probability.FreqDist(bigrams)
        for bigram, top in freq.most_common(n):
            yield bigram, top
