Apostila Parte 0
========================

Documentação da solução aplicada nos exercícios da Apostila - Parte 0. Aqui é
detalhado como cada item solicitado nos exercícios foram implementados. Caso
deseje apenas visualizar os resultados, execute os comandos descritos em
:ref:`verificando-resultados`.

Exercitando 01
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

-----

.. topic:: Crie uma string com o conteúdo "Ainda que falasse as línguas dos
    homens e falasse a língua dos anjos, sem amor eu nada seria."

    Implementado no construtor da Classe
    :class:`atividade_apostila.apostila0.Exercitando01`. A string acima deve
    ser passado como parâmetro.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01
        :end-before: def __str__

-----

.. topic:: Imprima cada caractere da string

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando01.text_chars`. A
    impressão na tela deve ser realizado fora do escopo deste método.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_chars

-----

.. topic:: Segmente a string em uma lista

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando01.text_split`.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_split

-----

.. topic:: Quantas palavras há na lista?

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando01.text_split_len`.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_split_len


-----

.. topic:: Imprima cada palavra da string

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando01.text_split`. A
    impressão na tela deve ser realizado fora do escopo deste método.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_split

-----

.. topic:: Substitua o termo "dos homens" por "do mundo"

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando01.text_replace`. Os
    termos devem ser passados como parâmetros.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_replace

-----

.. topic:: Imprima o fragmento que vai do 21º até o 30º caracteres

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando01.text_segment`. O
    método deve ser invocado passando os valores ``21`` e ``30`` conforme
    requisitado neste item.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_segment

-----

.. topic:: Imprima os últimos 15 caracteres

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando01.text_last`. O método
    deve ser invocado passando o valor ``15`` conforme requisitado neste item.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_last

-----

.. topic:: Salve a sentença em um arquivo do tipo txt

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando01.text_save`. O método
    deve ser invocado passando o caminho, relativo ou total, do arquivo de
    texto.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando01.text_save

Exercitando 02
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

-----

.. topic:: Crie uma lista com os parágrafos do documento

    Implementado no construtor da Classe
    :class:`atividade_apostila.apostila0.Exercitando02`. O caminho do ``docx``
    deve ser passado como parâmetro.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02
        :end-before: @property

-----

.. topic:: Crie uma lista com os parágrafos do documento

    A propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando02.paragraphs` cria um
    gerador com todos os parágrafos do documento, enquanto a propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando02.paragraphs_list`
    cria uma lista a partir deste gerador.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_list

-----

.. topic:: Quantos parágrafos o documento possui?

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando02.paragraphs_len`, que
    retorna o tamanho da lista gerado por
    :py:attr:`atividade_apostila.apostila0.Exercitando02.paragraphs_list`.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_len

-----

.. topic:: Imprima o conteúdo do 1º parágrafo do texto

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando02.paragraphs_segment`.
    Passando ``1`` como valor do parâmetro ``first``, é retornado o primeiro
    parágrafo. A impressão na tela deve ser realizado fora do escopo deste
    método.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_segment

-----

.. topic:: Imprima os parágrafos 3 a 6, inclusive

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando02.paragraphs_segment`.
    Passando ``3`` como valor do parâmetro ``first`` e ``6`` para o ``last`` é
    retornado os parágrafos requisitados. A impressão na tela deve ser
    realizado fora do escopo deste método.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_segment

-----

.. topic:: O termo "Machado" está no documento?

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando02.paragraphs_hastext`.
    O termo deve ser passado como parâmetro para o método. A impressão na tela
    deve ser realizado fora de seu escopo.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_hastext

-----

.. topic:: Crie um  texto corrido a partir dos parágrafos lidos

    Implementado na propriedade
    :py:attr:`atividade_apostila.apostila0.Exercitando02.paragraphs_text`, que
    retorna uma string com todos os parágrafos do documento. A impressão na
    tela deve ser realizado do escopo desta propriedade.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_text

-----

.. topic:: Substitua o termo "Batista" por "João Batista"

    Implementado no método
    :py:meth:`atividade_apostila.apostila0.Exercitando02.paragraphs_replacetext`.
    Passando ``Batista`` como valor do parâmetro ``old`` e ``João Batista``
    para o ``new``, é retornado o texto com os termos substituidos. A impressão
    na tela deve ser realizado fora do escopo deste método.

    .. literalinclude:: ../../atividade_apostila/apostila0.py
        :linenos:
        :pyobject: Exercitando02.paragraphs_replacetext
