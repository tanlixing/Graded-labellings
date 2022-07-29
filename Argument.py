class Argument:
    # Labels
    (OUT, IN, UNDEC, BLANK) = ('0', '1', '3', '9')

    def __init__(self, id):
        self.__id = id
        self.Attacks = set()
        self.Attackers = set()
        self.INAttackers = set()
        self.UNDECAttackers = set()

    def addAttacks(self, arg):
        self.Attacks.add(arg)

    def addAttackers(self, arg):
        self.Attackers.add(arg)

    def addINAttackers(self, arg):
        self.INAttackers.add(arg)

    def addUNDECAttackers(self, arg):
        self.UNDECAttackers.add(arg)

    def removeINAttackers(self, arg):
        self.INAttackers.remove(arg)

    def removeUNDECAttackers(self, arg):
        self.UNDECAttackers.remove(arg)

    def getNeighbornum(self):
        return len(self.Attackers) + len(self.Attacks)


if __name__ == "__main__":
    a = Argument(1)
    a.addAttacks(2)
    a.addAttacks(3)
    a.addAttackers(4)
    a.addAttackers(5)

    print(a.getNeighbornum())
    print(a.Attackers)
