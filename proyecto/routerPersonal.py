class RouterPersonal(object):
    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'personal':
            return 'personal'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'personal':
            return 'personal'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'personal' or obj2._meta.app_label == 'personal':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'personal':
            return model._meta.app_label == 'personal'
        elif model._meta.app_label == 'personal':
            return False
        return None
