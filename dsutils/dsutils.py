import os
import tempfile
import inspect
import sys

from typing import Optional, Tuple


class DataDir:

    def __init__(self, dirname: Optional[str] = None) -> None:
        if not dirname:
            dirname = inspect.getmodule(self).__package__

        dirname = os.path.join(os.path.dirname(__file__), '..', 'df', dirname)
        dirname = os.path.abspath(dirname)
        self._datadir = dirname

    @property
    def datadir(self) -> str:
        if os.path.exists(self._datadir):
            if not os.path.isdir(self._datadir):
                raise NotADirectoryError
        else:
            os.mkdir(self._datadir)

        return self._datadir

    def datafilename(self, name: Optional[str] = None) -> str:
        if name:
            name = os.path.join(self.datadir, os.path.basename(name))
        else:
            name = os.path.basename(tempfile.NamedTemporaryFile().name)
            name = os.path.join(self.datadir, f'{name}.txt')

        return name

    def datadirname(self, name: Optional[str] = None) -> str:
        if name:
            name = os.path.join(self.datadir, os.path.basename(name))
        else:
            name = os.path.basename(tempfile.TemporaryDirectory().name)
            name = os.path.join(self.datadir, f'{name}')

        return name
