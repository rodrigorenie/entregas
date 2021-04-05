Atividade Final
================

Documentação da solução aplicada a Atividade Final. Aqui é detalhado como cada
item solicitado foi implementado. Caso deseje apenas visualizar os resultados,
execute os comandos descritos em :ref:`verificando-resultados`.

.. topic:: Analisar textos: os textos baixados podem estar relacionados com um
    interesse da equipe, mas devem ser baixadas, no mínimo, 50.000 (cinquenta
    mil sentenças).

    Para a análise, deve-se produzir:

    #. Contagem de sentenças
    #. Vocabulário
    #. Frequência de palavras relevantes (com gráfico de colunas ou barras)
    #. Trigramas relevantes (com gráfico de colunas ou barras)
    #. Quais locais (entidades da classe LOCAL) são citados no texto processado?
    #. Quantas vezes cada local é  citado?
    #. Qual é a proporção de pronomes frente aos verbos do texto?
    #. Nuvem de palavras
    #. Obtenha um resumo dos textos utilizados, acompanhados das palavras-chave

Análise NLTK
************************

A análise utilizando NLTK foi implementada na Classe
:py:class:`atividade_final.trabalho_final.ProjetoFinalNLTK`.

    .. literalinclude:: ../../atividade_final/trabalho_final.py
        :linenos:
        :pyobject: ProjetoFinalNLTK

Análise Spacy
************************

A análise utilizando Spacy foi implementada na Classe
:py:class:`atividade_final.trabalho_final.ProjetoFinalSpacy`.

    .. literalinclude:: ../../atividade_final/trabalho_final.py
        :linenos:
        :pyobject: ProjetoFinalSpacy
