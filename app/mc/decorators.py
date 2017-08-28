
import inspect
from functools import wraps


MC_DEFAULT_EXPIRE = 0


def gen_key_factory(prefix, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}

    def gen_key(func=None, *a, **kws):
        if not callable(func):
            raise TypeError('func must me a callable object')
        name = func.__name__
        func_prefix = ':'.join([prefix, name])
        a_num = len(a)
        args.update(zip(arg_names[:a_num], a))
        args.update(kws)
        for _ in arg_names:
            func_prefix = ''.join([func_prefix, ':{', _, '}'])
        print(func_prefix)

        key = func_prefix.format(**args)
        return key

    return gen_key


def cache(prefix, mc, expire=MC_DEFAULT_EXPIRE, max_retry=0):
    def deco(f):
        args, varargs, varkws, defaults = inspect.getargspec(f)
        if varargs and varkws:
            raise Exception('do not support args and kws')
        gen_key = gen_key_factory(prefix, args, defaults)

        @wraps(f)
        def deco_func(*args, **kws):
            key = gen_key(f, *a, **kws)
