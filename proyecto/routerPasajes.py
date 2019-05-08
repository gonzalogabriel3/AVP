class RouterPasajes(object):
    def db_for_read(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'pasajes':
            return 'pasajes'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on myapp models to 'other'"
        if model._meta.app_label == 'pasajes':
            return 'pasajes'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in myapp is involved"
        if obj1._meta.app_label == 'pasajes' or obj2._meta.app_label == 'pasajes':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the myapp app only appears on the 'other' db"
        if db == 'pasajes':
            return model._meta.app_label == 'pasajes'
        elif model._meta.app_label == 'pasajes':
            return False
        return None
