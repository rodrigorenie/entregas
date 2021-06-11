from rich import box
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.rule import Rule


class DSExercise:

    def __init__(self, title):
        self._title = title
        self._items = {}

    @staticmethod
    def text(*args, **kwargs):
        return Text(*args, **kwargs)

    @staticmethod
    def columns(*args, **kwargs):
        return Columns(renderables=args, expand=True, **kwargs)

    def __iter__(self):
        for number, (item, resolution) in enumerate(self._items.items()):
            yield f'{number+1:02}', item, resolution

    def item(self, item, *resolutions):
        self._items[item] = resolutions

    def print(self):
        console = Console(width=80)
        console.print(Panel(Text(self._title, justify='center')))

        for number, item, resolutions in self:
            console.print(Columns([
                Panel(number, width=6, box=box.SIMPLE),
                Panel(item, width=73, box=box.SIMPLE)
            ]))
            console.print(*resolutions, sep='\n')
            console.print()
            console.print(Rule(characters='-'))
