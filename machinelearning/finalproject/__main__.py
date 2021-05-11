import pandas as pd
import rich.rule

from machinelearning.finalproject import Diabetes
from dsutils import DataDir

from rich import box
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.console import Console, RenderGroup
from rich.rule import Rule

class Atividade:

    def __init__(self, titulo):
        self.titulo = titulo
        self.itens = {}

    def __iter__(self):
        for num, (item, res) in enumerate(self.itens.items()):
            yield f'{num+1:02}', item, res

    def item(self, item, *resposta):
        self.itens[item] = resposta

    def print(self):
        console = Console(width=80)
        console.print(Panel(Text(self.titulo, justify='center')))

        for num, item, resposta in self:
            console.print(Columns([
                Panel(num, width=6, box=box.SIMPLE),
                Panel(item, width=73, box=box.SIMPLE)
            ]))
            console.print(*resposta, sep='\n\n')
            console.print(Rule(characters='-'))



def ex1():
    diabetes = Diabetes()

    # group1 = pd.read_csv(DataDir.join('instances_positive.csv'))
    # group2 = pd.read_csv(DataDir.join('instances_negative.csv'))
    #
    # print(diabetes.predict(group1))
    # print(diabetes.predict(group2))
    #
    # for model, score in diabetes.accuracy():
    #     print(model, score)

    atividade = Atividade('Construa um sistema que permita indicar risco de '
                          'diabetes em pacientes. Utilize o arquivo '
                          '"diabetes.csv"')
    atividade.item(
        'Todas as etapas da preparação dos dados devem ser consideradas '
        '(normalizar e balancear)',
        Text('NORMALIZADOS', justify='center'),
        diabetes.df.rocket.normalized,
        Text('BALANCEADOS', justify='center'),
        diabetes.df.rocket.normalized.balanced
    )

    atividade.item(
        'Teste diferentes indutores e selecione o melhor',

        ''
    )

    atividade.item(
        'Deve-se criar um programa que receba uma nova instancia e a '
        'classifique (pode ser selecionada entre os dados originais)',

        ''
    )

    atividade.item(
        'O retorno do módulo de inferência deve apresentar a classe indicada e '
        'a distribuição probabilística das classes (predict_proba)',

        ''
    )

    atividade.item(
        'Ao final, entregue uma pasta com todos os programas desenvolvidos',

        ''
    )

    atividade.print()


if __name__ == '__main__':
    ex1()
    raise SystemExit





