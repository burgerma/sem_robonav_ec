# coding: utf8
import numpy as np


class DNA(object):
    """
    Description:
    ------------
        DNA Class for rockets
    """

    def __init__(self):
        self.path = np.asarray([[], []])
        self.accSteps = 0
        self.useCounter = 0

    def generateNewRandomDNA(self, accsteps=200):
        """
        Description:
        -----------
            generates a new random DNA for DNA-Class
        Parameters
        ----------
            accSteps : int
                length of acceleration dna, default: 200
        """

        # set length of acceleration steps
        self.accSteps = accsteps

        # set random acceleration values
        a_x = (((np.random.uniform(-0.5, 0.5, self.accSteps))*10))
        a_y = (((np.random.uniform(0, 1, self.accSteps))*20))

        # Gravity Test
        # self.__accSteps = 100
        # a_x = -np.ones((100))*10
        # a_y = np.ones((100))*20

        self.path = np.append(self.path, [a_x, a_y], axis=1)

        # test with uni-dna
        # self.path = np.ones_like(self.path)
