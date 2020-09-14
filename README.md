# Self Adaptive Monte Carlo Tree Search (SA-MCTS)
General game playing (GGP) is the design of artificial intelligence programs
that can play games it has never seen before by figuring out the strategy on
the go. Monte Carlo Tree Search (MCTS) is a popular method for developing
GGP AI. MCTS along with its enhancements have some parameters that
control the algorithm. Usually, these parameters are tuned on-line by trying
many combinations manually. This means the AI may perform well in some
games and perform badly in some others. This project aims to implement an online
parameter tuning strategy i.e. a self-adaptive MCTS (SA-MCTS) strategy
that finds the best parameters for the particular game while performing the
search.  

This is an implemention of **C. F. Sironi, J. Liu and M. H. M. Winands, "Self-Adaptive Monte Carlo
Tree Search in General Game Playing," in IEEE Transactions on Games,
vol. 12, no. 2, pp. 132-144, June 2020, doi: 10.1109/TG.2018.2884768**

# Understanding the code
##### Entry point: 
*main.py* / *benchmark.py*

##### Other files:
* **main.py:** Can be used for testing during development
* **benchmark.py:** Used to benchmark win ratio of all the types of agents against the others in all available games
* **game.py:** Exports a `Game` class that can be used to specify the agents that'll play the game and the game type. The game can be played by calling the `playGame()` method - used by *main.py* and *benchmark.py*

## /agents
##### Entry point: 
*agentsList.py* and *Agent.py*

##### Other files:
* **agentsList.py:** 
    1. Exports the names of the supported agent types
    2. Exports `benchmarkList` which is an iterable list of the supported agent types
* **Agent.py:** The AI agent that uses an allocation strategy from /tuners and MCTS simulation defined in *mcts.py*

## /agents/tuners
#### A collection of allocation strategies
##### Entry point: 
Any one of the tuner (*nmc.py* or *cmaes.py*)
##### Development Guidelines:
All tuners should extend the `TunerMeta` base class

## /games
##### Entry point:
*gamesList.py* and *games.py*
##### Development Guidelines:
All games should extend the `BoardMeta` base class
##### Other files:
* **gamesList.py:**
    1. Exports the names of the available games
    2. Exports `benchmarkList` which is an iterable list of the available games
* **games.py:** Exports a function to get an instance of a game board

# Contributors
* Ramvardhan R. (https://github.com/ram-the-coder)