import sys
sys.path.append('../')
import src as ttt
import cProfile
composition = [ttt.Team([ttt.Rating()]),ttt.Team([ttt.Rating()])]
pr = cProfile.Profile()
pr.enable()
for _ in range(100):
    game = ttt.Game(composition,[0,1])
pr.disable()
pr.print_stats(sort='time')

