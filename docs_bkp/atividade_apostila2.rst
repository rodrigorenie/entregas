Apostila Parte 2
========================

Documentação da solução aplicada nos exercícios da Apostila - Parte 2. Aqui é
detalhado como cada item solicitado nos exercícios foram implementados. Caso
deseje apenas visualizar os resultados, execute os comandos descritos em
:ref:`verificando-resultados`.

Exercitando 01
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: Utilize o arquivo com a obra Memórias Póstumas de Bras Cubas e
    compare os stemms obtidos a partir do 6º e 7º parágrafos do texto. Utilize
    Porter, Lancaster e RSPL.

    Implementado na função :py:func:`atividade_apostila.apostila2.ex01`.

    .. literalinclude:: ../../atividade_apostila/apostila2.py
        :linenos:
        :pyobject: ex01

Exercitando 02
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

#. Utilize o arquivo ``Noticia_1`` disponível na pasta de dados da turma e
   realize as tarefas de POS e NER.
#. Salve o resultado de POS em um arquivo, com ``<seu_nome>_POS_Noticia1``
#. Salve o resultado de NER em um arquivo, com ``<seu_nome>_NER_Noticia1``

Implementado na função :py:func:`atividade_apostila.apostila2.ex02`.

.. literalinclude:: ../../atividade_apostila/apostila2.py
    :linenos:
    :pyobject: ex02

Exercitando 03
************************

Execute o que se pede. Logo após, cole a solução do exercício neste documento.
Lembre-se de salvar seu programa, para estudos posteriores.

.. topic:: O NLTK possui um corpus com as obras de Machado de Assis
    (``from nltk.corpus import machado``):

    1. Execute ``print(machado.readme())`` para conhecer melhor o corpus
    2. Utilizando oo documentos relativos a Dom Casmurro e O alienista, faça o
       que se pede:

        a. Classifique as palavras de acordo com suas classes gramaticais de
           cada documento. Salve o corpus POS Tagged em uma planilha ou texto
           para uso posterior. É importante manter a informação sobre o
           documento origem dos novos documentos;
        b. Obtenha a lista de entidades em cada documento, salvando para uso
           posterior;
        c. Analisando os documentos marcados (tagged) tanto POS quanto NER,
           quais são as classes mais utilizadas?
        d. Observe que há uma tendência de que termos menos relevantes para a
           análise sejam mais frequentes. Então, repita os procedimentos
           anteriores, mas com os termos que são relevantes para uma análise do
           que está sendo falado (trata-se de uma análise preliminar e ainda
           superficial do discurso);
        e. Determine o vocabulário comum entre os textos
        f. Determine a frequência de termos comuns nos dois textos,
           separadamente;
        g. Determine a frequência de termos comuns utilizados pelo autor
           considerando os dois textos.
        h. *Desafio*: Quais são as entidades mais citadas pelo autor?

Implementado na função :py:func:`atividade_apostila.apostila2.ex03`.

.. literalinclude:: ../../atividade_apostila/apostila2.py
    :linenos:
    :pyobject: ex03
