import inspect
import pyperclip


class MethodInspector:
    def __init__(self, obj):
        self.obj = obj
        self.methods = dict(inspect.getmembers(obj))

    def _get_source(self, method_name):
        return inspect.getsource(self.methods[method_name])

    def _get_parents(self):
        return type(self.obj).__bases__

    def print_source(self, method_name):
        print(self._get_source(method_name))

    def copy_source(self, method_name):
        pyperclip.copy(self._get_source(method_name))

    def print_parents(self):
        print("\n".join([x.__name__ for x in self._get_parents()]))

    def show_methods(self):
        print("\n".join(self.methods.keys()))
