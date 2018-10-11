class ModuleTraverser(object):
    def __init__(self, func_callback = None, type_callback = None):
        super(ModuleTraverser, self).__init__()

        self.func_callback_ = func_callback
        self.type_callback_ = type_callback

    def traverse(self, module, user_data = None):
        # save a copy incase module changes
        d = dict([(name, cls) for name, cls in module.__dict__.items()])

        for name in d:
            cls = d[name]
            if self.type_callback_ and isinstance(cls, type):
                self.type_callback_(module, name, cls, user_data)
            elif self.func_callback_ and callable(cls):
                self.func_callback_(module, name, cls, user_data)
