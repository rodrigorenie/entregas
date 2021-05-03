Exercícios da Apostila 0
==============================

.. seealso::
    :ref:`Resultados` > :ref:`Resultados de Análise de Texto`


Apostila 0 Exercitando 01
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento. Lembre-se de salvar seu programa, para
estudos posteriores.


.. topic:: Crie uma string com o conteúdo "Ainda que falasse as línguas dos homens e falasse a língua dos anjos, sem
    amor eu nada seria."

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex01.text`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text


.. topic:: Imprima cada caractere da string

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex01.text_chars`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_chars


.. topic:: Segmente a string em uma lista

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex01.text_split`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_split


.. topic:: Quantas palavras há na lista?

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex01.text_split_len`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_split_len


.. topic:: Imprima cada palavra da string

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex01.text_split`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_split


.. topic:: Substitua o termo "dos homens" por "do mundo"

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex01.text_replace`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_replace


.. topic:: Imprima o fragmento que vai do 21º até o 30º caracteres

    Implementado na propriedade
    :py:attr:`textanalysis.booklet.booklet0.Ex01.text_segment`. O
    método deve ser invocado passando os valores ``21`` e ``30`` conforme
    requisitado neste item.

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_segment


.. topic:: Imprima os últimos 15 caracteres

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex01.text_last`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_last


.. topic:: Salve a sentença em um arquivo do tipo txt

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex01.text_save`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex01.text_save


Apostila 0 Exercitando 02
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.


.. topic:: Crie uma lista com os parágrafos do documento

    Implementado no construtor da Classe
    :class:`textanalysis.booklet.booklet0.Ex02`. O caminho do ``docx``
    deve ser passado como parâmetro.

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02
        :end-before: @property

-----

.. topic:: Crie uma lista com os parágrafos do documento

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex02.paragraphs_list`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_list

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs


.. topic:: Quantos parágrafos o documento possui?

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex02.paragraphs_len`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_len


.. topic:: Imprima o conteúdo do 1º parágrafo do texto

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex02.paragraphs_segment`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_segment


.. topic:: Imprima os parágrafos 3 a 6, inclusive

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex02.paragraphs_segment`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_segment


.. topic:: O termo "Machado" está no documento?

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex02.paragraphs_hastext`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_hastext


.. topic:: Crie um  texto corrido a partir dos parágrafos lidos

    Implementado em :attr:`textanalysis.booklet.booklet0.Ex02.paragraphs_text`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_text


.. topic:: Substitua o termo "Batista" por "João Batista"

    Implementado em :meth:`textanalysis.booklet.booklet0.Ex02.paragraphs_replacetext`

    .. literalinclude:: ../../../textanalysis/booklet/booklet0.py
        :linenos:
        :pyobject: Ex02.paragraphs_replacetext
