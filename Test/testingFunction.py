class Rea:
    def __init__(self):
        self.rea = 0

    def __add__(self, other):
            self.rea += other

if __name__ == "__main__":
    rea = Rea()
    reb = Rea()
    reb + 1
    rea + 2
    print(rea.rea)
    rea + 1
    rea + reb
    print(rea.rea)