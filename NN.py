import random
from Node import *
from Population import *
#import Population
# from Population import Population.addinnov
import pygame


# noinspection SpellCheckingInspection
class Network:
    def __init__(self, innum, outnum, nodemut=0.01, connectmut=0.1, biasmut=0.1, tanmult=0.1, logrange=(-2, 0), biasrange=10):
        """
        :param innum: Number of input nodes
        :param outnum: Number of output nodes
        :param nodemut: Rate of node mutation in the hidden layer
        :param connectmut: Rate of connection mutation
        :param biasmut: Rate of bias mutation, both in hidden and output layers with equal probability
        :param tanmult: The tangent multiplier for the tan-1 curve
        :param logrange: Range of exponent numbers for the relative bias mutation shifts
        :param biasrange: The absolute range of the randomly set non-relative bias (can exceed with relative bias mut)
        """
        self.nodemut = nodemut
        self.connectmut = connectmut
        self.biasmut = biasmut
        self.nodelayer = 0
        self.tonode = 0
        self.fromnode = 0
        self.hidbias = random.random() * 20 - 10
        self.outbias = random.random() * 20 - 10
        self.inputs = []
        self.hidden = []
        self.outputs = []
        self.maininputs = []  # inputs from the main program
        self.mainoutputs = []  # outputs to the main program
        self.all = [self.inputs, self.hidden, self.outputs]  # don't think this is filled here, needs to be refreshed
        self.innovs = []  # the container a tuple of: (from, to) as node numbers, innov number dealt with in population
        self.nodecount = 0
        self.connections = []
        self.popfuncs = Population()  # experimental variable to fix some import issues
        self.tanmultiplier = tanmult  # multiplier for tangent function used in biases
        self.logrange = logrange
        self.biasrange = biasrange
        for i in range(innum):
            self.inputs.append(Node(0, self.nodecount))
            self.nodecount += 1
        for i in range(outnum):
            self.outputs.append(Node(2, self.nodecount))
            self.nodecount += 1
        if innum <= 0 or outnum <= 0:  # checks if class was initiated with too small values
            raise ValueError('Input or Output value to small')
        # self.all = [self.inputs, self.hidden, self.outputs] # repeated statement to refresh for newly add nodes, first
        # set statement maybe not necessary
        self.connectall()
        # print('yall gonna connect the dots')   # lmao wtf

    def connectall(self):  # connects all nodes when generating a net # idk how useful this is # idk if compatible
        self.mutlayer = 2  # most of this function ripped straight from mutate()  # only needs to be set once
        for i in range(len(self.outputs)):
            self.mutnode = self.all[self.mutlayer][i]
            for j in range(len(self.inputs)):
                self.innode = self.all[self.mutlayer - 2][j]
                self.mutnode.inputs.append((self.innode, random.random() * 2 - 1))  # weights still need to be random

    def mutate(self):
        # print('mutate')
        muttype = random.randint(1, 3)  # 1 = node mut, 2 = connect mut, 3 = bias mut
        if muttype == 1 or True:  # testing with multiple mutations in one cycle
            if random.randint(1, int(1 / self.nodemut)) == 1:  # node add mutation # int to prevent errors
                layer = 2  # hidden or output connected nodes
                node = self.all[layer][random.randint(0, len(self.all[layer]) - 1)]
                if len(node.inputs) != 0:
                    connectnum = random.randint(0, len(node.inputs) - 1)
                    connectnode = node.inputs[connectnum][0]
                    del node.inputs[connectnum]
                    self.hidden.append(Node(1, self.nodecount))
                    self.nodecount += 1
                    # print(f'Connect node + num: {connectnode, connectnum}')
                    # print(f'Node.inputs: {node.inputs}')
                    self.hidden[-1].inputs.append((connectnode, random.random() * 2 - 1))
                    node.inputs.append((self.hidden[-1], random.random() * 2 - 1))  # inputs stored as (node, weight)
                    self.connections.append((self.hidden[-1].nodenum, node.nodenum))
                    self.connections.append((connectnode, self.hidden[-1].nodenum))
                    # print('check1')
                    self.addinnovs(self.hidden[-1].nodenum, node.nodenum,
                                   self.popfuncs.addinnov((self.hidden[-1].nodenum, node.nodenum)))
                    # print('check2')
                    self.addinnovs(connectnode, self.hidden[-1].nodenum,
                                   self.popfuncs.addinnov((connectnode, self.hidden[-1].nodenum)))
                    # print('check3')
                    # print('\n\n\n\n\n\n\n\n\n\ninnode added')
        if muttype == 2 or True:
            if random.randint(1, int(1 / self.connectmut)) == 1:  # connection add mutation
                i = 1
                while i == 1:
                    self.mutlayer = random.randint(1, 2)
                    if (self.mutlayer == 1 or self.mutlayer == 2) and len(self.hidden) == 0:
                        # print(self.all)
                        self.mutlayer = 2
                        # print(self.mutlayer)
                        self.innode = self.all[self.mutlayer - 2][
                            random.randint(0, len(self.all[self.mutlayer - 2]) - 1)]
                        # skip hidden
                    else:
                        # print(self.all)
                        # print(self.mutlayer)
                        self.innode = self.all[self.mutlayer - 1][
                            random.randint(0, len(self.all[self.mutlayer - 1]) - 1)]  # input
                    self.mutnode = self.all[self.mutlayer][
                        random.randint(0, len(self.all[self.mutlayer]) - 1)]  # pick a node
                    self.mutnode.inputs.append((self.innode, random.random() * 2 - 1))  # add connection node & weight
                    # self.hidden.append(Node(1)) ################## must be pushed between 2 nodes and use ?averaged or
                    # halfed? weights
                    self.connections.append((self.innode.nodenum, self.mutnode.nodenum))
                    self.addinnovs(self.innode.nodenum, self.mutnode.nodenum,
                                   self.popfuncs.addinnov((self.innode.nodenum, self.mutnode.nodenum)))
                    # print('connectmut executed')
                    i = random.randint(1, 2)  # possibly add var for mutation repetition rate
        if muttype == 3 or True:
            if random.randint(1, int(1 / self.biasmut)):  # connection bias mutation
                logmultiplier = random.randint(self.logrange[0], self.logrange[1]) # splits range tuple in ran func
                if random.randint(1, 4) == 1:  # 25% chance of non-relative bias change
                    layer = random.randint(1, 2)
                    changenum = (random.random() * (self.biasrange * 2) - self.biasrange)
                    if layer == 1 and len(self.hidden) > 0:
                        self.hidbias = changenum
                    else:
                        self.outbias = changenum
                    # print(f'changenum: {changenum}')
                else:
                    layer = random.randint(1, 2)
                    changenum = (random.random() * (self.biasrange * 2) - self.biasrange) ** logmultiplier
                    if layer == 1 and len(self.hidden) > 0:  # to not change an unused variable
                        self.hidbias += math.tan(changenum) * self.tanmultiplier
                    else:
                        self.outbias += math.tan(changenum) * self.tanmultiplier
                    # print(f'mathtan: {math.tan(changenum) * self.tanmultiplier},changenum: {changenum}')

    def run(self):
        self.mainoutputs = []
        # print(f'self.in {self.inputs}')
        # print(f'mainin {self.maininputs}')
        for i in range(len(self.inputs)):
            self.inputs[i].getval(self.maininputs[i])
        for i in range(len(self.outputs)):
            self.mainoutputs.append(self.outputs[i].returnval(self.hidbias, self.outbias))
        # print(f'bias: {self.outbias}')

    def getinput(self, inputlist):  # gets main inputs from main program
        self.maininputs = inputlist

    def getoutput(self):
        # print(self.mainoutputs)
        return self.mainoutputs

    def get_layers(self):
        # print()
        for i in range(len(self.inputs)):
            print(f'in> {self.inputs[i].inputs}')
        for i in range(len(self.hidden)):
            print(f'hid> {self.hidden[i].inputs}')
        for i in range(len(self.outputs)):
            print(f'out> {self.outputs[i].inputs}')
        print()
        pass

    def addinnovs(self, a, b, c):  # innov numbers stored as (from, to, innov number)
        self.innovs.append((a, b, c))

    # TODO: fix nets appearing empty
    def drawnet(self, screen, x, y, r):  # called from main to draw the selected net
        for i in range(len(self.outputs)):
            for j in range(len(self.outputs[i].inputs)):
                # print(f'i, j, Nodenum: {i, j, self.outputs[i].inputs[j][0].nodenum}')
                l1 = self.outputs[i].inputs[j][0].layer
                n1 = self.outputs[i].inputs[j][0].nodenum
                l2 = 2
                n2 = i
                width = int(self.outputs[i].inputs[j][1] * 5)
                if self.outputs[i].inputs[j][1] < 0:  # setup for drawing node connections
                    colour = (0, 200, 200)
                    #print('les negatori')
                elif self.outputs[i].inputs[j][1] > 0:  # test for inaccurate value statement (not the value i want)
                    colour = (200, 0, 0)
                elif self.outputs[i].inputs[j][1] == 0:  # test for inaccurate value statement (not the value i want)
                    colour = (200, 200, 200)
                else:
                    colour = (0, 0, 0)
                    print('something went wrong')
                    print(self.outputs[i].inputs[j][1])
                pygame.draw.line(screen, colour, (x + l1 * r * 8, y + n1 * r * 4),
                                 (x + l2 * r * 8, y + n2 * r * 4), width)  # l means 'layer', n means 'number'
        for i in range(len(self.hidden)):
            for j in range(len(self.hidden[i].inputs)):
                # print(f'i, j, Nodenum: {i, j, self.outputs[i].inputs[j][0].nodenum}')
                l1 = self.hidden[i].inputs[j][0].layer
                n1 = self.hidden[i].inputs[j][0].nodenum
                l2 = 1
                n2 = i
                print(f'n1: {n1}')
                width = int(self.hidden[i].inputs[j][1] * 5)
                if self.hidden[i].inputs[j][1] < 0:  # setup for drawing node connections
                    colour = (0, 200, 200)
                elif self.hidden[i].inputs[j][1] >= 0:  # test for inaccurate value statement (not the value i want)
                    colour = (200, 0, 0)
                else:
                    colour = (200, 200, 200)
                    print('something went wrong')
                    print(self.hidden[i].inputs[j][1])
                pygame.draw.line(screen, colour, (x + l1 * r * 8, y + n1 * r * 4),
                                 (x + l2 * r * 8, y + n2 * r * 4), width)  # x & y: screen pos, r: node radius
        # next draw node indicators
        x = int(x)
        y = int(y)  # prevents floating point values raising errors eg. 300.0 raising error
        r = int(r)
        for i in range(3):
            for j in range(len(self.all[i])):
                pygame.draw.circle(screen, (255, 255, 255), (x + i * r * 8, y + j * r * 4), r)
                pygame.draw.circle(screen, (0, 0, 0), (x + i * r * 8, y + j * r * 4), r, 1)

    def isempty(self):
        if len(self.outputs) == 0:
            return True
        else:
            return False

# TODO: Make sure you can't have 2 or more connections between the same nodes, bc that would be dumb
