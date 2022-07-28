from scipy import sparse
import numpy as np
from Argument import Argument


class GroundedSemantics:
    # 常量定义区域
    (OUT, IN, UNDEC) = ('0', '1', '3')
    setGrExt = []

    def __init__(self, argNum: int, data: sparse.csr_matrix, m: int, n: int):
        self.m = m
        self.n = n
        self.data = data
        self.argNum = argNum
        self.argList = [Argument(i) for i in range(argNum)]
        self.labellings = [GroundedSemantics.UNDEC for i in range(argNum)]
        self.undecList = []

    def initIn(self):
        for i in range(self.argNum):
            if len(self.argList[i].Attackers) < self.m:
                self.labellings[i] = GroundedSemantics.IN
                for item in self.argList[i].Attacks:
                    self.argList[item].addINAttackers(i)

    def initArgList(self):
        for i in range(self.argNum):
            for j in range(self.argNum):
                if self.data[i, j] != 0:
                    self.argList[i].addAttacks(j)
                    self.argList[j].addAttackers(i)
        self.initIn()
        for i in range(self.argNum):
            if len(self.argList[i].INAttackers) >= self.n:
                self.labellings[i] = GroundedSemantics.OUT
            else:
                self.undecList.append(i)

    def checkValidAttackerNum(self, index: int):
        count = 0
        for i in self.argList[index].Attackers:
            if self.labellings[i] != GroundedSemantics.OUT:
                count += 1
        return count

    def inLab(self, labellings: list):
        E = set()
        for i in range(self.argNum):
            if labellings[i] == GroundedSemantics.IN:
                E.add(i)
        return E

    def updateOUT(self, labellings: list):
        for i in range(self.argNum):
            count = 0
            for j in self.argList[i].Attackers:
                if labellings[j] == GroundedSemantics.IN:
                    count += 1
                    if count == self.n and\
                       labellings[i] == GroundedSemantics.UNDEC:
                        labellings[i] = GroundedSemantics.OUT
                        break

    def SelectArg(self, labellings: list):
        for item in self.undecList:
            if labellings[
                    item] == GroundedSemantics.UNDEC and self.checkValidAttackerNum(
                        item) < self.m:
                return item
        return -1

    def ComputGr(self):
        self.initArgList()
        # self.undecList.sort(key=lambda x: self.argList[x].getNeighbornum(),reverse=True)
        if 0 == len(self.undecList):
            print(self.inLab(self.labellings))
            return
        index = self.SelectArg(self.labellings)
        while -1 != index:
            self.labellings[index] = GroundedSemantics.IN
            self.updateOUT(self.labellings)
            index = self.SelectArg(self.labellings)
        print(self.inLab(self.labellings))


if __name__ == "__main__":
    '''
    Matrix = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    gr = GroundedSemantics(6, myMatrix, 2, 2)
    gr.ComputGr()
    '''

    Matrix = np.array([[1, 1, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    gr = GroundedSemantics(4, myMatrix, 2, 2)
    gr.ComputGr()
