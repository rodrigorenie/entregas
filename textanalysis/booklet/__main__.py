import os

from atividade_apostila import apostila0, apostila1, apostila2
from rich.table import Table
from rich.console import Console


def apostila01(table: Table) -> None:
    ex = apostila0.Ex01(
        'Ainda que falasse as línguas dos homens e falasse a língua dos anjos, '
        'sem amor eu nada seria.'
    )

    table.add_row(
        '00', '01',
        'Crie uma string com o conteúdo "Ainda que falasse as línguas dos homens e falasse a  língua dos  anjos, sem '
        'amor eu nada seria."',
        str(ex)
    )

    table.add_row(
        '00', '01',
        'Imprima cada caractere da string',
        ' '.join([c for c in ex.text_chars])
    )

    table.add_row(
        '00', '01',
        'Segmente a string em uma lista',
        str(list(ex.text_split))
    )

    table.add_row(
        '00', '01',
        'Quantas palavras há na lista?',
        str(ex.text_split_len)
    )

    table.add_row(
        '00', '01',
        'Imprima cada palavra da string',
        ' | '.join(list(ex.text_split))
    )

    table.add_row(
        '00', '01',
        'Substitua o termo "dos homens" por "do mundo"',
        ex.text_replace('dos homens', 'do mundo')
    )

    table.add_row(
        '00', '01',
        'Imprima o fragmento que vai do 21º até o 30º caracteres',
        '"{}"'.format(ex.text_segment(21, 30))
    )

    table.add_row(
        '00', '01',
        'Imprima os últimos 15 caracteres',
        '"{}"'.format(ex.text_last(15))
    )

    table.add_row(
        '00', '01',
        'Salve a sentença em um arquivo do tipo txt',
        'Arquivo salvo em:\n{}'.format(
            ex.text_save(os.path.dirname(__file__) + '/../dados/apostila01_ex01.txt')
        )
    )

    ex = apostila0.Exercitando02(os.path.dirname(__file__) + '/../dados/ROMANCE.docx')

    table.add_row(
        '00', '02',
        'Crie uma lista com os parágrafos do documento',
        'ex.paragraphs_list: tipo {}'.format(type(ex.paragraphs_list))
    )

    table.add_row(
        '00', '02',
        'Quantos parágrafos o documento possui?',
        str(ex.paragraphs_len)
    )

    table.add_row(
        '00', '02',
        'Imprima o conteúdo do 1º parágrafo  do texto',
        str(ex.paragraphs_segment(1))
    )

    table.add_row(
        '00', '02',
        'Imprima os parágrafos 3 a 6, inclusive',
        '\n\n'.join(ex.paragraphs_segment(3, 6))
    )

    table.add_row(
        '00', '02',
        'O termo ‘Machado’ está no documento?',
        'Sim' if ex.paragraphs_hastext('Machado') else 'Não'
    )

    table.add_row(
        '00', '02',
        'Crie um  texto corrido a partir dos parágrafos lidos',
        ex.paragraphs_text
    )

    table.add_row(
        '00', '02',
        'Substitua o termo "Batista" por "João Batista"',
        ex.paragraphs_replacetext('Batista', 'João Batista')
    )


if __name__ == '__main__':
    console = Console(width=120)

    t = Table(show_header=True, width=120, show_lines=True)
    t.add_column("Apostila", justify='center', width=10)
    t.add_column("Exercício", justify='center', width=10)
    t.add_column("Item", width=30)
    t.add_column("Resultado", overflow='fold')

    apostila01(t)
    console.print(t)

    apostila1.ex01()
    apostila1.ex02()
    apostila1.ex03()
    apostila1.ex04()

    apostila2.ex01()
    apostila2.ex02()
    apostila2.ex03()
