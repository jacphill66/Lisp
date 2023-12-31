class Environment:
    def __init__(self, outer=None, bindings=None, exprs=None):
        self.data = {}
        self.macros = []
        self.files = {}
        self.outer = outer

        if bindings:
            count = 0
            for bind in bindings:
                # exprs[count].accept(self)
                self.set(bind, exprs[count])
                count += 1

    def set(self, key, val):
        self.data[key] = val
        return val

    def set_global(self, key, val):
        if self.outer:
            return self.set_global(key, val)
        else:
            self.data[key] = val

    def find(self, key):
        if key in self.data:
            return self
        elif self.outer:
            return self.outer.find(key)
        return None

    def contains(self, key):
        if key in self.data:
            return True
        elif self.outer:
            return self.outer.find(key)
        return False

    def get(self, key):
        env = self.find(str(key))
        if env:
            return env.data[str(key)]
        raise Exception("'" + str(key) + "' " "not found.")

    def __repr__(self):
        if self.outer:
            return f'({self.outer.__repr__()} ({self.data}))'
        else:
            # return f'global scope {self.data}' # str(self.data)
            return f'global scope' # str(self.data)