import numpy as np
from random import shuffle
from copy import deepcopy

import rocketlib.utilities as ut
from rocketlib.population import Rocket
from rocketlib.dna import DNA

crossovermodes = {0:'1pt',1:'full',2:'npt',3:'arith'}
#------------------------------------------------------------------------------#
#                              SECTION CROSSOVER                               #
#------------------------------------------------------------------------------#

def crossover_1point(parentdna):

    # shuffle dna List to create a randomized dna draw
    shuffle(parentdna)
    childdna = deepcopy(parentdna)

    i = 0
    while i < len(parentdna)-1:
        # check the path lengths of both parents, and use the shorter one for
        # the random number of the recombination process
        if (len(parentdna[i].path) > len(parentdna[i+1].path)):
            r = np.random.randint(0, np.shape(parentdna[i+1].path)[1])

        else:
            r = np.random.randint(0, np.shape(parentdna[i].path)[1])

        # buffering the dna of the two parents
        dna_mate_a = deepcopy(parentdna[i].path)
        dna_mate_b = deepcopy(parentdna[i+1].path)

        # recombinate the parents dna to two child dnas
        childdna[i].path = np.concatenate(
            (dna_mate_a[:, 0:r], dna_mate_b[:, r:]), axis=1)
        childdna[i+1].path = np.concatenate(
            (dna_mate_b[:, 0:r], dna_mate_a[:, r:]), axis=1)

        # increase the iterator variable by two for the next set of parents
        i += 2
    return childdna


def crossover_full(parentdna):

    # mix parent dna set
    shuffle(parentdna)

    # copy dna set for crossover
    childdna = deepcopy(parentdna)

    # generate children
    i = 0
    while i < len(parentdna)-1:
        # parent path
        mateA = parentdna[i].path
        mateB = parentdna[i+1].path

        # child path
        childA = deepcopy(mateA)
        childB = deepcopy(mateA)

        # crossover
        childA[:, ::2] = mateB[:, 1::2]
        childB[:, 1::2] = mateB[:, ::2]

        # update child dna
        childdna[i].path = childA
        childdna[i+1].path = childB
        i += 2
    return childdna


def crossover_npoint(dnalist, points):
    """
    Parameters
    ----------
        dnalist: list of DNA objects
            list of dna which shall be recombined
        points: int
            number of points to be crossovers
    Returns
    --------
        dnalist: list of DNA objects
            list of recombined dna

    Description
    -----------
        Function to crossover the dna of two parents on a given number of
        points. 
    """
    # check, if number of given points are to many, or equal full crossover
    if (points >= (len(dnalist[0].path[0])-1)):
        print("Given number of crossover points to large!")
        print("Number of crossover points reduced to fit path length.")
        print("Using <crossover_full> instead.")
        dnalist = crossover_full(dnalist)
        return dnalist

    # shuffeling the dna list to simplify the drawing of parents and deep copy
    # the dnalist to avoid address errors and unwanted behaviour
    dnalist = deepcopy(dnalist)
    shuffle(dnalist)

    # all possible indices for the path
    crossover_range = np.arange(1, len(dnalist[0].path[0]-2))

    # first loop iterates over pairs of parents
    for i in range(0, len(dnalist), 2):
        # select new crossover points for each pair of parents and sorting them
        # to simlify the crossover process
        crossover_points = np.array([0, len(dnalist[0].path[0])-1])
        np.random.shuffle(crossover_range)
        crossover_points = np.sort(
            np.append(crossover_points, crossover_range[:points]))

        # containers for the offspring
        childA = deepcopy(dnalist[i].path)
        childB = deepcopy(dnalist[i].path)

        # variable cur_parent is necessary to determine, which parents turn it is
        # to give its dna to the corresponding child
        cur_parent = 1

    # second loop iterates over the crossover points
        for j, cp in enumerate(crossover_points):
            if (j == len(crossover_points)-1):
                break

            if (cur_parent == 1):
                childA[:, cp:crossover_points[j+1]
                       ] = dnalist[i].path[:, cp:crossover_points[j+1]]
                childB[:, cp:crossover_points[j+1]] = dnalist[i +
                                                              1].path[:, cp:crossover_points[j+1]]
                cur_parent = 2
            else:
                childA[:, cp:crossover_points[j+1]
                       ] = dnalist[i].path[:, cp:crossover_points[j+1]]
                childB[:, cp:crossover_points[j+1]] = dnalist[i +
                                                              1].path[:, cp:crossover_points[j+1]]
                cur_parent = 1

        # assigning the offsprings dnas to the list, which shall be returned
        dnalist[i].path = childA
        dnalist[i+1].path = childB

    return dnalist

