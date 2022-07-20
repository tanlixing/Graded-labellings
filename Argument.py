class Argument:

    def __init__(self, id):
        self.__id = id
        self.setAttacks = set()
        self.setAttackers = set()

    def addAttacks(self, arg):
        self.setAttacks.add(arg)

    def addAttackers(self, arg):
        self.setAttackers.add(arg)


if __name__ == "__main__":
    argument = Argument(1)
    argument.addAttacks(2)
    argument.addAttacks(3)
    b = Argument(2)
    b.addAttacks(4)
    b.addAttacks(5)

    print(b.setAttacks)
    print(len(b.setAttacks))
