import logging
import imp
import sys


class AopModuleImporter(object):
    def __init__(self):
        super(AopModuleImporter, self).__init__()
        self.fullname = None
        self.path = None

    def find_module(self, fullname, path=None):
        try:
            parts = fullname.split('.')
            self.module_info = imp.find_module(parts[-1], path)
        except:
            return None

        return self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        module = None
        try:
            module = imp.load_module(name, *self.module_info)
        except:
            logging.exception('err')

        if module:
            sys.modules[name] = module

        return module
