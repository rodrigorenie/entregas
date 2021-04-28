.. _textanalysis.classactivity:

Atividade da Aula
=================

Selecione uma notícia completa, copie-a e salve-a em um arquivo de texto. Utilize a notícia baixada e crie um script que
realize o que se pede.


.. config:option:: Contar o número de palavras no texto

    :attr:`textanalysis.classactivity.News.sents_words_len`:

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_words_len

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents


.. config:option:: Imprimir as 10 palavras mais utilizadas

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_words

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_clean


-----

.. topic:: Imprimir os 10 bigramas mais utilizados

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_bigram


-----

.. topic:: Contar o número de sentenças no texto

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_len


-----

.. topic:: Realizar a classificação gramatical (POS e NER)

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_pos

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_ner


-----

.. program-output:: python -m textanalysis.classactivity
    :cwd: ../../../
    :caption:

.. program-output:: python -c "print('olá')"

.. _NLTK: https://www.nltk.org
.. _GoogleDrive: https://docs.google.com/document/d/13s6jq6--Ouh3eGQ8qKt1urZbT49Sq2eXM2drTfZT0EQ/edit?usp=sharing