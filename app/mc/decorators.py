
import inspect
from functools import wraps
import time


MC_DEFAULT_EXPIRE = 2


def gen_key_factory(prefix, arg_names, defaults):
    '''
    params:
        prefix:key的前缀。建议为蓝图名，类名
        ars_names:[], 被装饰函数的位置参数，关键字参数的名字
        defaults: 关键字参数的默认值
    '''

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

        key = func_prefix.format(**args)
        return key

    return gen_key


def cache(prefix, mc, expire=MC_DEFAULT_EXPIRE, max_retry=0):
    '''
    mc: libmc instance
    expire: expire time, unit is seconds
    '''

    def deco(f):
        args, varargs, varkws, defaults = inspect.getargspec(f)
        if varargs and varkws:
            raise Exception('do not support args and kws')
        gen_key = gen_key_factory(prefix, args, defaults)

        @wraps(f)
        def deco_func(*a, **kws):
            key = gen_key(f, *a, **kws)
            r = mc.get(key)
            print(type(r))
            print(key)
            retry = max_retry
            while r is None and retry > 0:
                print('mc invalid')
                if mc.add(key + '#mutex', 1, int(max_retry * 0.1)):
                    print('add mutex')
                    break

                time.sleep(1)
                r = mc.get(key)
                retry -= 1

            if r is None:
                r = f(*a, **kws)
                if r is not None:
                    mc.set(key, r, expire)
                if retry > 0:
                    mc.delete(key + '#mutex')
            return r

        return deco_func
    return deco


def create_cache(mc):
    def _cache(prefix, mc=mc, expire=MC_DEFAULT_EXPIRE, max_retry=5):
        return cache(prefix, mc=mc, expire=expire, max_retry=max_retry)
    return {'cache': _cache}
