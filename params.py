from math import inf

C = {
    'name': 'C', # MCTS Exploration Constant
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 1, # For continuous domain
    'domain': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], # For discrete domain
    'default': 0.2
}

eps = {
    'name': 'eps', # Probability of selecting a random action with MAST
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 1, # For continuous domain
    'domain': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], # For discrete domain
    'default': 0.4
}

K_GRAVE = {
    'name': 'K', # Equivalance parameter of GRAVE
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 2000, # For continuous domain
    'domain': [0, 10, 50, 100, 250, 500, 750, 1000, 2000, inf], # For discrete domain
    'default': 250
}

K_UCT = {
    'name': 'K', # Equivalance parameter of GRAVE
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 0, # For continuous domain
    'domain': [0], # For discrete domain
    'default': 0
}

Ref = {
    'name': 'Ref', # Visit threshold used by GRAVE
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 10000, # For continuous domain
    'domain': [0, 50, 100, 250, 500, 1000, 10000, inf], # For discrete domain
    'default': 50
}

VO = {
    'name': 'VO', # Used in mcts selection phase
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 0.025, # For continuous domain
    'domain': [0.001, 0.005, 0.01, 0.015, 0.02, 0.025], # For discrete domain
    'default': 0.01
}

T = {
    'name': 'T', # Min number visits before selection and expansion is performed on a node
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 200, # For continuous domain
    'domain': [0, 5, 10, 20, 30, 40, 50, 100, 200, inf], # For discrete domain
    'default': 0
}