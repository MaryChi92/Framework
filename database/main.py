from threading import local
from sqlite3 import Connection


class Session:
    current = local()

    def __init__(self):
        self.created_objects = []
        self.updated_objects = []
        self.deleted_objects = []

    def register_mappers(self, registry):
        self.registry = registry.get_registry()

    def get_mapper(self, model):
        return self.registry[model.mapper](self.connection)

    def add_created(self, object):
        self.created_objects.append(object)

    def add_updated(self, object):
        self.updated_objects.append(object)

    def add_deleted(self, object):
        self.deleted_objects.append(object)

    def commit(self):
        self.insert()
        self.update()
        self.delete()

        self.created_objects.clear()
        self.updated_objects.clear()
        self.deleted_objects.clear()

    def insert(self):
        for object in self.created_objects:
            self.registry[object.mapper](self.connection).insert(object)

    def update(self):
        for object in self.updated_objects:
            self.registry[object.mapper](self.connection).update(object)

    def delete(self):
        for object in self.deleted_objects:
            self.registry[object.mapper](self.connection).delete(object)

    @classmethod
    def new_current(cls):
        cls.current.session = Session()
        cls.current.session.connection = Connection("db.sqlite3")

    @classmethod
    def get_current(cls):
        return cls.current.session


class Objects:
    def create(self):
        Session.get_current().add_created(self)

    def update(self):
        Session.get_current().add_updated(self)

    def delete(self):
        Session.get_current().add_deleted(self)
