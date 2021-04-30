import os
import docx

from typing import Optional, Union, Iterator


class Ex01:
    """Implementa a atividade descrita em :ref:`Apostila 0 Exercitando 01`.

    :param text: Texto a ser utilizado como base para o exercício.
    :type text: str
    :rtype: None
    """

    def __init__(self, text: str = None) -> None:
        self._text = text if text else ''

    def __str__(self) -> str:
        """Define que a representação de string desta classe é o conteúdo do
        texto.

        :rtype: str
        """
        return self._text

    @property
    def text_chars(self) -> Iterator[str]:
        """Cria um gerador para os caracteres individuais do texto.

        :rtype: Iterator[str]
        """
        for char in self._text:
            yield char

    @property
    def text_split(self) -> Iterator[str]:
        """Divide o texto em uma lista de palavras, separadas por um espaço em
        branco, e cria um gerador para os itens da lista.

        :rtype: Iterator[str]
        """
        for item in self._text.split():
            yield item

    @property
    def text_split_len(self) -> int:
        """Contabiliza o tamanho da lista do gerador criado por
        :func:`Ex01.text_split`.

        :rtype: int
        """
        return len(list(self.text_split))

    def text_replace(self, old: str, new: str) -> str:
        """Substitui um trecho no texto indicado pelo parâmetro ``old`` pelo
        texto indicado no parâmetro ``new``.

        :param old: Texto original a ser substituído.
        :type old: str
        :param new: Texto novo.
        :type new: str

        :return: O texto substituído.
        :rtype: str
        """
        self._text = self._text.replace(old, new)
        return self._text

    def text_segment(self, first: int, last: Optional[int] = None) -> str:
        """Retorna o segmento do texto indicado, da posição inicial ``first``
        até a posição ``last``, ambos *INCLUSIVO*, ou seja, retorna o caracter
        das posições indicadas. Se ``last`` for omitido, retorna apenas o
        caracter indicado por ``first``.

        :raises ValueError: Erro gerado quando ``first`` é menor ou igual a
            zero ou quando ``first`` menor que ``last``.

        :param first: Posição inicial do segmento (deve ser maior que zero).
        :type first: int
        :param last: Posição final do segmento, opcional.
        :type last: int, opcional

        :return: String com o segmento do texto ou uma string vazia se
            ``first`` for maior que o tamanho do texto.
        :rtype: str
        """
        if first <= 0:
            raise ValueError('first must be 1 or higher')

        if not last:
            last = first

        if last < first:
            raise ValueError('last must be equal or greater than first')

        return self._text[first-1:last]

    def text_last(self, n: int) -> str:
        """Retorna os últimos caracteres do texto, de tamanho indicado pelo
        parâmetro ``n``, que é opcional com valor padrão ``15``.

        :param n: Tamanho do segmento.
        :type n: int, opcional

        :raises IndexError: se o tamanho do segmento é maior que o texto em si.

        :return: Segmento do texto dos últimos ``n`` caracteres.
        :rtype: str
        """
        return self._text[-n:]

    def text_save(self, filename: str) -> str:
        """Salva o texto em um arquivo indicado pelo parâmetro ``filename``.

        :param filename: Caminho do arquivo
        :type filename: str

        :return: Caminho completo do arquivo salvo
        :rtype: str
        """
        with open(filename, 'w') as f:
            f.write(self._text + '\n')
            return os.path.abspath(filename)


class Ex02:
    """Classe que implementa os itens solicitado no Exercitando 2 da apostila
    "Parte 0". Cada método desta classe implementa um item solicitado. Esta
    classe carrega um documento em formato ``docx``.

    :param docpath: Caminho do arquivo ``docx`` a ser carregado.
    :type docpath: str

    :rtype: None
    """

    def __init__(self, docpath: str) -> None:
        self._doc = docx.Document(docpath)

    @property
    def paragraphs(self) -> Iterator[str]:
        """Cria um gerador para os parágrafos encontrados no documento.

       :rtype: Iterator[str]
       """
        for paragraph in self._doc.paragraphs:
            yield paragraph.text

    @property
    def paragraphs_list(self) -> list[str]:
        """Cria uma lista contendo cada parágrafo encontrado no documento.

        :return: Lista com os parágrafos.
        :rtype: list[str]
        """
        return list(self.paragraphs)

    @property
    def paragraphs_len(self):
        """Contabiliza o tamanho da lista do gerador criado por
        :func:`Exercitando02.paragraphs`.

        :returns: Tamanho da lista.
        :rtype: int
        """
        return len(self.paragraphs_list)

    def paragraphs_segment(self, first: int,
                           last: int = None) -> Union[list[str], str]:
        """Retorna os parágrafos do documento, da posição inicial ``first`` até
        a posição ``last``, ambos *INCLUSIVO*, ou seja, também retorna os
        parágrafos nas posições indicadas. Se ``last`` for omitido, retorna
        apenas o parágrafo indicado por ``first``.

        :raises ValueError: Erro gerado quando ``first`` é menor ou igual a
            zero ou quando ``first`` menor que ``last``.

        :param first: Posição inicial do segmento (deve ser maior que zero).
        :type first: int
        :param last: Posição final do segmento.
        :type last: int, opcional

        :return: Uma lista de string com os parágrafos solicitados, ou uma
            única string de parágrafo de ``last`` for omitido.
        :rtype: list[str] ou str
        """
        if first <= 0:
            raise ValueError('first parameter must be greater '
                             'or equal to one')

        if last and first > last:
            raise ValueError('last parameter must be greater '
                             'or equal to first')

        if last:
            return self.paragraphs_list[first - 1:last]
        else:
            return self.paragraphs_list[first - 1]

    def paragraphs_hastext(self, text: str) -> bool:
        """Verifica se a string indicado pelo parâmetro ``text`` existe no
        documento.

        :param text: Texto a procurar no documento.
        :type text: str

        :return: Verdadeiro ou falso.
        :rtype: bool
        """
        return text in self.paragraphs_text

    @property
    def paragraphs_text(self) -> str:
        """Retorna uma string com o conteúdo do documento.

        :return: String do documento.
        :rtype: str
        """
        return '\n'.join(self.paragraphs_list)

    def paragraphs_replacetext(self, old: str, new: str) -> str:
        """Retorna uma string com o conteúdo do documento, substiuindo o texto
        indicado pelo parâmetro ``old`` por ``new``.

        :param old: Texto original a ser substituído.
        :type old: str
        :param new: Texto novo.
        :type new: str

        :return: String com o texto substituído.
        :rtype: str
        """
        return self.paragraphs_text.replace(old, new)
