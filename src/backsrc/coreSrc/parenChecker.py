class ParenCounter:
    def __init__(self, ldata=0, rdata=0, depth=0):
        self.ldata = ldata
        self.rdata = rdata
        self.tokens = []
        self.depth = depth