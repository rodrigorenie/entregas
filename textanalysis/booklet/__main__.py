import os

from textanalysis.booklet import booklet0

from rich.table import Table
from rich.console import Console


def booklet0ex01() -> None:
    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True)

    table.add_column("", justify='center')
    table.add_column("Atividade")
    table.add_column("Resultado", justify='right', overflow='fold')

    ex = booklet0.Ex01(
        'Ainda que falasse as línguas dos homens e falasse a língua dos anjos, '
        'sem amor eu nada seria.'
    )

    act = 'Crie uma string com o conteúdo "Ainda que falasse as línguas dos ' \
          'homens e falasse a  língua dos  anjos, sem amor eu nada seria."'
    res = str(ex)
    table.add_row('01', act, res)

    act = 'Imprima cada caractere da string'
    res = ' '.join([c for c in ex.text_chars])
    table.add_row('02', act, res)

    act = 'Segmente a string em uma lista'
    res = str(list(ex.text_split))
    table.add_row('03', act, res)

    act = 'Quantas palavras há na lista?'
    res = str(ex.text_split_len)
    table.add_row('04', act, res)

    act = 'Imprima cada palavra da string'
    res = ' | '.join(list(ex.text_split))
    table.add_row('05', act, res)

    act = 'Substitua o termo "dos homens" por "do mundo"'
    res = ex.text_replace('dos homens', 'do mundo')
    table.add_row('06', act, res)

    act = 'Imprima o fragmento que vai do 21º até o 30º caracteres'
    res = '"{}"'.format(ex.text_segment(21, 30))
    table.add_row('07', act, res)

    act = 'Imprima os últimos 15 caracteres'
    res = '"{}"'.format(ex.text_last(15))
    table.add_row('08', act, res)

    act = 'Salve a sentença em um arquivo do tipo txt'
    res = 'Arquivo salvo em: {}'.format(ex.text_save('booklet0_ex01.txt'))
    table.add_row('09', act, res)

    console.print(table)


def booklet0ex02() -> None:
    ex = booklet0.Ex02('ROMANCE.docx')

    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True)

    table.add_column("", justify='center')
    table.add_column("Atividade")
    table.add_column("Resultado", justify='right', overflow='fold')

    act = 'Crie uma lista com os parágrafos do documento'
    res = 'Apenas os dois primeiros parágrafos:\n'
    res += str(ex.paragraphs_list[0:2])
    table.add_row('01', act, res)

    act = 'Quantos parágrafos o documento possui?'
    res = str(ex.paragraphs_len)
    table.add_row('02', act, res)

    act = 'Imprima o conteúdo do 1º parágrafo  do texto'
    res = str(ex.paragraphs_segment(1))
    table.add_row('03', act, res)


    # table.add_row(
    #     '00', '02',
    #     'Imprima os parágrafos 3 a 6, inclusive',
    #     '\n\n'.join(ex.paragraphs_segment(3, 6))
    # )
    #
    # table.add_row(
    #     '00', '02',
    #     'O termo ‘Machado’ está no documento?',
    #     'Sim' if ex.paragraphs_hastext('Machado') else 'Não'
    # )
    #
    # table.add_row(
    #     '00', '02',
    #     'Crie um  texto corrido a partir dos parágrafos lidos',
    #     ex.paragraphs_text
    # )
    #
    # table.add_row(
    #     '00', '02',
    #     'Substitua o termo "Batista" por "João Batista"',
    #     ex.paragraphs_replacetext('Batista', 'João Batista')
    # )

    console.print(table)


if __name__ == '__main__':
    booklet0ex02()

    # apostila1.ex01()
    # apostila1.ex02()
    # apostila1.ex03()
    # apostila1.ex04()
    #
    # apostila2.ex01()
    # apostila2.ex02()
    # apostila2.ex03()
