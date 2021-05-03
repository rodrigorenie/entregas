Apostila Parte 1
========================

Documentação da solução aplicada nos exercícios da Apostila - Parte 1. Aqui é
detalhado como cada item solicitado nos exercícios foram implementados. Caso
deseje apenas visualizar os resultados, execute os comandos descritos em
:ref:`verificando-resultados`.

Exercitando 01
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: Imprima as palavras dos documentos ``neg/cv002_tok-3321.txt`` e
    ``pos/cv003_tok-8338.txt``

    Implementado na função :py:func:`atividade_apostila.apostila1.ex01`.

    .. literalinclude:: ../../atividade_apostila/apostila1.py
        :linenos:
        :pyobject: ex01

Exercitando 02
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: Utilize o arquivo ``Noticia_1`` disponível na pasta de dados da
    turma e liste os 50 bigramas e trigramas mais frequentes obtidos do texto.

    Implementado na função :py:func:`atividade_apostila.apostila1.ex02`.

    .. literalinclude:: ../../atividade_apostila/apostila1.py
        :linenos:
        :pyobject: ex02

Exercitando 03
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

#. Analise a frequência das palavras ``['the', 'that']`` no arquivo
   ``singles.txt`` e, depois, no arquivo ``pirates.txt``.
#. Inclua a geração do gráfico de frequência.
#. Gere a lista dos 15 bigramas mais frequentes do texto.
#. Gere a lista dos 20 quadrigramas gramas mais frequentes que possuam a
   palavra ``life``.

Implementado na função :py:func:`atividade_apostila.apostila1.ex03`.

.. literalinclude:: ../../atividade_apostila/apostila1.py
    :linenos:
    :pyobject: ex03

Exercitando 04
************************

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

    Implementado na função :py:func:`atividade_apostila.apostila1.ex04`.

    .. literalinclude:: ../../atividade_apostila/apostila1.py
        :linenos:
        :pyobject: ex04
