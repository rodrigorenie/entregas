import seaborn

from dataclasses import dataclass
from collections.abc import Iterator
from matplotlib import pyplot


class DSPlot:

    @dataclass(frozen=True)
    class Color:
        green1: str = '#004949'
        pink1: str = '#FF6DB6'
        purple1: str = '#490092'
        purple2: str = '#b66dff'
        blue1: str = '#006ddb'
        green2: str = '#009292'
        blue2: str = '#6db6ff'
        red: str = '#920000'
        pink2: str = '#ffb6db'
        brown: str = '#924900'
        orange: str = '#db6d00'
        green3: str = '#24ff24'
        yellow: str = '#ffff6d'
        black: str = '#322E2F'
        blue3: str = '#b6dbff'

        def __iter__(self) -> Iterator[str]:
            for color in self.__dict__.values():
                yield color

    @dataclass(frozen=True)
    class Marker:
        point = '.'
        circle = 'o'
        plus_filled = 'P'
        hexagon2 = 'H'
        star = '*'
        square = 's'
        x_filled = 'X'
        diamond = 'D'
        triangle_down = 'v'

        def __iter__(self) -> Iterator[str]:
            for marker in self.__dict__.values():
                yield marker

    color = Color()
    marker = Marker()

    pyplot_rc = {
        'axes.axisbelow': False,
        'axes.edgecolor': 'lightgrey',
        'axes.facecolor': 'None',
        'axes.grid': False,
        'axes.labelcolor': 'dimgrey',
        # 'axes.spines.right': False,
        # 'axes.spines.top': False,
        'figure.facecolor': 'white',
        'lines.solid_capstyle': 'round',
        'patch.edgecolor': 'w',
        'patch.force_edgecolor': True,
        'text.color': 'dimgrey',
        'xtick.bottom': False,
        'xtick.color': 'dimgrey',
        'xtick.direction': 'out',
        'xtick.top': False,
        'ytick.color': 'dimgrey',
        'ytick.direction': 'out',
        # 'ytick.left': False,
        # 'ytick.right': False
    }

    pyplot.rcParams['axes.prop_cycle'] = pyplot.cycler(color=list(color))
    seaborn.set(rc=pyplot_rc)
    # seaborn.set_context('notebook', rc={'font.size': 12,
    #                                     'axes.titlesize': 20,
    #                                     'axes.labelsize': 12})
