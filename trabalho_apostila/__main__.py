import os

from trabalho_apostila import apostila0
from rich.table import Table
from rich.console import Console


def apostila01(table: Table) -> None:
    """Adiciona na tabela passada como parâmetro todos os exercícios e respectivos itens da Apostila 01, assim como o
    resultado de cada um.

    :param table: Instância de :class:`rich.table.Table`
    :rtype: None
    """
    ex = apostila0.Exercitando01()

    table.add_row(
        '00', '01',
        'Crie uma string com o conteúdo "Ainda que falasse as línguas dos homens e falasse a  língua dos  anjos, sem '
        'amor eu nada seria."',
        ex.text
    )

    table.add_row(
        '00', '01',
        'Imprima cada caractere da string',
        ' '.join([c for c in ex.chars()])
    )

    table.add_row(
        '00', '01',
        'Segmente a string em uma lista',
        str(list(ex.words()))
    )

    table.add_row(
        '00', '01',
        'Quantas palavras há na lista?',
        str(ex.words_len())
    )

    table.add_row(
        '00', '01',
        'Imprima cada palavra da string',
        ' | '.join(list(ex.words()))
    )

    table.add_row(
        '00', '01',
        'Substitua o termo "dos homens" por "do mundo"',
        ex.replace()
    )

    table.add_row(
        '00', '01',
        'Imprima o fragmento que vai do 21º até o 30º caracteres',
        '"{}"'.format(ex.segment())
    )

    table.add_row(
        '00', '01',
        'Imprima os últimos 15 caracteres',
        '"{}"'.format(ex.last())
    )

    table.add_row(
        '00', '01',
        'Salve a sentença em um arquivo do tipo txt',
        'Arquivo salvo em:\n{}'.format(
            ex.save(os.path.dirname(__file__) + '/../dados/apostila01_ex01.txt')
        )
    )

    docpath = os.path.dirname(__file__) + '/../dados/ROMANCE.docx'
    ex = apostila0.Exercitando02(docpath)

    table.add_row(
        '00', '02',
        'Crie uma lista com os parágrafos do documento',
        'ex.paragraphs(): tipo {}'.format(type(ex.paragraphs()))
    )

    table.add_row(
        '00', '02',
        'Quantos parágrafos o documento possui?',
        str(ex.paragraphs_len())
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
        'Sim' if ex.text_exists('Machado') else 'Não'
    )

    table.add_row(
        '00', '02',
        'Crie um  texto corrido a partir dos parágrafos lidos',
        ex.paragraphs_text()
    )

    table.add_row(
        '00', '02',
        'Substitua o termo "Batista" por "João Batista"',
        ex.text_replace('Batista', 'João Batista')
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
