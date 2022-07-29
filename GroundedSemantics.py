import string
from scipy import sparse
import numpy as np
from Argument import Argument


class GroundedSemantics:

    def __init__(self, argNum: int, data: sparse.csr_matrix, m: int, n: int):
        self.m = m
        self.n = n
        self.data = data
        self.argNum = argNum
        self.argList = [Argument(i) for i in range(argNum)]
        self.labellings = [Argument.UNDEC for i in range(argNum)]
        self.undecList = []

    def addEffAttacker(self, x: int, label: string):
        for item in self.argList[x].Attacks:
            if label == Argument.IN:
                self.argList[item].addINAttackers(x)
            elif label == Argument.UNDEC:
                self.argList[item].addUNDECAttackers(x)

    def removeEffAttacker(self, x: int, label: string):
        for item in self.argList[x].Attacks:
            if label == Argument.IN:
                self.argList[item].removeINAttackers(x)
            elif label == Argument.UNDEC:
                self.argList[item].removeUNDECAttackers(x)

    def initIn(self):
        for i in range(self.argNum):
            if len(self.argList[i].Attackers) < self.m:
                self.labellings[i] = Argument.IN
                self.addEffAttacker(i, Argument.IN)

    def initArgList(self):
        for i in range(self.argNum):
            for j in range(self.argNum):
                if self.data[i, j] != 0:
                    self.argList[i].addAttacks(j)
                    self.argList[j].addAttackers(i)
        self.initIn()
        for i in range(self.argNum):
            if len(self.argList[i].INAttackers) >= self.n:
                self.labellings[i] = Argument.OUT
            else:
                self.addEffAttacker(i, Argument.UNDEC)
                self.undecList.append(i)

    def inLab(self, labellings: list):
        E = set()
        for i in range(self.argNum):
            if labellings[i] == Argument.IN:
                E.add(i)
        return E

    def updateOUT(self, x: int, labellings: list):
        for att in self.argList[x].Attacks:
            if labellings[att] == Argument.OUT:
                continue
            if len(self.argList[att].INAttackers) >= self.n:
                self.removeEffAttacker(att, labellings[att])
                labellings[att] = Argument.OUT

    def SelectArg(self, labellings: list):
        for i in self.undecList:
            if labellings[i] == Argument.UNDEC and\
                 len(self.argList[i].INAttackers) + len(self.argList[i].UNDECAttackers) < self.m:
                return i
        return -1

    def ComputGr(self):
        self.initArgList()
        # self.undecList.sort(key=lambda x: self.argList[x].getNeighbornum(),reverse=True)
        if 0 == len(self.undecList):
            print(self.inLab(self.labellings))
            return
        # print(self.labellings)
        index = self.SelectArg(self.labellings)
        while -1 != index:
            self.labellings[index] = Argument.IN
            self.addEffAttacker(index, Argument.IN)
            self.updateOUT(index, self.labellings)
            index = self.SelectArg(self.labellings)
        # print(self.labellings)
        print(self.inLab(self.labellings))


if __name__ == "__main__":
    '''
    Matrix1 = np.array([[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 0, 1, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix1)
    argNum = 5
    m = n = 1
    '''
    '''
    Matrix2 = np.array([[1, 1, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix2)
    argNum = 4
    m = n = 2
    '''
    Matrix3 = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                        [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                        [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix3)
    argNum = 6
    m = n = 2
    gr = GroundedSemantics(argNum, myMatrix, m, n)
    gr.ComputGr()
