import logging
import functools

from typing import Optional, Callable


class DSLog:
    """Classe auxiliar para interface com módulo :mod:`logging` do Python.

    Esta classe configura o módulo :mod:`logging` do Python definido um nível
    de log customizado para que as mensagens não conflitem com os logs do
    sistema ou de outros módulos.

    Além disso, são definidos métodos para facilitar e padronizar a geração de
    logs.

    :cvar DSINFO: Nível de log customizado
    """

    DSINFO: int = 45

    logging.addLevelName(DSINFO, "INFO")
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s.%(msecs)03d [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        # filename='dados/debug.log',
        # filemode='w'
    )

    @staticmethod
    def log(msg: str, level: Optional[int] = DSINFO) -> None:
        """Gera uma mensagem de log.

        Gera uma mensagem de log cujo nível padrão é ``DSINFO``.
        """
        logging.log(level=level, msg=msg)

    @staticmethod
    def logged(func: Optional[Callable] = None, *,
               msg: Optional[str] = None, level: Optional[int] = DSINFO):
        """Decorador para gerar mensagens de log automaticamente.

        Este método tem como objetivo ser utilizado como decorador de funções ou
        outros métodos, gerando uma mensagem de log com o nome da função ou
        método decorado quando este é executado.

        Exemplo:

        >>> import dsutils
        >>>
        >>> @dsutils.DSLog.logged
        >>> def teste():
        >>>     return 1
        >>>
        >>> teste() # Gera um log informando que teste está em execução
        """
        if func is None:
            return functools.partial(DSLog.logged, msg=msg, level=level)

        name = func.__qualname__
        msg = f'{name}: {msg}' if msg is not None else '{name}: em execução'

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.log(level=level, msg=msg.format(name=name))
            return func(*args, **kwargs)

        return wrapper
