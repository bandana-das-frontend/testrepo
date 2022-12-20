from django.core.cache import cache
from hashlib import md5


def get_local(key):
    if key in cache:
        return cache.get(key)
    return None


def set_local(key, val):
    cache.set(key, val)
    return


def set_local_with_timeout(key, val, timeout):
    cache.set(key, val, timeout)
    return


def delete_local(key):
    cache.delete(key)
    return


class CacheIt(object):
    def __init__(self, *dec_args, **dec_kw):
        self.dec_args = dec_args
        self.dec_kw = dec_kw

    def _showargs(self, *fargs, **kw):
        pass

    def _showinstance(self, instance):
        pass

    def __call__(self, f):
        def wrapper(*fargs, **kw):
            if len(self.dec_args) == 0:
                key = f.__name__ + str(fargs) + str(tuple(sorted(kw.items())))
                key = md5(key).hexdigest()
            else:
                key = f.__name__

                for dec_arg in self.dec_args:
                    key += ',' + str(kw.get(dec_arg))

                key = md5(key).hexdigest()

                # Evict cache if the page is provided and page number is 1
                if kw.get("page") and kw.get("page").isdigit() and int(kw.get("page")) == 1:
                    delete_local(key)

            ret = get_local(key)

            if not ret:
                ret = f(*fargs, **kw)
                # If page is present in the def argument then cache it to infinite.
                # This will make sure there is no auto cache eviction.
                if kw.get("page"):
                    set_local_with_timeout(key, ret, None)
                else:
                    set_local(key, ret)

            return ret

        # Save wrapped function reference
        self.f = f
        wrapper.__name__ = f.__name__
        wrapper.__dict__.update(f.__dict__)
        wrapper.__doc__ = f.__doc__
        return wrapper