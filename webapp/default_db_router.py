# DB router for app1


class DefaultRouter(object):
    """
    A router to control app1 db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on webapp models to 'default'"
        return 'read_db'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'webapp' or obj2._meta.app_label == 'webapp':
            return True
        return None