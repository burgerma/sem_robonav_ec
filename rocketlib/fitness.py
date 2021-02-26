import rocketlib.utilities as ut
import numpy as np


def calcFitness(world, population):
    """
    Description:
        calculate fitness of a population
    Paramterers:
    ------------
        world       : RocketWorld
        population  : pg.sprite.Group() of Rockets
                fitness of all rockets in the population will be updated
    Returns:
    --------
        avg_fitness : float
                average fitness of the population
    """

    # initalising
    target_pos = ut.from_pygame(world.target, world.height)
    rocket_finalpos = np.zeros((len(population), 2))
    rocket_traveldist = np.zeros((len(population), 1))
    start_pos = np.array([0, 0])

    # get rocket positions and calulate euclidian distances
    for i, rocket in enumerate(population):
        # get start position
        if i == 0:
            start_pos[0] = np.asarray(ut.from_pygame(
                rocket.trajectory[0], world.height))[0]

        # get final rocket positions
        rocket_finalpos[i] = np.asarray(
            ut.from_pygame(rocket.getPos(), world.height))

        # calculate the euclidian distances between consecutive trajectory
        # points and sum up to get total travel distance for each rocket
        rocket_traveldist[i] = np.sum(np.linalg.norm(
            np.diff(rocket.trajectory, axis=0), axis=1))

    # min distance between start and target
    min_path = np.linalg.norm(target_pos-start_pos)

    # calculate target score from euclidian distance from final position to target
    rocket_targetdist = np.linalg.norm(rocket_finalpos-target_pos, axis=1)
    target_score = np.abs(
        np.interp(rocket_targetdist, [0, min_path], [-10, -1]))

    # calculate travel score from deviation from minpath
    delta = np.abs(rocket_traveldist-min_path)
    travel_score = np.abs(np.interp(delta[:, 0], [0, min_path], [-10, -1]))

    fitness_values = score_to_fitness(
        target_score, travel_score, world.travel_weight, world.travel_weight)

    world.maxfitness = max(fitness_values)
    total_fitness = 0

    # update fitness score of rockets
    for i, rocket in enumerate(population):
        rocket.fitness = fitness_values[i]
        total_fitness += fitness_values[i]

    # average fitness
    avg_fitness = total_fitness/len(population)
    return avg_fitness


def score_to_fitness(target_score, travel_score, target_weight, travel_weight):
    """
    Description:
    ------------
        calculate fitness based on travel_score and target_score

    Paramterers:
    ------------
        target_score : np.array
        travel_score : np.array
        target_weight: int or float
        travel_weight: int or float
    Returns:
    --------
        fitness : np.array
    """
    fitness = np.exp(target_score/travel_weight)*(target_weight+travel_score)
    return fitness
