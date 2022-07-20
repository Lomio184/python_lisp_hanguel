class Python:
    pass

class Evalutate(Python):
    def __init__(self, bootStrap = None):
        super(Python, self).__init__()
        self.bootstrap = bootStrap

    def Eval(self):
        return 2 + 2

ev = Evalutate(1)
import runpy

runpy._run_code("2+2", run_globals="test.py")