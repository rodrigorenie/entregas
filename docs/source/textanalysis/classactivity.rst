.. _textanalysis.classactivity:

Atividade da Aula
=================

Documentação da solução aplicada na atividade da aula do dia 05/03. Aqui é
detalhado como cada item solicitado foi implementado. Caso deseje apenas
visualizar os resultados, execute os comandos descritos em
:ref:`verificando-resultados`.

A atividade consiste selecionar o texto de uma notícia e, utilizando a
biblioteca `NLTK`_, realizar as tarefas listadas na sequência.

-----

.. topic:: Contar o número de palavras no texto

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_words_len

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents


-----

.. topic:: Imprimir as 10 palavras mais utilizadas

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_words

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.sents_clean


-----

.. topic:: Imprimir os 10 bigramas mais utilizadas

    .. literalinclude:: ../../../textanalysis/classactivity/classactivity.py
        :linenos:
        :pyobject: News.top_bigram


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


.. _NLTK: https://www.nltk.org