# Seminar Roboternavigation - Evolutionary Computing
Demonstrator for an ***Evolutionary Algorithm*** with small rocktes trying to evolve towards reaching a marked target
# Requirements
Use `pip install -r requirements.txt` to install requirements

Or manually install:

    - pygame 1.9.4
    - numpy 1.15.1
    - matplotlib 2.2.3
# Usage
Run `python main.py`. The evolutionary algorithm runs with a default parameter set. For changing the parameters and modes please refere to the corresponding section below. The live plot shows the average fitness of the current generation, average fitness of children and current maximal fitness in the population. The algorithm runs for 50 generations. At the end the plot is saved as a pdf file in the program directory.

### Key bindings
| Key                | Function                     |
| ------------------ | ---------------------------- |
| **<kbd>R</kbd>**   | run algorithm                |
| **<kbd>S</kbd>**   | simulation only (no drawing) |
| **<kbd>D</kbd>**   | activate drawing             |
| **<kbd>ESC</kbd>** | exit                         |

# Parameters and modes
 Parameters and modes are set by the *modes* list in `main.py` that is handed over to the `RocketWorld`.  
 The *modes* list **needs** the following format:
    
    modes = [pstr, xbool, xstr, mfloat, sstr]

All possible values are listed below.
 
## Table of modes and parameters
| **pstr** | **Parent Selection Mode**          | **sstr** | **Survivor Selection Mode**  |
| -------- | ------------------------------ | -------- | ------------------------ |
| 'lin'    | Ranking Linear                 | 'rpl'    | replace worst (GENITOR)  |
| 'exp'    | Ranking Exponential            | '1gen'   | age-based one Generation |
| 'fps'    | Fitness Proportional Selection |

| **xbool** | **Crossover**       | **xstr** | **Crossover Mode**              |
| --------- | --------------- | -------- | --------------------------- |
| True      | apply crossover | '1pt'    | 1-point crossover           |
| False     | no crossover    | 'npt'    | n-point crossover           |
|           |                 | 'full'   | full crossover              |
|           |                 | 'arith'  | simple arithmetic crossover |

| **mfloat** | **Mutationrate**      |
| ---------- | ----------------- |
| float      | set mutation rate |






