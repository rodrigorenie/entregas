import functools
import time

from dsutils import DSLog
from typing import Optional, Callable


class DSTime:
    """Classe auxiliar para interface com módulo :mod:`time` do Python.
    """

    @staticmethod
    def timed(func: Optional[Callable] = None, *,
              msg: Optional[str] = None,
              level: Optional[int] = DSLog.DSINFO):
        """Decorador para cronometrar a execção de código automaticamente.

       Este método tem como objetivo ser utilizado como decorador de funções ou
       outros métodos, cronometrando seu tempo de execução automaticamente. Ao
       final da execução da função ou método decorado, é gerado um log com o seu
       tempo de execução utilizando o método :meth:`DSLogger.log`.

       Exemplo:

       >>> import dsutils
       >>>
       >>> @dsutils.DSTimer.timed
       >>> def teste():
       >>>     return 1
       >>>
       >>> teste() # Gera um log informando o tempo de execução da função
       """
        if func is None:
            return functools.partial(DSTime.timed, msg=msg, level=level)

        name = func.__qualname__
        msg = msg if msg is not None else '{name}: execução levou {run_time}'

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            run_time = time.perf_counter()
            value = func(*args, **kwargs)
            run_time = time.perf_counter() - run_time
            run_time = time.strftime('%H:%M:%S', time.gmtime(run_time))
            DSLog.log(msg.format(name=name, run_time=run_time))
            return value

        return wrapper


timed = DSTime.timed
