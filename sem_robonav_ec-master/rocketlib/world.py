# coding: utf8
import sys
import os
import copy
import numpy as np
from copy import deepcopy
# pygame imports
import pygame as pg
from pygame.locals import QUIT, KEYDOWN, USEREVENT, K_ESCAPE, K_s, K_d, K_r
from pygame.colordict import THECOLORS as COLORS

# import rocket world libs
from rocketlib.population import Rocket
import rocketlib.utilities as ut
import rocketlib.selection as selection
import rocketlib.variation as variation
import rocketlib.fitness as fitness
import rocketlib.plots as plots     


class RocketWorld(object):
    """
    Description:
    ------------
        world for Rockets
    Parameters
    ----------
        populationSize  : int
            defines the size of the population
        resolution      : tupel (width, height)
            resolution of pygame window
        lifeTime        : int
        target          : tupel
        framerate       : int
        modes           : list
            list of algorithm parameters
    """
    
    def __init__(self, populationSize, resolution,
                 lifeTime, target=(640, 100), framerate=30, modes:list=None):

        if modes == None:
            # set up default algorithm parameters
            # Parent Selection: Ranking Linear
            # Crossover: yes, simple arithmetic crossover
            # Mutation Rate: 0.1
            # Survior Selection: Replace worst GENITOR
            self.modes = ['lin',True,'arith',0.1,'rpl']
        else:
            self.modes = modes

        # population parameters
        self.population = pg.sprite.OrderedUpdates()
        self.childpopulation = None

        # population parameters and stats
        self.populationSize = populationSize
        self.max_genenerations = 50
        self.maxfitness = 0
        self.child_fitness = 0
        self.generation = 1
        self.alive = 0

        # fitness parameters
        self.target_weight = 10
        self.travel_weight = 4
        self.fitness_limit = fitness.score_to_fitness(10, 10, self.target_weight,
                                                      self.travel_weight)

        # rocket dna seeds
        self.lifeTime = lifeTime

        # world parameter
        self.resolution = resolution
        self.height = self.resolution[1]
        self.framerate = framerate
        self.target = target

        # internal variables
        self.__clock = pg.time.Clock()

        # flags
        self.timerFlag = False
        self.activeGen = False
        self.simulate = False
        self.start = False

        # set up directories
        self.gameFolder = os.path.dirname("__file__")
        self.imgFolder = os.path.join(self.gameFolder, "img")

        # set up pygame window
        pg.init()
        self.fontSize = 25
        self.font = pg.font.Font(None, self.fontSize)
        self.screen = pg.display.set_mode(self.resolution)
        pg.display.set_caption("Evolutionary Computing - Rocket World")

        # add icon to pygame window
        icon = pg.image.load(os.path.join(
            self.imgFolder, "rocket_icon.png")).convert_alpha()
        icon.set_colorkey(COLORS['white'])
        pg.display.set_icon(icon)

    def createInitialGen(self):
        for i in range(self.populationSize):
            self.population.add(
                Rocket(self.imgFolder, self.resolution, i))

    def evaluateChildren(self, childdna):
        self.childpopulation = pg.sprite.Group()
        for i in range(len(childdna)):
            self.childpopulation.add(Rocket(self.imgFolder, self.resolution, i,
                                            dna=childdna[i]))

        for curLifetime in range(self.lifeTime):
            for rocket in self.childpopulation:
                rocket.update(simulate=True)
                if(rocket.killFlag == False):
                    self.alive += 1
            if (self.alive == 0):
                break
            self.alive = 0


    def createNewGen(self):
        self.alive = 0
        self.generation += 1

        #----------------------------------------------------------------------#
        #                   SECTION PARENT SELECTION                           #
        #----------------------------------------------------------------------#
        fitness_limit = 0.9
        selectSize = np.int(self.populationSize*1)
        parentdna = []
        
        if self.modes[0] == selection.parentselectionmodes.get(0):
            parentdna = selection.fitness_proportional_selection(
                self.population, self.populationSize, selectSize=selectSize)
        elif self.modes[0] == selection.parentselectionmodes.get(1):
            parentdna = selection.ranking_selection(
                self.population, self.populationSize, selectSize=selectSize,
                mode='lin')
        elif self.modes[0] == selection.parentselectionmodes.get(2):
            parentdna = selection.ranking_selection(
                self.population, self.populationSize, selectSize=selectSize,
                mode='exp')
        elif self.modes[0] == selection.parentselectionmodes.get(3):
            parentdna = selection.selection_by_absolute_value(
                self.population, self.maxfitness, fitness_limit)

        #!SECTION
        #----------------------------------------------------------------------#
        #                     SECTION VARIATION                                #
        #----------------------------------------------------------------------#
        # No Crossover
        if self.modes[1] == False:
            childdna = deepcopy(parentdna)
        # Crossover
        elif self.modes[1] == True:
            if self.modes[2] == variation.crossovermodes.get(0):
                childdna = variation.crossover_1point(parentdna)
            elif self.modes[2] == variation.crossovermodes.get(1):
                childdna = variation.crossover_full(parentdna)
            elif self.modes[2] == variation.crossovermodes.get(2):
                childdna = variation.crossover_npoint(parentdna, 80)
            elif self.modes[2] == variation.crossovermodes.get(3):
                childdna = variation.simple_arithmetic_crossover(
                    parentdna, alpha=None, fullmode=None)
        # Mutation
        if bool(self.modes[3]):
            childdna = variation.mutate_dnas(childdna, mutation_rate=self.modes[3])

        #!SECTION
        
        #----------------------------------------------------------------------#
        #                 SECTION SURVIVOR SELECTION                           #
        #----------------------------------------------------------------------#
        # simulate population of children
        self.evaluateChildren(childdna)
        # calculate fitness of children
        self.child_fitness = fitness.calcFitness(self, self.childpopulation)
        # 
        # Age-Based Replacement
        # lifespan 1 generation
        if self.modes[4] == selection.survirorselectionmode.get(0):
            survivordna = deepcopy(childdna)
        # 
        # Fitness-Based Replacement
        # Replace worst (GENITOR)
        elif self.modes[4] == selection.survirorselectionmode.get(1):
            survivordna = selection.survivor_replace_worst(self.population,
                                                       self.childpopulation, self.populationSize)
        #!SECTION
        #----------------------------------------------------------------------#
        #                     SECTION REPLACEMENT                              #
        #----------------------------------------------------------------------#
        self.killCurGen()
        # flag for rocket with max fitness in current generation
        king = False
        for i in range(self.populationSize):
            if i < len(survivordna):
                # flag for rocket with max fitness in current generation
                if i == self.populationSize-1:
                    king = True
                self.population.add(Rocket(self.imgFolder, self.resolution, i,
                                           dna=survivordna[self.populationSize-1-i],king=king))
            else:
                self.population.add(Rocket(self.imgFolder, self.resolution, i))
        return
        #!SECTION

    def killCurGen(self):
        self.population = pg.sprite.Group()
        return

    def eventCheck(self):
        '''
        Description:
        -----------
            check for events, e.g pressed keys
        '''
        for event in pg.event.get():
            if event.type == USEREVENT+1:
                self.timerFlag = False

            if event.type == KEYDOWN and event.key == K_s:
                self.simulate = True
            if event.type == KEYDOWN and event.key == K_d:
                self.simulate = False
            if event.type == KEYDOWN and event.key == K_r:
                self.start = True

            if event.type == QUIT or (event.type == KEYDOWN
                                      and event.key == K_ESCAPE):
                pg.quit()
                sys.exit()

    #------------------------------------------------------------------------------#
    #                                 SECTION DRAW                                 #
    #------------------------------------------------------------------------------#

    def draw(self):
        """
        Description:
            draw everything to the screen
        """
        # reset to black screen
        # comment next line for fancy effects :-)
        self.screen.fill(COLORS['black'])


        # draw transparent trajectories
        surface = pg.Surface(self.resolution)
        surface.set_alpha(125)
        surface.fill(COLORS['black'])

        for rocket in self.population:
            pg.draw.lines(surface, COLORS['cyan'],
                          False, rocket.trajectory,1)
        self.screen.blit(surface, (0, 0))

        # draw target
        pg.draw.circle(self.screen, COLORS['white'], self.target, 15)

        # draw rockets3
        self.population.draw(self.screen)

        # FPS Display, Generation and Alive Counter
        fps = self.font.render("FPS: " + str(int(self.__clock.get_fps())), True,
                               COLORS['white'])
        generation = self.font.render("Generation: %s" % (int(self.generation)),
                                      True, COLORS['white'])
        alive = self.font.render("Alive: %s" % (int(self.alive)),  True,
                                 COLORS['white'])
        self.screen.blit(alive, (50, 78))
        self.screen.blit(generation, (50, 64))
        self.screen.blit(fps, (50, 50))

        # has to be the last screen command, otherwise there is nothing to see
        pg.display.flip()
        #!SECTION

    def run(self):
        """
        Description:
        ------------
            run RocketWorld Evolutionary Algorithm with Fitness Plot and visualization
            of rockets
        Use keyboard to control:
        -----------------------
            press 'r' to start run of algorithm
            press 's' to switch to simulation only (rockets wont draw)
            press 'd' to activate draw of rockets
        """
        # create initial Population (1. Generation)
        if (self.activeGen == False):
            self.createInitialGen()
            self.activeGen = True

        # init live plotter for average fitness
        FitnessPlotter = plots.AverageFitness(
            self, self.modes)

        # display usage hints
        ut.display_hints(self)
        # wait for key press 'r' to run algorithm
        while not self.start:
            self.eventCheck()

        while self.start:
            # lifecyle iteration
            for curLifetime in range(self.lifeTime):
                # clock ticks for drawing
                if self.simulate == False:
                    self.__clock.tick(self.framerate)
                # check for events
                self.eventCheck()

                # update rockets
                for rocket in self.population:
                    rocket.update(simulate=self.simulate)
                    if(rocket.killFlag == False):
                        self.alive += 1
                # draw rockets
                if self.simulate == False:
                    self.draw()
                if (self.alive == 0):
                    break
                self.alive = 0

            # evaluate the fitness of current generation
            af = fitness.calcFitness(self, self.population)
            print("Generation %s: Average Fitness: %s" %
                  (self.generation, round(af)))

            # update fitness plot
            FitnessPlotter.update(af, self.child_fitness, self.maxfitness)

            # check for generation limit and save plots
            if self.generation == self.max_genenerations:
                FitnessPlotter.save_figure()
                self.start = False
                break

            # create next generation
            self.createNewGen()
