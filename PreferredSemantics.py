import copy
import string
from Argument import *
from scipy import sparse
import numpy as np


class PreferredSemantics:
    # 常量定义区域
    (OUT, IN, UNDEC, BLANK) = ('0', '1', '3', '9')
    setPrExt = []

    def __init__(self, argNum: int, data: sparse.csr_matrix, m: int, n: int):
        self.m = m
        self.n = n
        self.data = data
        self.argNum = argNum
        self.argList = [Argument(i) for i in range(argNum)]
        self.labellings = [PreferredSemantics.BLANK for i in range(argNum)]

    def initIn(self):
        for i in range(self.argNum):
            if len(self.argList[i].setAttackers) < self.m:
                self.labellings[i] = PreferredSemantics.IN

    def initArgList(self):
        blankNum = 0
        for i in range(self.argNum):
            for j in range(self.argNum):
                if self.data[i, j] != 0:
                    self.argList[i].addAttacks(j)
                    self.argList[j].addAttackers(i)
        self.initIn()
        for i in range(self.argNum):
            if self.labellings[i] == PreferredSemantics.IN:
                continue
            count = 0
            for j in self.argList[i].setAttackers:
                if self.labellings[j] == PreferredSemantics.IN:
                    count += 1
                    if count == self.n:
                        break
            if count == self.n:
                self.labellings[i] = PreferredSemantics.OUT
            else:
                blankNum += 1
        return blankNum

    def updateOUT(self, labellings: list):
        updateNum = 0
        for i in range(self.argNum):
            count = 0
            for j in self.argList[i].setAttackers:
                if labellings[j] == PreferredSemantics.IN:
                    count += 1
                    if count == self.n:
                        if labellings[i] != PreferredSemantics.OUT:
                            if labellings[i] == PreferredSemantics.BLANK:
                                updateNum = updateNum + 1
                            labellings[i] = PreferredSemantics.OUT
                        break
        return updateNum

    def TRANS(self, x: int, labellings: list, label: string):
        labellingsTmp = copy.deepcopy(labellings)
        labellingsTmp[x] = label
        return labellingsTmp

    def inLab(self, labellings: list):
        E = set()
        for i in range(self.argNum):
            if labellings[i] == PreferredSemantics.IN:
                E.add(i)
        return E

    def CheckINValid(self, labellings: list):
        #print(labellings)
        for i in range(self.argNum):
            if labellings[i] != PreferredSemantics.IN:
                continue
            count = 0
            for j in self.argList[i].setAttackers:
                if labellings[j] != PreferredSemantics.OUT:
                    count += 1
                    if count == self.m:
                        return False
        return True

    def FindExt(self, labellings: list, blankNum: int):
        if 0 == blankNum:
            if self.CheckINValid(labellings):
                #print(labellings)
                E = self.inLab(labellings)
                #print(E)
                if len(PreferredSemantics.setPrExt) == 0:
                    PreferredSemantics.setPrExt.append(E)
                else:
                    flag = True
                    for S in PreferredSemantics.setPrExt:
                        if E.issubset(S):
                            flag = False
                            break
                    if flag:
                        PreferredSemantics.setPrExt.append(E)
                        return

        for i in range(len(labellings)):
            if labellings[i] == PreferredSemantics.BLANK:
                labellingsTmp = self.TRANS(i, labellings, PreferredSemantics.IN)
                self.FindExt(labellingsTmp, blankNum - 1 - self.updateOUT(labellingsTmp))
                labellingsTmp = self.TRANS(i, labellings, PreferredSemantics.UNDEC)
                self.FindExt(labellingsTmp, blankNum - 1)

    def EnumPr(self):
        self.FindExt(self.labellings, self.initArgList())
        print(PreferredSemantics.setPrExt)


if __name__ == "__main__":
    '''
    Matrix = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    pr = PreferredSemantics(6, myMatrix, 2, 2)
    pr.EnumPr()
    '''
    Matrix = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    pr = PreferredSemantics(6, myMatrix, 2, 2)
    pr.EnumPr()
