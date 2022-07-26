class Argument:

    def __init__(self, id):
        self.__id = id
        self.setAttacks = set()
        self.setAttackers = set()

    def addAttacks(self, arg):
        self.setAttacks.add(arg)

    def addAttackers(self, arg):
        self.setAttackers.add(arg)

    def getNeighbornum(self):
        return len(self.setAttackers) + len(self.setAttacks)


if __name__ == "__main__":
    a = Argument(1)
    a.addAttacks(2)
    a.addAttacks(3)
    a.addAttackers(4)
    a.addAttackers(5)

    print(a.getNeighbornum())
