import pandas
import dsutils


@dsutils.logged
@dsutils.timed
def pandas_test():
    df = pandas.read_csv(dsutils.datadir.join('hypo.csv'), na_values=['?'])

    print(df.hypo.numericals.hypo.instances)
    print(df.hypo.categoricals.hypo.instances)

    print(df.hypo.numericals)
    print(df.hypo.categoricals)
    print(df.hypo.classes)

    nona = df.hypo.nona
    print(nona)

    norm = df.hypo.nona.hypo.normalized
    print(norm)

    bal = df.hypo.nona.hypo.normalized.hypo.balanced
    print(bal)

    red = df.hypo.nona.hypo.normalized.hypo.balanced.hypo.reduced
    print(red)

    train, test = df.hypo.nona.hypo.normalized.hypo.balanced.hypo.split()
    print(train)
    print(test)


if __name__ == '__main__':
    pandas_test()
