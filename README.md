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

# How to run this?

1. Clone / download this code.
2. You can run `benchmark.py` to perform benchmarking. You can either choose to benchmark a particular allocation strategy or you can choose to benchmark all allocation strategies against an offline tuned agent.

# Guidelines to contribute

1. Fork this repo
2. Clone your forked repo using the command `git clone <url to your fork>`
3. Run `pip install -r requirements.txt` to install dependencies
4. Make changes
5. To commit your changes run the following commands:
   - `git add .`
   - `git commit -m "write a short message here denoting the change you are making"`
   - `git push origin master`
6. Now make a pull request

# Understanding the code structure

##### Entry point:

_main.py_ / _benchmark.py_

##### Other files:

- **main.py:** Can be used for testing during development
- **benchmark.py:** Used to benchmark the agents
- **game.py:** Exports a `Game` class that can be used to specify the agents that'll play the game and the game type. The game can be played by calling the `playGame()` method - used by _main.py_ and _benchmark.py_

## /agents

##### Entry point:

_agentsList.py_ and _Agent.py_

##### Other files:

- **agentsList.py:**
  1. Exports the names of the supported agent types
  2. Exports `benchmarkList` which is an iterable list of the supported agent types
- **Agent.py:** The AI agent that uses an allocation strategy from /tuners and MCTS simulation defined in _mcts.py_

## /agents/tuners

#### A collection of allocation strategies

##### Entry point:

Any one of the tuner (_nmc.py_ or _cmaes.py_)

All tuners implement the methods defined in `TunerMeta`. These methods serve as an API to interact with any tuner.

##### Development Guidelines:

All tuners should extend the `TunerMeta` base class

## /games

##### Entry point:

_gamesList.py_ and _games.py_

All games implement the methods defined in `BoardMeta`. These methods serve as an API to interact with any game.

##### Development Guidelines:

All games should extend the `BoardMeta` base class

##### Other files:

- **gamesList.py:**
  1. Exports the names of the available games
  2. Exports `benchmarkList` which is an iterable list of the available games
- **games.py:** Exports a function to get an instance of a game board

# Contributors

- Ramvardhan R. (https://github.com/ram-the-coder)
- Sathish Kumar E. (https://github.com/sathishk0230)
- Sudharshan V. (https://github.com/Sudharshanv2000)
