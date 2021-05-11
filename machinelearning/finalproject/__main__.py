import pandas

from machinelearning.finalproject import Diabetes, Hypothyroid
from dsutils import Exercise, DataDir


def ex1():
    diabetes = Diabetes()

    ex = Exercise('Construa um sistema que permita indicar risco de diabetes '
                  'em pacientes. Utilize o arquivo "diabetes.csv"')
    ex.item(
        'Todas as etapas da preparação dos dados devem ser consideradas '
        '(normalizar e balancear)',
        ex.text('Normalizados (primeiros itens)', justify='center'),
        diabetes.df.rocket.normalized.df.head(),
        ex.text('Balanceados (primeiros itens)', justify='center'),
        diabetes.df.rocket.normalized.balanced.df.head()
    )

    resultado = []
    for modelo, acuracia in diabetes.accuracy():
        text = ex.text(f'{str(modelo):>30s}: {acuracia:1.3f}')
        resultado.append(text)

    ex.item(
        'Teste diferentes indutores e selecione o melhor',
        *resultado
    )

    resultado = [
        ex.text("Instâncias de Teste 1 (todos verdadeiramente positivos)",
                justify='center'),
        diabetes.predict(
            pandas.read_csv(DataDir.join('instances_positive.csv'))
        ),

        ex.text("Instâncias de Teste 2 (todos verdadeiramente negativos)",
                justify='center'),
        diabetes.predict(
            pandas.read_csv(DataDir.join('instances_negative.csv'))
        )
    ]
    ex.item(
        'Deve-se criar um programa que receba uma nova instancia e a '
        'classifique (pode ser selecionada entre os dados originais)',
        *resultado
    )

    ex.item(
        'O retorno do módulo de inferência deve apresentar a classe indicada e '
        'a distribuição probabilística das classes (predict_proba)',
        'Incluído no resultado do item anterior')

    ex.item(
        'Ao final, entregue uma pasta com todos os programas desenvolvidos',
        ''
    )

    ex.print()


def ex2():
    ex = Exercise('Com o arquivo "hypothyroid.csv", desenvolva um modelo de '
                  'clusters que descreva as características de cada tipo de '
                  'hipotireoidismo')

    ex.item(
        'Todas as etapas da preparação dos dados devem ser consideradas '
        '(normalizar e balancear)',
        ''
    )

    ex.item(
        'Determine o número ideal de clusters antes de obter o modelo'
        ''
    )

    ex.item(
        'Após obter o modelo, liste as características de cada grupo (listar '
        'os valores dos centroides), analise-as e descreva os grupos',
        ''
    )

    ex.item(
        'Sua análise pode ser realizada como comentário do programa ou como '
        'relatório gerencial. Opte pela forma que mais convier à equipe.',
        ''
    )

    ex.print()


if __name__ == '__main__':
    # ex1()
    # ex2()
    Hypothyroid()
