import dsutils
from textanalysis.classactivity import News


def ex01():
    news = News()
    ex = dsutils.DSExercise('Atividade da Aula do dia 05/03')

    ex.item(
        'Contar o número de palavras no texto',
        '{:>50s}'.format(str(news.sents_words_len))
    )

    ex.item(
        'Imprimir as 10 palavras mais utilizadas',
        '\n'.join(
            ['{:>50s}: {:3}'.format(w, n) for w, n in news.top_words()]
        )
    )

    ex.item(
        'Imprimir os 10 bigramas mais utilizados',
        '\n'.join(
            ['{:>50s}: {:3}'.format(str(b), n) for b, n in news.top_bigram()]
        )
    )

    ex.item(
        'Contar o número de sentenças no texto',
        '{:>50s}'.format(str(news.sents_len))
    )

    ex.item(
        'Realizar a classificação gramatical (POS e NER)',
        'Mostrando apenas o primeiro parágrafo, veja a implementação de '
        'News.sents_pos e News.sents_ner',
        '\n\nPOS\n' + str(next(news.sents_pos)),
        '\n\nNER\n' + str(next(news.sents_ner)).replace('\n', '')
    )

    ex.print()


if __name__ == '__main__':
    ex01()
