from Bird import *
from Pipe import *
from Population import *
import pygame
from pygame.locals import *
import sys

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("DotsAI")
screen = pygame.display.set_mode((600, 600))
scr_w = screen.get_width()
scr_h = screen.get_height()
pipetick = 240
pipes = [Pipe(screen, 1)]
eventtick = 0
score = 0
fitnesslist = []  # probs stored as [[net, fitness],...]
font = pygame.font.Font(None, 60)

# net settings
popsize = 50
newnetrate = 0.1  # fraction of totally random nets
newnetnum = 3  # how many parent nets are generated
gen = 0
stripemptynets = True
topkeepnum = 3  # not included in popnum

population = Population()
birds = []
for i in range(popsize):
    # print(i)
    birds.append(Bird(screen))


# protect innovation
def reset():
    global pipetick, pipes, eventtick, birds, score, fitnesslist, gen, newnetnum
    pipetick = 240
    pipes = [Pipe(screen, 1)]
    eventtick = 0
    score = 0
    gen += 1
    # print(gen)
    print(fitnesslist)
    nets = copy.deepcopy(population.combfunc(fitnesslist, newnetnum))
    print(fitnesslist)
    for i in range(int(popsize * (1 - newnetrate))):
        birds.append(Bird(screen, copy.deepcopy(nets[random.randint(0, len(nets) - 1)])))
        birds[-1].net.mutate()
    for i in range(int(popsize * newnetrate)):
        birds.append(Bird(screen))
    for i in range(0, popsize):
        # birds[i].net.mutate()
        pass

    for i in range(topkeepnum):
        print(f'Saved net: {fitnesslist[-(i+1)][0]},fitnesslist: {fitnesslist[-(i+1)][1]},score: {fitnesslist[-(i+1)][0].score}')
        birds.append(Bird(screen, fitnesslist[-(i+1)][0].net))  # makes sure the best of the last generation continues
    fitnesslist = []
    for i in birds:
        i.reset()
    print('New Generation')


if __name__ == '__main__':
    while 1:
        clock.tick(60 + 10 * score)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            for i in range(len(birds)):
                fitnesslist.append([birds[0], birds[0].score])
                del birds[0]
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            birds[-1].net.get_layers()
        screen.fill((0, 50, 255))
        if pipetick > 0:
            pipetick -= 1
        else:
            pipes.append(Pipe(screen))
            pipetick = 240
        # if score == 0:  # 10 as buffer cause i cant be bothered to work it out
        #   pipes.append(Pipe(screen, 1))  # 1 indicates a set height for the first pipe
        i = 0
        while i < len(pipes):
            # print(i)
            if pipes[i].edge():
                del pipes[i]
                i -= 1
                continue
            pipes[i].move()
            pipes[i].draw()
            i += 1
        i = 0
        while i < len(birds):
            # print(i)
            birds[i].tick()
            birds[i].getevents(events)
            birds[i].getpipey(pipes[0].y1, pipes[0].y2)
            birds[i].move()
            if birds[i].net.isempty() == 1:
                del birds[i]
                i -= 1
            #print(birds[i].net.hidbias)
            # print(i)
            if pipes[0].collide(birds[i].getrect()):
                # reset()
                fitnesslist.append([birds[i], birds[i].score])  # store as list to support object assignment
                del birds[i]
                # print('death')
                continue
            score += pipes[0].scoreup(birds[-1].x, score)
            if birds[i].collide():
                # reset()
                fitnesslist.append([birds[i], birds[i].score])
                del birds[i]
                # i -= 1
                continue
            birds[i].draw()
            i += 1
        if len(birds) == 0:
            # print(fitnesslist)
            reset()

        screen.blit(font.render(str(score), True, (0, 0, 0)), (scr_w / 2, 10))
        screen.blit(font.render(str(gen), True, (0, 0, 0)), (10, 10))
        txt = font.render(str(len(birds)), True, (0, 0, 0))
        screen.blit(txt, (scr_w - txt.get_width(), 10))
        # print(scr_w/2)
        birds[-1].net.drawnet(screen, scr_w / 2 + 50, 10, 10)
        # Bird(screen).net.drawnet(screen, scr_w + 20, 10, 5)
        pygame.event.pump()
        pygame.display.update()

# TODO: stop it being slow AF, basically just optimise it a bit
