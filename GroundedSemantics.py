import copy
from Argument import *
from scipy import sparse
import numpy as np


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

    def initIn(self):
        for i in range(self.argNum):
            if len(self.argList[i].setAttackers) < self.m:
                self.labellings[i] = GroundedSemantics.IN

    def initArgList(self):
        undecNum = 0
        for i in range(self.argNum):
            for j in range(self.argNum):
                if self.data[i, j] != 0:
                    self.argList[i].addAttacks(j)
                    self.argList[j].addAttackers(i)
        self.initIn()
        for i in range(self.argNum):
            if self.labellings[i] == GroundedSemantics.IN:
                continue
            count = 0
            for j in self.argList[i].setAttackers:
                if self.labellings[j] == GroundedSemantics.IN:
                    count += 1
                    if count == self.n:
                        break
            if count == self.n:
                self.labellings[i] = GroundedSemantics.OUT
            else:
                undecNum = undecNum + 1
        print(self.labellings)
        print(undecNum)
        return undecNum

    def checkValidAttackerNum(self, index: int):
        count = 0
        for i in self.argList[index].setAttackers:
            if self.labellings[i] != GroundedSemantics.OUT:
                count += 1
        return count

    def IsContinue(self, s: int):
        if s == 0:
            return False
        for i in range(self.argNum):
            if self.labellings[i] == GroundedSemantics.UNDEC and \
               self.checkValidAttackerNum(i) >= self.m:
                return False
        return True

    def inLab(self, labellings: list):
        E = set()
        for i in range(self.argNum):
            if labellings[i] == GroundedSemantics.IN:
                E.add(i)
        return E

    def updateOUT(self, labellings: list, undecNum: int):
        for i in range(self.argNum):
            count = 0
            for j in self.argList[i].setAttackers:
                if labellings[j] == GroundedSemantics.IN:
                    count += 1
                    if count == self.n and\
                       labellings[i] == GroundedSemantics.UNDEC:
                        labellings[i] = GroundedSemantics.OUT
                        undecNum = undecNum - 1
                        break
        return undecNum

    def ComputGr(self):
        undecNum = self.initArgList()
        while self.IsContinue(undecNum):
            for i in range(self.argNum):
                if self.labellings[i] == GroundedSemantics.UNDEC and \
                   self.checkValidAttackerNum(i) < self.m:
                    self.labellings[i] = GroundedSemantics.IN
                    undecNum = undecNum - 1
                    undecNum = self.updateOUT(self.labellings, undecNum)
        GroundedSemantics.setGrExt.append(self.inLab(self.labellings))
        print(GroundedSemantics.setGrExt)


if __name__ == "__main__":
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
    '''
