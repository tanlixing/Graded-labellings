import copy
import string
from Argument import Argument
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
        self.blankList = []

    def initIn(self):
        for i in range(self.argNum):
            if len(self.argList[i].Attackers) < self.m:
                self.labellings[i] = PreferredSemantics.IN
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
                self.labellings[i] = PreferredSemantics.OUT
            else:
                self.blankList.append(i)

    def updateOUT(self, labellings: list):
        for i in range(self.argNum):
            count = 0
            for j in self.argList[i].Attackers:
                if labellings[j] == PreferredSemantics.IN:
                    count += 1
                    if count == self.n and labellings[
                            i] != PreferredSemantics.OUT:
                        labellings[i] = PreferredSemantics.OUT
                        break

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
        # print(labellings)
        for i in range(self.argNum):
            if labellings[i] != PreferredSemantics.IN:
                continue
            count = 0
            for j in self.argList[i].Attackers:
                if labellings[j] != PreferredSemantics.OUT:
                    count += 1
                    if count == self.m:
                        return False
        return True

    def SelectArg(self, labellings: list):
        for item in self.blankList:
            if labellings[item] == PreferredSemantics.BLANK:
                return item
        return -1

    def FindExt(self, labellings: list):
        index = self.SelectArg(labellings)
        if -1 == index:
            if self.CheckINValid(labellings):
                # print(labellings)
                E = self.inLab(labellings)
                # print(E)
                if len(PreferredSemantics.setPrExt) == 0:
                    PreferredSemantics.setPrExt.append(E)
                else:
                    flag = True
                    for S in PreferredSemantics.setPrExt:
                        if S.issubset(E):
                            PreferredSemantics.setPrExt.remove(S)
                        elif E.issubset(S):
                            flag = False
                            break
                    if flag:
                        PreferredSemantics.setPrExt.append(E)
            return

        labellingsTmp = self.TRANS(index, labellings, PreferredSemantics.IN)
        self.updateOUT(labellingsTmp)
        self.FindExt(labellingsTmp)
        labellingsTmp = self.TRANS(index, labellings, PreferredSemantics.UNDEC)
        self.FindExt(labellingsTmp)

    def EnumPr(self):
        self.initArgList()
        self.blankList.sort(key=lambda x: self.argList[x].getNeighbornum(),
                            reverse=True)
        # print(self.blankList)
        self.FindExt(self.labellings)
        print(PreferredSemantics.setPrExt)


if __name__ == "__main__":
    '''
    Matrix = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    pr = PreferredSemantics(6, myMatrix, 2, 2)
    pr.EnumPr()
    '''
    Matrix = np.array([[0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                       [0, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1],
                       [0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0]])
    myMatrix = sparse.csr_matrix(Matrix)
    pr = PreferredSemantics(6, myMatrix, 2, 2)
    pr.EnumPr()
