class InterPreterOptionBufferdIo:
    def __init__(self, waitBuffer):
        self.interPreTerBuffer = waitBuffer

    def outOfTerminal(self):
        import sys
        return sys.stdout.write(self.interPreTerBuffer)