import nltk
import string
import os


from typing import Optional, Iterator


class News:
    """implementa a atividade descrita em :ref:`textanalysis.classactivity`.

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
        self.newsdir = newsdir
        self.newsfile = newsfile

        self._sent = nltk.tokenize.punkt.PunktSentenceTokenizer()
        self._word = nltk.tokenize.treebank.TreebankWordTokenizer()

        self._stopwords = list(string.punctuation)
        self._stopwords += nltk.corpus.stopwords.words('english')
        self._stopwords += ['a', 'the']

        self._text = None

    @property
    def stopwords(self):
        return self._stopwords

    @property
    def newsdir(self) -> str:
        """Propriedade que define o caminho da pasta de dados

        A pasta de dados é o diretório onde todos os arquivos carregados ou
        gerados por esta classe ficam armazenados. Se for definido com
        ``None``, é definido o valor padrão
        ``../../data/textanalysis.classactivity``. Neste caso o atributo
        :attr:`text` também é definido para ``None`` para recarregar o texto
        deste arquivo.

        :return: valor atual da propriedade :attr:`newsdir`
        :rtype: str

        :raises FileNotFoundError: se for definido com um caminho que não
                existe
        :raises TypeError: se for definido com um caminho que não é
                uma pasta
        """
        return self._datadir

    @newsdir.setter
    def newsdir(self, datadir: str) -> None:
        if not datadir:
            datadir = os.path.join(os.path.dirname(__file__), '..', '..',
                                   'data', 'textanalysis.classactivity')
            datadir = os.path.abspath(datadir)

        if not os.path.exists(datadir):
            raise FileNotFoundError(
                f"O caminho informado '{datadir}' não existe"
            )

        if not os.path.isdir(datadir):
            raise TypeError(
                f"O caminho informado '{datadir}' não é uma pasta"
            )

        self._datadir = datadir
        self._text = None

    @property
    def newsfile(self) -> str:
        """Propriedade que define o caminho do arquivo de notícia

        O caminho deve ser relativo à pasta de dados definido no atributo
        :attr:`newsdir`. Se for definido com ``None``, é definido o valor
        padrão ``news.txt``. Neste caso o atributo :attr:`text` também é
        definido para ``None`` para recarregar o texto deste arquivo.

        :return: valor atual da propriedade :attr:`newsfile`
        :rtype: str

        :raises FileNotFoundError: se for definido com um caminho que não
                existe
        :raises TypeError: se for definido com um caminho que não é
                uma pasta
        """
        return self._newsfile

    @newsfile.setter
    def newsfile(self, newsfile: str) -> None:
        if not newsfile:
            newsfile = 'text.txt'

        newsfile = os.path.join(self.newsdir, newsfile)

        if not os.path.exists(newsfile):
            raise FileNotFoundError(
                f"O caminho informado '{newsfile}' não existe"
            )

        if not os.path.isfile(newsfile):
            raise TypeError(
                f"O caminho informado '{newsfile}' não é um arquivo"
            )

        self._newsfile = newsfile
        self._text = None

    @property
    def text(self) -> str:
        """Conteúdo do arquivo definido em :attr:`newsfile`

        Na primeira execução, abre o arquivo definido em :attr:`newsfile`
        como somente leitura, armazena e retorna seu conteúdo. Nas execuções
        seguintes, apenas retorna o valor armazenado.

        :return: conteúdo do arquivo definido em :attr:`newsfile`
        :rtype: str
        """
        if not self._text:
            with open(self.newsfile, 'r', encoding='utf8') as newsfile:
                self._text = newsfile.read()

        return self._text

    @property
    def sents(self) -> Iterator[list]:
        """Gera a lista de sentenças tokenizada

        Gera um iterador sobre cada sentença encontrada em :attr:`text`.,
        com cada sentança devidamente tokenizada, sendo portanto uma lista de
        tokens.

        :return: iterador de lista de sentenças tokenizadas
        :rtype: Iterator[list]
        """
        for sent in self._sent.tokenize(self.text):
            sent = sent.replace('\n', ' ')
            sent = self._word.tokenize(sent)
            yield sent

    @property
    def sents_clean(self) -> Iterator[list]:
        """Gera a lista de sentenças tokenizadas sem *stopwords*.

        Mesma funcionalidade de :attr:`sents`, porém a sentença não contém
        tokens definidos em :attr:`stopwords`.

        :return: iterador de lista de sentenças tokenizadas
        :rtype: Iterator[list]
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
        :rtype: int
        """
        return sum([1 for _ in self.sents])

    @property
    def sents_words_len(self) -> int:
        """Quantidade de tokens

        Contabiliza a quantidade de tokens de todas as sentenças.

        :return: quantidade de tokens em todas as sentaças
        :rtype: int
        """
        return sum([1 for _ in self.sents for _ in _])

    @property
    def sents_pos(self) -> Iterator[list]:
        """Gera a lista de sentenças com tokens POS

        Realiza o tagueamento gramatical das sentenças retornadas por
        :attr:`sents` utilizando a função :meth:`nltk.pos_tag_sents`.

        :return: iterador de lista de tokens POS
        :rtype: Iterator[list]
        """
        for sent in nltk.pos_tag_sents(self.sents):
            yield sent

    @property
    def sents_ner(self) -> Iterator[nltk.tree.Tree]:
        """Gera a lista de sentenças com tokens NER

        Realiza o reconhecimento de entidades nomeadas (NER) das sentenças
        retornadas por :attr:`sents` utilizando a função
        :meth:`nltk.ne_chunk_sents`.

        :return: iterador de lista de tokens NER
        :rtype: Iterator[list]
        """
        for sent in nltk.ne_chunk_sents(self.sents_pos):
            yield sent

    def top_words(self, n: int = 10) -> Iterator[tuple]:
        """Gera as palavras (tokens) mais frequentes no texto

        :param n: número de palavras a retornar
        :type n: int
        :return: iterador de tupla (palavra, frequência)
        :rtype: Iterator[list]
        """
        freq = nltk.FreqDist(_ for _ in self.sents_clean for _ in _)

        for word, top in freq.most_common(n):
            yield word, top

    def top_bigram(self, n: int = 10) -> Iterator[tuple]:
        """Gera os bigramas mais frequentes no texto

        :param n: número de bigramas a retornar
        :type n: int
        :return: iterador de tupla (palavra, frequência)
        :rtype: Iterator[list]
        """
        bigrams = nltk.ngrams([_ for _ in self.sents_clean for _ in _], 2)
        freq = nltk.FreqDist(bigrams)
        for bigram, top in freq.most_common(n):
            yield bigram, top
