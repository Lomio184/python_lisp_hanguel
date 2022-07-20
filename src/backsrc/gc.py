from src.bin.ADT import Memory

class Gc(Memory):
    __slots__ = 'gc_stack'

    def __init__(self, gc_stack):
        self.gc_stack = gc_stack

    def check(self):
        for rea in range(len(self.gc_stack)):
            if self.gc_stack[rea] is None or 'display' not in str(self.gc_stack[rea]):
                self.gc_stack.append(self.gc_stack[rea])