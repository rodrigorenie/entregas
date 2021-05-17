import os
import inspect

from dataclasses import dataclass


@dataclass(frozen=True)
class DSDataDir:
    path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'data')
    )

    @staticmethod
    def join(*args):
        caller = inspect.getmodule(inspect.currentframe().f_back).__package__
        path = os.path.join(DSDataDir.path, caller)
        for arg in args:
            arg = os.path.basename(arg)
            path = os.path.join(path, arg)
        return path
