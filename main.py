import sys
from PreferredSemantics import PreferredSemantics
from GroundedSemantics import GroundedSemantics
from SparseMatrix import SparseMatrix
from scipy import sparse


def testPr(argNum: int, m: int, n: int, data: sparse.csr_matrix):
    pr = PreferredSemantics(argNum, data, m, n)
    pr.EnumPr()


def testGr(argNum: int, m: int, n: int, data: sparse.csr_matrix):
    pr = GroundedSemantics(argNum, data, m, n)
    pr.ComputGr()


if __name__ == "__main__":
    argNum = int(input('Enter the number of arguments:'))
    m = int(input('Enter m:'))
    n = int(input('Enter n:'))
    if n < m:
        print('It should satisfies n ≥ m!')
        sys.exit()
    myMatrix = SparseMatrix(argNum, 'pr.npz')
    data = myMatrix.getData(0.25)
    # print(data.A)
    # testGr(argNum, m, n, data)
    testPr(argNum, m, n, data)
