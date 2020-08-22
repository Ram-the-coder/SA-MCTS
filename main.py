from nmc import NMCParameterTuning, MultiArmedBandit

nmc = NMCParameterTuning(1)
nmc.addArmsForParameters(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
while True:
    ch = input('Play? ')
    if ch != 'y':
        break
    nmc.play()