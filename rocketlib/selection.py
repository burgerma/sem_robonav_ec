import numpy as np
from copy import deepcopy

from rocketlib.population import Rocket
from rocketlib.dna import DNA
# dictonaries
parentselectionmodes = {0: 'fps', 1: 'lin', 2: 'exp', 3: 'by_value'}
survirorselectionmode = {0: '1gen', 1: 'rpl'}


def selection_by_absolute_value(population, maxfitness, limit):
    """
    Parameters
    -----------
        population  : pg.sprite.Group of Rocket Sprites
        limit       : float
                fitness value limit to discriminate

    Returns
    -------
        selecteddna : list
                list of dna, which was chosen for the next generation
    """
    fitness_sum = 0
    selecteddna = []
    for cur_Rocket in population:
        fitness_sum += cur_Rocket.fitness
        if(maxfitness*limit <= cur_Rocket.fitness):
            selecteddna.append(deepcopy(cur_Rocket.dna))

    return selecteddna


def fitness_proportional_selection(population, populationSize, selectSize=None):
    """
    Parameters
    ----------
        population      : pg.sprite.Group of Rocket Sprites
        populationSize  : int
                size of Population
        selectSize      : int
                size of selected DNA
    Returns
    --------
        selecteddna     : list
                list of selected DNA
    """
    if selectSize == None:
        selectSize = populationSize

    rockets = []
    Fmax = 0

    # calculate cumulative fitness and extract rockets to list
    for rocket in population:
        Fmax += rocket.fitness
        rockets.append(rocket)

    # calculate fitness-based probabilities
    propabilities = [rocket.fitness/Fmax for rocket in population]

    # get random rocket indices based on their probabilities
    choices = np.random.choice(populationSize, selectSize, p=propabilities)

    # select rocket dna based on choises
    selecteddna = []
    for i in choices:
        selecteddna.append(deepcopy(rockets[i].dna))

    return selecteddna


def ranking_selection(population, populationSize, s=2, selectSize=None, mode='lin'):
    """
    Parameters
    ----------
        population      : pg.sprite.Group of Rocket Sprites
        populationSize  : int
                size of Population
        s:  int 
            parameter for linear ranking (0...2)
        selectSize: int
            size of selected DNA, (default:None --> use populationSize)
        mode: str
            mode for ranking
            'lin' : linear ranking
            'exp' : exponential ranking
    Returns
    --------
        selecteddna: list
            list of selected DNA
    """
    if selectSize == None:
        selectSize = populationSize

    rockets = []
    # extract rockets to list
    for rocket in population:
        rockets.append(rocket)

    probabilities = None

    rockets.sort(key=sort_key)

    if mode == 'lin':
        probabilities = p_rank_lin(s, populationSize)
    elif mode == 'exp':
        probabilities = p_rank_exp(populationSize)

    # get random rocket indices based on their probabilities
    choices = np.random.choice(populationSize, selectSize, p=probabilities)

    # select rocket dna based on choises
    selecteddna = []
    for i in choices:
        selecteddna.append(deepcopy(rockets[i].dna))

    return selecteddna


def survivor_replace_worst(population, childpopulation, populationSize):
    rockets = []
    for rocket in population:
        rockets.append(rocket)
    for rocket in childpopulation:
        rockets.append(rocket)

    rockets.sort(key=sort_key, reverse=True)

    selecteddna = []
    for i in range(populationSize):
        selecteddna.append(deepcopy(rockets[i].dna))
    #print("Fitness of all rockets %s" %(len(rockets)))
    #print(np.round([rocket.fitness for rocket in rockets]))
    return selecteddna


def sort_key(rocket):
    return rocket.fitness


def p_rank_lin(s, u):
    return [(((2-s)/u)+((2*i*(s-1))/(u*(u-1)))) for i in range(u)]


def p_rank_exp(u):
    p = [(1-np.exp(-i)) for i in range(u)]
    c = sum(p)
    p = p/c
    return p
