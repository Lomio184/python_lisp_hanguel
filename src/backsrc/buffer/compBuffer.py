class CompilerBufferedIO:
    _bufferd_Priority = 0
    def __init__(self):
        self.buffered_io = []

    def _inBuffer(self, standardIo):
        return self.buffered_io.append(standardIo)