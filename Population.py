import copy
import random
from NN import *
import NN


# noinspection SpellCheckingInspection
class Population:
    def __init__(self):
        self.innovs = []  # innovation number as the index, tuple inside stored as (from, to) as node numbers

    def updatefitness(self, fitness):
        """updates the fitness the ensure protection of innovation, currently unused"""
        allinnovs = []  # allinnovs list stores [(from, to), count] to detect commonality between networks
        for i in range(len(fitness)):
            for j in range(len(fitness[i][0].net.innovs)):
                n = fitness[i][0].net.innovs[j]
                if allinnovs.count(n) == 0:
                    allinnovs.append([n, 1])
                else:
                    allinnovs[allinnovs.index(n)][1] += 1  # idk if its supposed to be j or i, was previously k
        # refer to whiteboard for below # thx past me lol
        for i in range(len(fitness)):  # calculate weights and assign them
            fitweight = 0
            for j in range(len(fitness[i][0].net.innovs)):
                n = fitness[i][0].net.innovs[j]
                for k in range(len(allinnovs)):
                    if allinnovs[k][0] == n:
                        fitweight += len(fitness) / allinnovs[k][1]
            fitness[i][1] *= fitweight  # fitness must be stored as a list as it won't allow item assignment
        return fitness

    def combine(self, net1, net2, net1n, net2n):
        fromnode = None
        tonode = None
        innum = len(net1.inputs)
        outnum = len(net1.outputs)
        nodemut = net1.nodemut
        connectmut = net1.connectmut
        biasmut = net1.biasmut
        newnet = NN.Network(innum, outnum, nodemut, connectmut, biasmut)
        newconnects = []
        for i in range(len(net1.connections)):
            if net2.connections.count(net1.connections[i]) == 0:
                newconnects.append(net1.connections[i])
        for i in range(len(net2.connections)):
            if net1.connections.count(net2.connections[i]) == 0:
                newconnects.append(net2.connections[i])
        for i in range(len(newconnects)):
            for j in range(len(newnet.all)):
                for k in range(len(newnet.all[j])):
                    if newnet.all[j][k].nodenum == newconnects[i][0]:
                        # print(f'newnet[j][k] {newnet.all[j][k]}')
                        fromnode = copy.deepcopy(newnet.all[j][k])
                    if newnet.all[j][k].nodenum == newconnects[i][1]:
                        # print(f'newnet[j][k] {newnet.all[j][k]}')
                        tonode = copy.deepcopy(newnet.all[j][k])
            if fromnode is not None and tonode is not None:
                tonode.inputs.append((copy.deepcopy(fromnode), random.random() * 2 - 1))
            fromnode = None
            tonode = None
        # print(f'Newnet: {newnet}')
        print(f'parents:\n{net1} (fitness:{net1n})\n{net2} (fitness:{net2n})')
        return newnet

    def combfunc(self, fitness, netnum):  # fitness stored as tuple of net and fitness number
        """Takes fitness as a tuple of (net, fitness value) and returns a new net that can be duplicated and mutated"""
        # fitness = self.updatefitness(fitness)
        nets = []
        for net in range(netnum):
            total = 0
            for i in range(len(fitness)):
                total += fitness[i][1] ** 2
            par1 = random.random() * total
            par2 = random.random() * total
            parnet1 = None
            parnet2 = None
            j = 0
            # parnet1 = copy.deepcopy(fitness[-1][0].net)  # code used to guarantee the best net is used
            for i in range(len(fitness)):
                j += fitness[i][1] ** 2
                if j >= par1:
                    parnet1 = copy.deepcopy(fitness[i][0].net)
                    parnet1num = fitness[i][1]
                    print(f'parnum1 deriv: {fitness[i][0]},index: {i}, fitness: {fitness[i][1]}')
                    break
                # print(f'par1, total, j:{par1, total, j}')
            j = 0
            for i in range(len(fitness)):
                j += fitness[i][1] ** 2
                if j >= par2:
                    parnet2 = copy.deepcopy(fitness[i][0].net)
                    parnet2num = fitness[i][1]
                    print(f'parnum2 deriv: {fitness[i][0]},index: {i}, fitness: {fitness[i][1]}')
                    break
            # combined = self.combine(parnet1, parnet2, parnet1num, parnet2num)
            combined = parnet1
            nets.append(combined)
        # print(nets)
        return nets
    # TODO: Test this code with changed "combined" net, combine() = trash, maybe actually fix it... or don't...

    def getinnovs(self, innovs):
        for i in range(len(innovs)):
            if self.innovs.count(innovs[i]) == 0:
                self.innovs.append(innovs[i])

        # for i in range(net1.outputs):
        #     node = net1.outputs[i]           # gonna store connections in the NN
        #     if node.hidden != 0:
        #         for j in range(node.)
        #         connectnode = node.inputs

    def addinnov(self, innov):
        """called from NN, returns innov num and adds it if necessary"""
        # print('Addinnov function')
        # print(f'self: {self}')
        # print(f'innovs: {self.innovs}')
        if self.innovs.count(innov) == 0:
            self.innovs.append(innov)
            return len(self.innovs) - 1
        else:
            return self.innovs.index(innov)
