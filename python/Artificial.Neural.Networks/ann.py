#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
#-*-encoding = 'utf-8'-*-
#this is the test for neural network test
#version 1.0

import random

class Mynn():
    '''
    This is a neural network project.
    var = [eta, epoch,
    func = [predict, train
    '''
    def __init__(self, eta=0.02, epoch=50, input=4):
        self.eta = eta
        self.epoch = epoch
        self.input = input
        self._W_setosa = [random.uniform(-1, 1) for i in range(self.input+1)]
        self._W_versicolor = [random.uniform(-1, 1) for i in range(self.input+1)]
        self._W_virginica = [random.uniform(-1, 1) for i in range(self.input+1)]

    def _sigma_(self, result:float, theta=0.2):
        if result > theta:
            return 1.0
        else:
            return -1.0

    def _output_(self, X:list, flag="name"):
        if flag == "setosa":
            wi = self._W_setosa
        elif flag == "versicolor":
            wi = self._W_versicolor
        elif flag =="virginica":
            wi = self._W_virginica
        else:
            print("please set flag to %s", "_output_")
        gz = sum([a*b for a, b in zip(X, wi)])
        return self._sigma_(gz)

    def _update_(self, X:list, error=0, flag="name"):
        if error == 0:
            pass
        update = [error*self.eta*i for i in X]
        if flag == "setosa":
            self._W_setosa  = [w+u for w, u in zip(self._W_setosa, update)]
        elif flag == "versicolor":
            self._W_versicolor = [w+u for w, u in zip(self._W_versicolor, update)]
        elif flag =="virginica":
            self._W_virginica = [w+u for w, u in zip(self._W_virginica, update)]
        else:
            print("please set flag to [%s}", "_update_")

    def predict(self, X:list):
        X = [1.0] + X
        result = {}
        result['setosa'] = self._sigma_(self._output_(X, 'setosa'))
        result['versicolor'] = self._sigma_(self._output_(X, 'versicolor'))
        result['virginica'] = self._sigma_(self._output_(X, 'virginica'))
        print(result)

    def train(self, X_Doub:list, Y_Sing:list, flag="name"):
        Data = [X+[Y] for X, Y in zip(X_Doub, Y_Sing)]
        random.shuffle(Data)
        for _ in range(self.epoch):
            error = 0
            for *X, y in Data:
                X = [1.0] + X
                err = y - self._output_(X, flag)
                self._update_(X, err, flag)
#                print(self._W_setosa)
        return self

if __name__ == "__main__":
    import re
    Y_1 = []
    Y_2 = []
    Y_3 = []
    with open("/Users/Godfather/Downloads/data.txt", mode='r') as f:
        X_bach = []
        Y = []
        for line in f:
            *X, y = re.split(r',', line)
            X_list = []
            for _ in X:
                X_list.append(float(_)/2.0)
            X_bach.append(X_list)
            Y.append(y)
    for _ in Y:
        if re.search('setosa', _) :
            Y_1.append(1.0)
            Y_2.append(-1.0)
            Y_3.append(-1.0)
            continue
        if re.search('versic', _) :
            Y_1.append(-1.0)
            Y_2.append(1.0)
            Y_3.append(-1.0)
            continue
        if re.search('irgin', _):
            Y_1.append(-1.0)
            Y_2.append(-1.0)
            Y_3.append(1.0)
            continue
    model = Mynn()
    model.train(X_bach, Y_1, 'setosa')
    model.train(X_bach, Y_2, 'versicolor')
    model.train(X_bach, Y_3, 'virginica')
    X1 = [4.9, 3.1, 1.5, 0.1]
    X2 = [6.5, 3.0, 5.2, 2.0]
    X3 = [5.3, 3.7, 1.5, 0.2]
    model.predict(X1)
    model.predict(X2)
    model.predict(X3)