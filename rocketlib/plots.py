import matplotlib.pyplot as plt
import numpy as np
#from world import RocketWorld

mode2title = {'lin': 'Rank Lin.', 'exp': 'Rank Exp.', 'by_value': 'Fitness Barrier',
            'fps': 'Fitness Proportional', '1pt': '1Point',
            'full': 'Full', 'npt': 'npoint',
            'arith': 'Simple Arithmetic', '1gen': 'Age-Based 1 Generation',
            'rpl': 'Replace worst'}


class AverageFitness():
    """
    Description:
    ------------
        live plot of fitness data
    Parameters:
    -----------
        rworld : RocketWorld
        title : string
            title for plot and window, default: 'Average Fitness'
    """

    def __init__(self, rworld, modes, figtitle = "Average Fitness"):
        self.modes = modes
        self.filename = self.generate_filename(rworld)
        self.title = self.generate_title(rworld)
        # init data lists
        self.generation_fitness = [0]
        self.child_fitness = [0]
        self.maxfitness = [0]
        # create figure and ax
        self.fig = plt.figure(figtitle)
        self.ax = self.fig.add_subplot(111)
        # create data lines to be updated
        self.gf, = self.ax.plot(self.generation_fitness,
                                label="Generation Fitness")
        self.cf, = self.ax.plot(self.child_fitness, label="Child Fitness")
        self.mf, = self.ax.plot(self.maxfitness, label="Max. Fitness")
        # setup labels, title, ax limits
        self.ax.set_xlim([0, rworld.max_genenerations])
        self.ax.set_ylim([0, rworld.fitness_limit])
        self.ax.legend()
        plt.ylabel("Fitness")
        plt.xlabel("Generation")
        plt.title(self.title)
        plt.ion()
        plt.show()

    def update(self, gf, cf, mf):
        """
        Description:
            update fitness plot data
        Parameters:
        ----------
            gf : list of floats
                average generation fitness
            cf : list of floats
                average children fitness
            mf : list of floats
                maximum generation fitness
        """
        # append new data
        self.generation_fitness.append(gf)
        self.child_fitness.append(cf)
        self.maxfitness.append(mf)
        # update lines
        self.gf.set_ydata(self.generation_fitness)
        self.gf.set_xdata(range(len(self.generation_fitness)))
        self.cf.set_ydata(self.child_fitness)
        self.cf.set_xdata(range(len(self.child_fitness)))
        self.mf.set_ydata(self.maxfitness)
        self.mf.set_xdata(range(len(self.maxfitness)))
        # plt.pause(0.1)
    def generate_filename(self,rworld):
        if self.modes[1] == True:
            xtxt = "_Xover_"+self.modes[2]
        else:
            xtxt = "NoXover"

        filename = "EA_Population_"+str(rworld.populationSize)+\
                    "_Sel_"+self.modes[0]+\
                    xtxt+\
                    "_Mut_"+str(self.modes[3])+\
                    "_Rep_"+self.modes[4]+\
                    ".pdf"
        return filename

    def generate_title(self,rworld):
        if self.modes[1] == True:
            xtxt = "Crossover: " + mode2title.get(self.modes[2])
        else:
            xtxt = "No Crossover"

        title = r"Population Size: " + str(rworld.populationSize)+" "+\
                r"Parent Selection: " + mode2title.get(self.modes[0]) +"\n"+\
                xtxt +" "+\
                r"Mutation Rate: " + str(self.modes[3]) + "\n"+\
                r"Survivor Selection: " + mode2title.get(self.modes[4])
        return title

    def save_figure(self):
        self.fig.savefig(self.filename, orientation='landscape', format='pdf')
