import dsutils


@dsutils.logged
@dsutils.timed
def teste():
    return 1


if __name__ == '__main__':
    teste()
    print(dir(dsutils.DSPlot.color))
    for color in dsutils.DSPlot.color:
        print(color)

