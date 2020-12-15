import math
import random


class Node:
    def __init__(self, layer, nodenum):
        self.inputs = []
        self.layer = layer
        self.outval = None
        self.values = []
        self.weightreduc = 1000
        self.nodenum = nodenum

    def getval(self, inputval):  # recieves main input from NN class
        if self.layer == 0:
            self.outval = inputval

    def returnval(self, hidbias, outbias):  # returns the value of the node
        self.values = []
        if self.layer == 0:
            return self.outval
        else:
            # print(self.inputs)
            for i in range(len(self.inputs)):
                # print(f'self.inputs[i]: {self.inputs[i]}')
                self.values.append(self.inputs[i][0].returnval(hidbias, outbias) * self.inputs[i][1] / self.weightreduc)
                if self.layer == 1:
                    self.values[i] += hidbias
                elif self.layer == 2:
                    self.values[i] += outbias
                # ^appends input values * weights to list
            self.outval = math.tanh(sum(self.values))
            return self.outval