def simple_arithmetic_crossover(parent_dna, alpha=None, fullmode=False):
    """
    Parameters
    ----------
        parent_dna: list of DNA objects
            list of DNA objects which shall be recombined
        alpha: float 
            recombination coefficient, defaul: None
        fullmode: boolean
            mode, for a recombination of only the upper half of the
            dna sequence or both parts of the sequence. Later one leads to double
            the amount of children dna, default: False
    Returns
    --------
        dnalist: list of DNA objects
            list of recombined dna

    Description
    -----------
        Function which implements the simple arithmetic crossover function. In 
        general it recombines the dna strings equaly to the one-point crossover.
        The recombined genes are calculated between both parent genes, which 
        shall lead to a bigger solution space. For alpha = 0.5 the average
        between both genes will be calculated and replace the former genes
        after (or before) the randomly calculated crossover point.
    """
    if (alpha==None):
        alpha = np.random.uniform()
    dnalist = deepcopy(parent_dna)

    if(fullmode):
        for i in range(len(dnalist)):
            dnalist.append(dnalist[i])

    shuffle(parent_dna)
    
    for i in np.arange(0, len(parent_dna), 2):
        
        # get a random entry in the pathlist 
        r = np.random.randint(0, len(parent_dna[0].path[0]))
        
        child_dna_0 = parent_dna[i].path[:, 0:r]
        child_dna_1 = parent_dna[i+1].path[:, 0:r]


        recombination_data = alpha*parent_dna[i].path[:,:] + \
                                            (1-alpha)*parent_dna[i+1].path[:,:]
        child_dna_0 = np.concatenate((child_dna_0, recombination_data[:,r:]), axis=1)
        child_dna_1 = np.concatenate((child_dna_1, recombination_data[:,r:]), axis=1)
        dnalist[i].path = child_dna_0
        dnalist[i+1].path = child_dna_1

        if(fullmode):
            child_dna_2 = recombination_data[:,:r]
            child_dna_3 = recombination_data[:,:r]

            child_dna_2 = np.concatenate((child_dna_2, parent_dna[i].path[:,r:]), axis=1)
            child_dna_3 = np.concatenate((child_dna_3, parent_dna[i+1].path[:,r:]), axis=1)
            dnalist[i+len(recombination_data[0])].path = child_dna_2
            dnalist[i+1+len(recombination_data[0])].path = child_dna_3

    return dnalist

#!SECTION

#------------------------------------------------------------------------------#
#                               SECTION MUTATION                               #
#------------------------------------------------------------------------------#


def mutate_dnas(dnaList, mutation_rate):

    mutateddna = deepcopy(dnaList)
    # choose how many DNAs to mutate by mutation rate
    dnas_to_mutate = np.random.binomial(len(dnaList), mutation_rate)
    # determine dna indicies of DNAs to mutate
    # TODO mehrfach gleiche Indizes möglich?!?!?!**##!111elf
    dna_indicies = np.random.randint(0, len(dnaList), int(dnas_to_mutate))

    # length of single DNA (amount of genes)
    dna_length = len(dnaList[0].path[1, :])

    # choose how many genes on one DNA shall be mutated
    genes_to_mutate = int(dna_length/10)

    for i in dna_indicies:

        gen_indicies = np.random.randint(0, dna_length, genes_to_mutate)
        # print('gen ind: %s' % (gen_indicies))
        for j in gen_indicies:

            if j < 200:

                mutateddna[i].path[0, j] = (
                    ut.random_floats(decimals=3)-0.5)*14
                mutateddna[i].path[1, j] = (ut.random_floats(decimals=3))*20

    return mutateddna

#!SECTION
