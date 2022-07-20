class Debug:
    def __init__(self):
        self.debug_stack = []

    def __getitem__(self, item):
        self.debug_stack.append(item)

    #gc must be clear
    def clearHelper(self):
        self.debug_stack = []

    def __repr__(self):
        return 'DEBUG RESULTS : {val}'.format(
            val = self.debug_stack
        )