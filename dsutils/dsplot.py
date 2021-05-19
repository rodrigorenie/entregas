import seaborn

from dataclasses import dataclass
from collections.abc import Iterator
from matplotlib import pyplot


class DSPlot:

    @dataclass(frozen=True)
    class Color:
        yellow: str = '#ddb310'
        darkgreen: str = '#005900'
        lipstick: str = '#b80058'
        azure: str = '#008cf9'
        darkgray: str = '#585858'
        green: str = '#006e00'
        lavender: str = '#d163e6'
        brown: str = '#b24502'
        coral: str = '#ff9287'
        darkblue: str = '#000078'
        indigo: str = '#5954d6'
        turquoise: str = '#00c6f8'
        olive: str = '#878500'
        jade: str = '#00a76c'
        gray: str = '#bdbdbd'
        darkpink: str = '#8a034f'

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
