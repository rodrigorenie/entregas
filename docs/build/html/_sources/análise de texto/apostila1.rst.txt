Exercícios da Apostila 1
==============================

.. seealso::
    :ref:`Resultados` > :ref:`Resultados de Análise de Texto`


Apostila 1 Exercitando 01
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

-----

.. topic:: Imprima as palavras dos documentos ``neg/cv002_tok-3321.txt`` e
    ``pos/cv003_tok-8338.txt``

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex01.words`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
        :linenos:
        :pyobject: Ex01.words


Apostila 1 Exercitando 02
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: Utilize o arquivo ``Noticia_1`` disponível na pasta de dados da
    turma e liste os 50 bigramas e trigramas mais frequentes obtidos do texto.

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex02.top_bigrams`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
        :linenos:
        :pyobject: Ex02.top_bigrams

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex02.top_trigrams`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
        :linenos:
        :pyobject: Ex02.top_trigrams


Apostila 1 Exercitando 03
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

-----

.. topic:: Analise a frequência das palavras ``['the', 'that']`` no arquivo
    ``singles.txt`` e, depois, no arquivo ``pirates.txt``.

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex03.tokens_freq`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
            :linenos:
            :pyobject: Ex03.tokens_freq

-----

.. topic:: Inclua a geração do gráfico de frequência.

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex03.tokens_freq_plot`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
            :linenos:
            :pyobject: Ex03.tokens_freq_plot

-----

.. topic:: Gere a lista dos 15 bigramas mais frequentes do texto.

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex03.top_bigrams`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
            :linenos:
            :pyobject: Ex03.top_bigrams

-----

.. topic:: Gere a lista dos 20 quadrigramas gramas mais frequentes que possuam a
    palavra ``life``.

    Implementado em :meth:`textanalysis.booklet.booklet1.Ex03.top_life_quadrigrams`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
            :linenos:
            :pyobject: Ex03.top_life_quadrigrams



Apostila 1 Exercitando 04
******************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: O NLTK possui um corpus com as obras de Machado de Assis
    (``from nltk.corpus import machado``):

    1.	Execute ``print(machado.readme())`` para conhecer melhor o corpus
    2.	Utilizando o corpus machado, elabore um programa que atenda aos
        requisitos:

        a. Quais são as categorias presentes no corpus?
        b. Quais são os documentos dentro desse corpus?
        c. Imprima o conteúdo do arquivo do documento que contem a obra Memórias Postumas de Braz Cubas.
        d. Analise a frequência das palavras ``['olhos', 'estado']`` em Memórias Postumas de Bras Cubas.
        e. Quantas palavras há no texto? Use ``len(texto)``.
        f. Quantas palavras distintas há na obra?
        g. Qual é o vocabulário (palavras) presentes na obra?
        h. Quais são os 15 termos mais repetidos no texto de Machado de Assis?
        i. Tabular a frequência de palavras.
        j. Gerar um gráfico com os 15 termos mais repetidos.
        k. Remova os termos indesejados  e repita as questões ``h`` a ``j``.
        l. Obter a lista de todos os trigramas do texto.
        m. Obter a lista dos 15 bigramas que contenham a palavra ``olhos``.
        n. Gerar o gráfico dos bigramas com a palavra ``olhos``.

    Implementado na função :func:`textanalysis.booklet.booklet1.ex04`

    .. literalinclude:: ../../../textanalysis/booklet/booklet1.py
        :linenos:
        :pyobject: ex04
