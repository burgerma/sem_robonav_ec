# import custom libs
from rocketlib.world import RocketWorld
import rocketlib.utilities as ut

# window settings
resolution = xmax, ymax = (1280, 800)

# environment setup
target = (xmax/2-400, ymax-200)
framerate = 30

# rocket population parameters
populationSize = 100
lifeTime = 200  # old 30

# define evolutionary algorithm parameters and modes in a list
# Parent Selection:
#   'lin'   : Ranking Linear
#   'exp'   : Ranking Exponential
#   'fps'   : Fitness Proportional Selection
# Activate Crossover:
#   boolean
# Crossover Mode
#   '1pt'   : 1-Point Crossover
#   'npt'   : n-Point Crossover
#   'full'  : full Crossover
#   'arith' : simple arithmetic Crossover
# Mutation:
#   float   : Rate
# Survior Selection:
#   'rpl'   : Replace worst (GENITOR)
#   '1gen'  : Age-Based one Generation

modes = ['lin',True,'arith',0.1,'rpl']

if __name__ == "__main__":

    # set up rocket world
    w = RocketWorld(populationSize, resolution,
                    lifeTime, ut.to_pygame(target, ymax),framerate=framerate,modes=modes)
    # run rocket world
    w.run()
