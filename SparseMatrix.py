import scipy.sparse as ss
import numpy as np
import os


class SparseMatrix:
    def __init__(self, argNum: int, filename):
        self.__argNum = argNum
        self.__filename = os.path.dirname(__file__) + '\\' + filename
    
    # 随机产生argNum*argNum的稀疏矩阵
    def getData(self, density):
        data = ss.random(
            self.__argNum,
            self.__argNum,
            density,
            format='csr',
            data_rvs=np.ones,  # fill with ones
            dtype='f'  # use float32 first
        ).astype('int8')  # then convert to int8
        ss.save_npz(self.__filename, data)

        return data

    def ReadData(self):
        return ss.load_npz(self.__filename)
