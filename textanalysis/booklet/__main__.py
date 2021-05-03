import os

from textanalysis.booklet import booklet0
from textanalysis.booklet import booklet1

from rich import box
from rich.table import Table
from rich.table import Column
from rich.console import Console


def booklet0ex01() -> None:
    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True, box=box.MINIMAL)

    title = Table(show_header=False, width=80, show_lines=True)
    title.add_column("", justify='center')
    title.add_row("Apostila 0 - Exercitando 01")
    console.print(title)

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
    console.print("\n\n\n")


def booklet0ex02() -> None:
    ex = booklet0.Ex02('ROMANCE.docx')

    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True, box=box.MINIMAL)

    title = Table(show_header=False, width=80, show_lines=True)
    title.add_column("", justify='center')
    title.add_row("Apostila 0 - Exercitando 02")
    console.print(title)

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

    act = 'Imprima os parágrafos 3 a 6, inclusive'
    res = '\n\n'.join(ex.paragraphs_segment(3, 6))
    table.add_row('04', act, res)

    act = 'O termo ‘Machado’ está no documento?'
    res = 'Sim' if ex.paragraphs_hastext('Machado') else 'Não'
    res += '\n veja Ex02.paragraphs_hastext'
    table.add_row('05', act, res)

    act = 'Crie um  texto corrido a partir dos parágrafos lidos'
    res = ex.paragraphs_text
    idx = res.index('Batista')
    res = res[idx - 100:idx + 100]
    res = f'...\n{res}\n...\nver método:\nEx02.paragraphs_text'
    table.add_row('06', act, res)

    act = 'Substitua o termo "Batista" por "João Batista"'
    res = ex.paragraphs_replacetext('Batista', 'João Batista')
    idx = res.index('Batista')
    res = res[idx-100:idx+100]
    res = f'...\n{res}\n...\nver método:\nEx02.paragraphs_replacetext'
    table.add_row('07', act, res)

    console.print(table)
    console.print("\n\n\n")


def booklet1ex01() -> None:
    ex = booklet1.Ex01()

    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True, box=box.MINIMAL)

    title = Table(show_header=False, width=80, show_lines=True)
    title.add_column("", justify='center')
    title.add_row("Apostila 1 - Exercitando 01")
    console.print(title)

    table.add_column("", justify='center')
    table.add_column("Atividade")
    table.add_column("Resultado", justify='right', overflow='fold')

    act = 'Imprima as palavras dos documentos neg/cv002_tok-3321.txt e ' \
          'pos/cv003_tok-8338.txt'
    res = 'cv002_tok-3321.txt:\n'
    res += ', '.join(list(ex.words('cv002_tok-3321'))[0:50])
    res += ', ...\n\ncv003_tok-8338.txt:\n'
    res += ', '.join(list(ex.words('cv003_tok-8338'))[0:50])
    res += ', ...\n\n'
    table.add_row('01', act, res)

    console.print(table)
    console.print("\n\n\n")


def booklet1ex02() -> None:
    ex = booklet1.Ex02('Noticia_1.docx')

    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True, box=box.MINIMAL)

    title = Table(show_header=False, width=80, show_lines=True)
    title.add_column("", justify='center')
    title.add_row("Apostila 1 - Exercitando 02")
    console.print(title)

    table.add_column("", justify='center')
    table.add_column("Atividade")
    table.add_column("Resultado", justify='right', overflow='fold')

    act = 'Utilize o arquivo Noticia_1 disponível na pasta de dados da turma ' \
          'e liste os 20 bigramas e trigramas mais frequentes obtidos do texto'
    res = 'bigramas:\n'
    res += '\n'.join(['{}: {:2}'.format(a, b) for a, b in ex.top_bigrams()])
    res += '\n\ntrigramas:\n'
    res += '\n'.join(['{}: {:2}'.format(a, b) for a, b in ex.top_trigrams()])
    table.add_row('01', act, res)

    console.print(table)
    console.print("\n\n\n")


def booklet1ex03() -> None:
    exs = booklet1.Ex03('singles.txt')
    exp = booklet1.Ex03('pirates.txt')

    console = Console(width=80)
    table = Table(show_header=True, width=80, show_lines=True, box=box.MINIMAL)

    title = Table(show_header=False, width=80, show_lines=True)
    title.add_column("", justify='center')
    title.add_row("Apostila 1 - Exercitando 03")
    console.print(title)

    table.add_column("", justify='center')
    table.add_column("Atividade")
    table.add_column("Resultado", justify='right', overflow='fold')

    act = 'Analise a frequência das palavras ["the", "that"] no arquivo ' \
          'singles.txt e,depois, no arquivo pirates.txt'
    res = 'singles.txt\n'
    res += 'the: {:4}\n'.format(exs.word_freq('the'))
    res += 'that: {:4}\n'.format(exs.word_freq('that'))
    res += 'pirates.txt\n'
    res += 'the: {:4}\n'.format(exp.token_freq('the'))
    res += 'that: {:4}\n'.format(exp.token_freq('that'))
    table.add_row('01', act, res)

    act = 'Inclua a geração do gráfico de frequência'
    res = ''
    table.add_row('02', act, res)

    act = 'Gere a lista dos 15 bigramas mais frequentes do texto'
    res = 'singles.txt\n'
    res += '\n'.join([f'{a}: {b}' for a, b in exs.top_bigrams])
    res += '\n\npirates.txt\n'
    res += '\n'.join([f'{a}: {b}' for a, b in exp.top_bigrams])
    table.add_row('03', act, res)

    act = 'Gere a lista dos 20 quadrigramas gramas mais frequentes que ' \
          'possuam a palavra "life"'
    res = 'singles.txt\n'
    res += '\n'.join([f'{a}: {b}' for a, b in exs.top_quadrigrams])
    res += '\n\npirates.txt\n'
    res += '\n'.join([f'{a}: {b}' for a, b in exp.top_quadrigrams])
    table.add_row('04', act, res)

    console.print(table)
    console.print("\n\n\n")


if __name__ == '__main__':
    booklet0ex01()
    booklet0ex02()

    booklet1ex01()
    booklet1ex02()
    booklet1ex03()

    # apostila1.ex01()
    # apostila1.ex02()
    # apostila1.ex03()
    # apostila1.ex04()
    #
    # apostila2.ex01()
    # apostila2.ex02()
    # apostila2.ex03()
