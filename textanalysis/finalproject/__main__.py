import itertools
import os

from atividade_final import trabalho_final
from rich.table import Table
from rich.console import Console

if __name__ == '__main__':
    """  topn: int    

    Variável que define a quantidade de itens (TOP N) que serão demonstrados ao longo da execução do programa, tanto na
    saída texto quanto nos gráficos. Aumentar ou diminuir este valor não altera significativamente o tempo de 
    processamento, visto que o mais demorado é o processamentos do texto em si, não a contabilização do TOP N.
    """
    topn = 50

    """ s: Subtitles

    Classe que extrai o texto de todas as legendas encontradas na pasta passada como parâmetro. Possui duas principais
    funcionalidades:    
        s.subtitles_text: lista onde cada item é o texto de uma das legendas encontradas na pasta
        str(s): retorna um único objeto de texto contendo todas as legendas da lista acima concatenadas, separadas por
                duas linhas em branco (\n\n). 
    """

    dadospath = os.path.dirname(__file__) + '/../dados/'

    # s = Subtitles('dados/Breaking.Bad')
    # s = Subtitles('dados/The.Simpsons')
    s = trabalho_final.Subtitles(dadospath + '/Friends')

    """ ps: ProjetoFinalSpacy()
        pn: ProjetoFinalNLTK()

    Armazenam o objeto principal contendo toda a lógica de cada um dos algoritmos de análise de texto: Spacy e NLTK. As
    duas classes possuem os seguintes atributos:

        .tokens: lista com todos os tokens detectados pelo algoritmo
        .tokens_pron_verb: lista de bigramas que são pares de pronomes seguidos por um verbo        
        .trigrams: lista de todos os trigramas
        .vocabulary: lista de palavras únicas        

        .ner: lista contendo todos os tokens detectadas como NER
        .ner_person: lista de tokens NER especificamente da classe "PESSOAS"
        .ner_location: lista de tokens NER especificamente da classe "LOCAIS"

        .wordcloud: armazena a nuvem de palavras de todos os tokens (sem os stopwords)
        .summary: armazena o texto resumido de todo o texto carregado pela classe
        .summary_keywords: palavras chaves (apenas as raízes) do texto resumido

        atributos "<nome>_len": armazena o tamanho da lista retornada pelo atributo <nome>
        atributos "<nome>_frequency": armazena o objeto Counter do atributo <nome> (para fazer seu TOP N)

    Cada classe pode ser criada com os seguintes parâmetros:

        Spacy(text, selectfor)
            text: texto (string) para realizar a separação em sentenças e tokenização. Pode ser também uma lista de 
            strings. Se o tamanho do texto passar de nlp.max_length, é obrigatório dividí-lo antes, podendo passar 
            então como uma lista de strings.

            selectfor: pode ser "accuracy", onde será selecionado um pipile de treinamento mais veloz, porém mais lento.
            Ou "efficiency", onde será selecionado um pipeline de treinamento bem mais lento, porém mais preciso. 

        NLTK(text)
            text: texto (string) para realizar a separação em sentenças e tokenização.
    """

    ps = trabalho_final.ProjetoFinalSpacy(text=s.subtitles_text)
    pn = trabalho_final.ProjetoFinalNLTK(text=str(s))

    """
    A partir daqui, todo o código trata puramente de formatar corretamente o conteúdo dos atributos acima citados, para
    apresentar o resultado do NLTK e SPACY lado a lado permitindo, visualmente, analisar a diferença dos algoritimos.
    """

    t_fmtstr = '\n\n{:24} {:>22} {:>46}'
    d_fmtstr = '{:02} {:>40} : {:<4} {:>40} : {:<4}'

    #
    # Contagem de sentenças
    #

    console = Console(width=120)
    tablelist = []

    table = Table(show_header=True, width=120)
    table.add_column("Contagem")
    table.add_column("Spacy", justify="right")
    table.add_column("NLTK")

    table.add_row('Tokens', str(ps.tokens_len), str(pn.tokens_len))
    table.add_row('Sentenças', str(ps.sentences_len), str(pn.sentences_len))
    table.add_row('Vocabulário', str(len(ps.vocabulary)), str(len(pn.vocabulary)))
    table.add_row('Entidades NER', str(ps.ner_len), str(pn.ner_len))
    table.add_row('Entidades NER Pessoas', str(ps.ner_person_len), str(pn.ner_person_len))
    table.add_row('Entidades NER Locais', str(ps.ner_location_len), str(pn.ner_location_len))

    tablelist.append(table)

    for table in tablelist:
        console.print(table)

    #
    # Vocabulário
    #

    zipped = itertools.zip_longest \
        ([ps.vocabulary[s - 5:s] for s in range(5, len(ps.vocabulary) + 5, 5)],
                                   [pn.vocabulary[s - 5:s] for s in range(5, len(pn.vocabulary) + 5, 5)],
                                   fillvalue='-')
    print('\n\n{:20} {:>74} | {:<}'.format('Vocabulário', 'SPACY', 'NLTK'))
    for i, (spacy_v, nltk_v) in enumerate(zipped):
        print('{:04} {:>90} | {:<90}'.format(i + 1, str(', '.join(spacy_v)), str(', '.join(nltk_v))))

    #
    # Frequência de palavras relevantes (com gráfico de colunas ou barras)
    #

    zipped = itertools.zip_longest(ps.tokens_frequency.most_common(topn),
                                   pn.tokens_frequency.most_common(topn),
                                   fillvalue=('-', 0))
    highest_v = 0
    print(t_fmtstr.format('Top Tokens', 'SPACY', 'NLTK'))
    for i, ((spacy_v, spacy_n), (nltk_v, nltk_n)) in enumerate(zipped):
        if spacy_n > highest_v:
            highest_v = spacy_n
        if nltk_n > highest_v:
            highest_v = nltk_n
        print(d_fmtstr.format(i + 1, str(spacy_v), spacy_n, str(nltk_v), nltk_n))

    highest_v = ((highest_v - (highest_v % 100)) + 100)
    ps.plot(ps.tokens_frequency, title=f"TOP {topn} Tokens: SPACY",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_tokens_spacy.png")
    pn.plot(pn.tokens_frequency, title=f"TOP {topn} Tokens: NLTK",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_tokens_nltk.png")

    #
    # Trigramas relevantes (com gráfico de colunas ou barras)
    #

    zipped = itertools.zip_longest(ps.trigrams_frequency.most_common(topn),
                                   pn.trigrams_frequency.most_common(topn),
                                   fillvalue=('-', 0))
    highest_v = 0
    print(t_fmtstr.format('Top Trigramas', 'SPACY', 'NLTK'))
    for i, ((spacy_v, spacy_n), (nltk_v, nltk_n)) in enumerate(zipped):
        if spacy_n > highest_v:
            highest_v = spacy_n
        if nltk_n > highest_v:
            highest_v = nltk_n
        print \
            (d_fmtstr.format(i + 1, str(spacy_v), spacy_n, str(nltk_v), nltk_n))

    highest_v = ((highest_v - (highest_v % 100)) + 100)
    ps.plot(ps.trigrams_frequency, title=f"TOP {topn} Trigramas: SPACY",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_trigrams_spacy.png")
    pn.plot(pn.trigrams_frequency, title=f"TOP {topn} Trigramas: NLTK",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_trigrams_nltk.png")

    #
    # Quais locais (entidades da classe LOCAL) são citados no texto processado?
    # Quantas vezes cada local é citado?
    #
    zipped = itertools.zip_longest(ps.ner_person_frequency.most_common(topn),
                                   pn.ner_person_frequency.most_common(topn),
                                   fillvalue=('-', 0))
    highest_v = 0
    print(t_fmtstr.format('Top Pessoas', 'SPACY', 'NLTK'))
    for i, ((spacy_v, spacy_n), (nltk_v, nltk_n)) in enumerate(zipped):
        if spacy_n > highest_v:
            highest_v = spacy_n
        if nltk_n > highest_v:
            highest_v = nltk_n
        print \
            (d_fmtstr.format(i + 1, str(spacy_v), spacy_n, str(nltk_v), nltk_n))

    highest_v = ((highest_v - (highest_v % 100)) + 100)
    ps.plot(ps.ner_person_frequency, title=f"TOP {topn} Pessoas: SPACY",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_person_spacy.png")
    pn.plot(pn.ner_person_frequency, title=f"TOP {topn} Pessoas: NLTK",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_person_nltk.png")

    zipped = itertools.zip_longest(ps.ner_location_frequency.most_common(topn),
                                   pn.ner_location_frequency.most_common(topn),
                                   fillvalue=('-', 0))
    highest_v = 0
    print(t_fmtstr.format('Top Locais', 'SPACY', 'NLTK'))
    for i, ((spacy_v, spacy_n), (nltk_v, nltk_n)) in enumerate(zipped):
        if spacy_n > highest_v:
            highest_v = spacy_n
        if nltk_n > highest_v:
            highest_v = nltk_n
        print \
            (d_fmtstr.format(i + 1, str(spacy_v), spacy_n, str(nltk_v), nltk_n))

    highest_v = ((highest_v - (highest_v % 100)) + 100)
    ps.plot(ps.ner_location_frequency, title=f"TOP {topn} Locais: SPACY",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_location_spacy.png")
    pn.plot(pn.ner_location_frequency, title=f"TOP {topn} Locais: NLTK",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_location_nltk.png")

    #
    # Qual é a proporção de pronomes frente aos verbos do texto?
    #

    zipped = itertools.zip_longest \
        (ps.tokens_pron_verb_frequency.most_common(topn),
                                   pn.tokens_pron_verb_frequency.most_common(topn),
                                   fillvalue=('-', 0))
    highest_v = 0
    print(t_fmtstr.format('Top Pron-Verb', 'SPACY', 'NLTK'))
    for i, ((spacy_v, spacy_n), (nltk_v, nltk_n)) in enumerate(zipped):
        if spacy_n > highest_v:
            highest_v = spacy_n
        if nltk_n > highest_v:
            highest_v = nltk_n
        print \
            (d_fmtstr.format(i + 1, str(spacy_v), spacy_n, str(nltk_v), nltk_n))

    highest_v = ((highest_v - (highest_v % 100)) + 100)
    ps.plot(ps.tokens_pron_verb_frequency, title=f"TOP {topn} Pron-Verb: SPACY",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_pron_verb_spacy.png")
    pn.plot(pn.tokens_pron_verb_frequency, title=f"TOP {topn} Pron-Verb: NLTK",
            limit=topn, xlimit=highest_v, filename=dadospath + "/g_top_pron_verb_nltk.png")

    #
    # Nuvem de palavras
    #

    ps.wordcloud.to_file(dadospath + '/g_wordcloud_spacy.png')
    pn.wordcloud.to_file(dadospath + '/g_wordcloud_nltk.png')

    # TODO
    # Obtenha um resumo dos textos utilizados, acompanhados das palavras-chave
