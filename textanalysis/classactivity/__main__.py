from textanalysis.classactivity import News
from rich.table import Table
from rich.console import Console


if __name__ == '__main__':
    news = News()
    console = Console(width=80)
    table = Table(show_header=True, show_lines=True, width=80)

    table.add_column('', justify='center')
    table.add_column('Atividade')
    table.add_column('Resultado', justify='right')

    act = 'Contar o número de palavras no texto'
    res = str(news.sents_words_len)
    table.add_row('01', act, res)

    act = 'Imprimir as 10 palavras mais utilizadas'
    res = '\n'.join(['{}: {:3}'.format(w, n) for w, n in news.top_words()])
    table.add_row('02', act, res)

    act = 'Imprimir os 10 bigramas mais utilizados'
    res = '\n'.join(['{}: {:3}'.format(w, n) for w, n in news.top_bigram()])
    table.add_row('03', act, res)

    act = 'Contar o número de sentenças no texto'
    res = str(news.sents_len)
    table.add_row('04', act, res)

    act = 'Realizar a classificação gramatical (POS e NER)'
    res = 'News.sents_pos\nNews.sents_ner'
    table.add_row('05', act, res)

    console.print(table)
    # for word, top in c.top_words():
    #     print(word, top)
    # for b, top in c.top_bigram():
    #     print(b, top)
    # print(list(c.sents_pos))
    # for tree in c.sents_ner:
    #     print(type(tree))

