import os
import docx

from typing import Generator


class Exercitando01:
    """Classe que implementa os itens solicitado no Exercitando 1 da apostila "Parte 0". Cada método desta classe
    implementa um item solicitado.

    :param text: String utilizado como base para o exercício. O padrão é None, o que siginifica que será utilizado a
        seguinte sentaça: "Ainda que falasse as línguas dos homens e falasse a língua dos anjos, sem amor eu nada
        seria."
    :type text: str, optional
    :rtype: None
    """

    def __init__(self, text: str = None) -> None:
        self.text = text if text else 'Ainda que falasse as línguas dos homens e falasse a língua dos anjos, ' \
                                      'sem amor eu nada seria.'

    def chars(self) -> Generator[str, None, None]:
        """Cria um gerador pora cada caracter do texto.

        :rtype: None
        """
        for c in self.text:
            yield c

    def words(self) -> Generator[str, None, None]:
        """Divide o texto em uma lista de palavras (separadas por um espaço em branco) e cria um gerador com cada item
        da lista.

        :rtype: None
        """
        for w in self.text.split():
            yield w

    def words_len(self) -> int:
        """Contabiliza o tamanho da lista do gerador criado no método :func:`Exercitando01.words`.

        :rtype: int
        """
        return len(list(self.words()))

    def replace(self, t_from: str = 'dos homens', t_to: str = 'do mundo') -> str:
        """Substitui um trecho no texto indicado pelo parâmetro t_from pelo texto indicado no parâmetro t_to. Os dois
        parâmetros são opcionais, assumindo os valores 'dos homens' e 'do mundo' por padrão, respectivamente.

        :param t_from: Texto original a ser substituído
        :type: str, optional
        :param t_to: Texto a substituir

        :return: Uma cópia do texto substituído
        :rtype: str
        """
        self.text = self.text.replace(t_from, t_to)
        return self.text

    def segment(self, p_ini: int = 21, p_end: int = 30) -> str:
        """Retorna o segmento do texto indicado, da posição inicial p_ini até a posição final p_end, ambos INCLUSIVO, ou
        seja, retorna o caracter da posição indicada. Além disso, este método considera que o primeiro caracter do texto
        está na posição 1. Os parâmetros p_ini e p_end são opcionais e assumem os valores 21 e 30 por padrão
        respectivamente.

        :raises ValueError: Erro gerado nas seguintes condições:
            - Quando o valor inicial é menor ou igual a zero;
            - Quando o valor inicial é menor que o valor final;
        :raises IndexError: Erro gerado quando

        :param p_ini: Posição inicial do segmento (deve ser maior que zero)
        :param p_end: Posição final do segmento
        :return: Segmento do texto
        :rtype: str
        """
        if p_ini <= 0:
            raise ValueError('p_ini must be 1 or higher')

        if p_end < p_ini:
            raise ValueError('p_end must be equal or greater than p_ini')

        return self.text[p_ini-1:p_end]

    def last(self, n: int = 15) -> str:
        """Returna os últimos caracteres do texto, de tamanho indicado pelo parâmetro n. O parâmetro n é opcional com
        valor padrão 15.

        :param n: Tamanho do segmento
        :type: int, optional

        :raises IndexError: se o tamanho do segmento é maior que o texto em si.

        :return: Segmento do texto dos últimos n caracteres
        :rtype: str
        """
        return self.text[-n:]

    def save(self, filename: str = 'apostila01_ex01.txt') -> str:
        """Salva o texto em um arquivo indicado pelo parâmetro opcional filename, cujo valor padrão é
        'apostila_ex01.txt' (salva na pasta corrente).

        :param filename:
        :type: str, optional

        :return: Caminho completo do arquivo salvo
        :rtype: str
        """
        with open(filename, 'w') as f:
            f.write(self.text + '\n')
            return os.path.abspath(filename)


class Exercitando02:

    def __init__(self, docpath:str) -> None:
        self.doc = docx.Document(docpath)
        self._paragraphs = []
        self._paragraphs_text = ''

    def paragraphs(self) -> list[str]:
        self._paragraphs = [p.text for p in self.doc.paragraphs]
        return self._paragraphs

    def paragraphs_len(self):
        return len(self._paragraphs)

    def paragraphs_segment(self, first: int = 1, last: int = None) -> list[str]:
        if first <= 0:
            raise ValueError('first parameter must be greater or equal to one')

        if last and first > last:
            raise ValueError('last parameter must be greater or equal to first')

        if last:
            return self._paragraphs[first - 1:last]
        else:
            return self._paragraphs[first - 1]

    def text_exists(self, text: str) -> bool:
        return text in '\n'.join(self._paragraphs)

    def paragraphs_text(self) -> str:
        self._paragraphs_text = '\n'.join(self._paragraphs)
        return self._paragraphs_text

    def text_replace(self, old: str, new: str) -> str:
        self._paragraphs_text = self._paragraphs_text.replace(old, new)
        return self._paragraphs_text
