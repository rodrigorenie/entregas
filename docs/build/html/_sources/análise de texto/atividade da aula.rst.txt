Atividade da Aula
=================

.. seealso::
    :ref:`Resultados` > :ref:`Resultados de Análise de Texto`

Selecione uma notícia completa, copie-a e salve-a em um arquivo de texto. Utilize a notícia baixada e crie um script que
realize o que se pede.


.. topic:: Contar o número de palavras no texto

    Implementado em :attr:`textanalysis.classactivity.News.sents_words_len`

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_words_len

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents


.. topic:: Imprimir as 10 palavras mais utilizadas

    Implementado em :attr:`textanalysis.classactivity.News.top_words`

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_words

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_clean


.. topic:: Imprimir os 10 bigramas mais utilizados

    Implementado em :attr:`textanalysis.classactivity.News.top_bigram`

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_bigram


.. topic:: Contar o número de sentenças no texto

    Implementado em :attr:`textanalysis.classactivity.News.sents_len`

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_len


.. topic:: Realizar a classificação gramatical (POS e NER)

    Implementado em :attr:`textanalysis.classactivity.News.sents_pos`

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_pos

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_ner
