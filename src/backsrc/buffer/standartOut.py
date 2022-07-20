from src.backsrc.buffer.InterBuffer import InterPreterOptionBufferdIo
from src.backsrc.buffer.compBuffer import CompilerBufferedIO
import sys


class Print(CompilerBufferedIO,InterPreterOptionBufferdIo):
    def __init__(self, args):
        self.args = None if args == None else args

    def standardOut(self):
        sentence = ''
        for _ in self.args:
            sentence += str(_)
        sys.stdout.write(sentence)
        self.flushing()
        sys.stdout.write("\n")
        self.flushing()
        return

    def flushing(self):
        sys.stdout.flush()