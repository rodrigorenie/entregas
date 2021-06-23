import argparse

from textanalysis.booklet import booklet0
from textanalysis.booklet import booklet1

from dsutils import DSExercise


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='textanalysis.booklet',
        description='Imprime o resultados dos exercícios das apostilas'
    )
    parser.add_argument('-b', nargs='*',
                        choices=['booklet0', 'booklet1', 'booklet2'],
                        help='Seleciona qual apostila deseja mostrar o '
                             'resultado')

    return parser


def booklet0ex01() -> None:
    ex = booklet0.Ex01('Ainda que falasse as línguas dos homens e falasse a '
                       'língua dos anjos, sem amor eu nada seria.')

    table = DSExercise('Apostila 0 - Exercitando 01')

    table.item(
        f'Crie uma string com o conteúdo {str(ex)}',
        str(ex)
    )

    table.item(
        'Imprima cada caractere da string',
        ' '.join([c for c in ex.text_chars])
    )

    table.item(
        'Segmente a string em uma lista',
        str(list(ex.text_split))
    )

    table.item(
        'Quantas palavras há na lista?',
        table.text(str(ex.text_split_len), justify='center')
    )

    table.item(
        'Imprima cada palavra da string',
        ' | '.join(list(ex.text_split))
    )

    table.item(
        'Substitua o termo "dos homens" por "do mundo"',
        ex.text_replace('dos homens', 'do mundo')
    )

    table.item(
        'Imprima o fragmento que vai do 21º até o 30º caracteres',
        '"{}"'.format(ex.text_segment(21, 30))
    )

    table.item(
        'Imprima os últimos 15 caracteres',
        '"{}"'.format(ex.text_last(15))
    )

    table.item(
        'Salve a sentença em um arquivo do tipo txt',
        'Arquivo salvo em: {}'.format(ex.text_save('booklet0_ex01.txt'))
    )

    table.print()


def booklet0ex02() -> None:
    ex = booklet0.Ex02('ROMANCE.docx')
    table = DSExercise('Apostila 0 - Exercitando 02')

    table.item(
        'Crie uma lista com os parágrafos do documento',
        'Apenas os dois primeiros parágrafos:\n',
        str(ex.paragraphs_list[0:2])
    )

    table.item(
        'Quantos parágrafos o documento possui?',
        table.text(str(ex.paragraphs_len), justify='center')
    )

    table.item(
        'Imprima o conteúdo do 1º parágrafo  do texto',
        str(ex.paragraphs_segment(1))
    )

    table.item(
        'Imprima os parágrafos 3 a 6, inclusive',
        '\n\n'.join(ex.paragraphs_segment(3, 6))
    )

    table.item(
        'O termo ‘Machado’ está no documento?',
        table.columns(
            'Sim' if ex.paragraphs_hastext('Machado') else 'Não',
            '(Veja Ex02.paragraphs_hastext)'
        )
    )

    table.item(
        'Crie um texto corrido a partir dos parágrafos lidos',
        ex.paragraphs_text
    )

    table.item(
        'Substitua o termo "Batista" por "João Batista"',
        ex.paragraphs_replacetext('Batista', 'João Batista')
    )

    table.print()


def booklet1ex01() -> None:
    ex = booklet1.Ex01()

    table = DSExercise('Apostila 1 - Exercitando 01')

    table.item(
        'Imprima as palavras dos documentos neg/cv002_tok-3321.txt e '
        'pos/cv003_tok-8338.txt',

        'cv002_tok-3321.txt\n',
        ', '.join(list(ex.words('cv002_tok-3321'))[0:50]),

        '\n\ncv003_tok-8338.txt\n',
        ', '.join(list(ex.words('cv003_tok-8338'))[0:50]),
    )

    table.print()


def booklet1ex02() -> None:
    table = DSExercise('Apostila 1 - Exercitando 02')
    ex = booklet1.Ex02('Noticia_1.docx')

    table.item(
        'Utilize o arquivo Noticia_1 disponível na pasta de dados da turma  e '
        'liste os 20 bigramas e trigramas mais frequentes obtidos do texto',
        table.columns(
            table.text('bigramas\n', justify='center'),
            table.text('trigramas\n', justify='center'),
        ),
        table.columns(
            table.text('\n', justify='right').join([
                table.text(f'{a}: {b:2}') for a, b in ex.top_bigrams()
            ]),
            table.text('\n', justify='right').join([
                table.text(f'{a}: {b:2}') for a, b in ex.top_trigrams()
            ])
        )
    )

    table.print()


def booklet1ex03() -> None:
    exs = booklet1.Ex03('singles.txt')
    exp = booklet1.Ex03('pirates.txt')
    table = DSExercise('Apostila 1 - Exercitando 03')

    exs.tokens_freq_plot()
    exp.tokens_freq_plot()

    table.item(
        'Analise a frequência das palavras ["the", "that"] no arquivo '
        '"singles.txt" e,depois, no arquivo "pirates.txt"',

        table.columns(
            table.columns(
                table.text('singles.txt', justify='center'),
                'the: {:4}'.format(exs.words_freq['the']),
                'that: {:4}'.format(exs.words_freq['that']),
            ),
            table.columns(
                table.text('pirates.txt', justify='center'),
                'the: {:4}'.format(exp.words_freq['the']),
                'that: {:4}'.format(exp.words_freq['that']),
            )

        ),
    )

    table.item(
        'Inclua a geração do gráfico de frequência',
        table.columns(
            table.text('singles.txt', justify='center'),
            '... {}'.format(exs.tokens_freq_plot()[-37:])
        ),
        table.columns(
            table.text('pirates.txt', justify='center'),
            '... {}'.format(exp.tokens_freq_plot()[-37:])
        )
    )

    table.item(
        'Gere a lista dos 15 bigramas mais frequentes do texto',

        table.columns(
            table.text('singles.txt\n', justify='center'),
            table.text('pirates.txt\n', justify='center'),
        ),

        table.columns(
            table.text('\n', justify='right').join([
                table.text(f'{a}: {b:2}') for a, b in exs.top_bigrams
            ]),
            table.text('\n', justify='right').join([
                table.text(f'{a}: {b:2}') for a, b in exp.top_bigrams
            ])
        )
    )

    table.item(
        'Gere a lista dos 20 quadrigramas gramas mais frequentes que possuam a '
        'palavra "life"',

        table.text('singles.txt\n', justify='center'),
        table.text('\n', justify='right').join([
            table.text(f'{a}: {b:2}') for a, b in exs.top_life_quadrigrams
        ]),

        table.text('\n\npirates.txt\n', justify='center'),
        table.text('\n', justify='right').join([
            table.text(f'{a}: {b:2}') for a, b in exp.top_life_quadrigrams
        ])
    )

    table.print()


def booklet1ex04() -> None:
    table = DSExercise('Apostila 1 - Exercitando 03')

    table.item(
        '',
        booklet1.ex04()
    )


if __name__ == '__main__':

    args = get_argparser().parse_args()

    if args.b is None or 'booklet0' in args.b:
        booklet0ex01()
        booklet0ex02()

    if args.b is None or 'booklet1' in args.b:
        booklet1ex01()
        booklet1ex02()
        booklet1ex03()
        # booklet1ex04()

    # apostila2.ex01()
    # apostila2.ex02()
    # apostila2.ex03()
