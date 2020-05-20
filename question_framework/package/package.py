import os
import inspect

PACKAGES = {}

def registered_class(cls):
    instance = cls()
    PACKAGES[instance.name] = instance
    return cls

def package_names():
    return list(PACKAGES.keys())

def get_package(name):
    return PACKAGES[name]

class Package:

    @property
    def name(self):
        return type(self).__name__

    @property
    def templates(self):
        templates = os.listdir(self.template_dir)
        return templates

    @property
    def package_dir(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    @property
    def template_dir(self):
        return os.path.join(self.package_dir, "templates")