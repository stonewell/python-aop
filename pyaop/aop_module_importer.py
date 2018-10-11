import logging
import imp
import sys

from .module_traverser import ModuleTraverser
from .aspects.aspect_manager import AspectManager


class AopModuleImporter(object):
    def __init__(self):
        super(AopModuleImporter, self).__init__()
        self.module_info_ = None

        self.module_traverser_ = ModuleTraverser(self.func_callback, self.type_callback)
        self.aspect_manager_ = AspectManager()
        self.aspect_manager_.load_aspects()

    def find_module(self, fullname, path=None):
        try:
            parts = fullname.split('.')
            self.module_info_ = imp.find_module(parts[-1], path)
        except:
            return None

        return self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        module = None
        try:
            module = imp.load_module(name, *self.module_info_)
        except:
            logging.exception('load module err:%s', name)

        if module:
            sys.modules[name] = module

            module_hooker = self.aspect_manager_.get_module_hooker(name)

            if module_hooker:
                self.module_traverser_.traverse(module, module_hooker)

        return module

    def func_callback(self, m, name, f, user_data):
        user_data.hook_functin(m, name, f)

    def type_callback(self, m, name, t, user_data):
        user_data.hook_type(m, name, t)
