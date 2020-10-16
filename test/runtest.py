import unittest
import sys
sys.path.append('..')
import src as ttt
#import old
from importlib import reload  # Python 3.4+ only.
reload(ttt)
#reload(old)
import math

#import trueskill as ts
#env = ts.TrueSkill(draw_probability=0.25)
import time

#start = time.time()
#g = ttt.Game([[ttt.Rating(ttt.Gaussian(29,1))] ,[ttt.Rating()]], [1,0], 0.0)
#time.time() -start

#start = time.time()
#g = old.Game([[old.Rating(29,1)] ,[old.Rating()]], [1,0], 0.0)
#time.time() -start

class tests(unittest.TestCase):
    def test_gaussian_init(self):
        N01 = ttt.Gaussian(mu=0,sigma=1)
        self.assertAlmostEqual(N01.mu,0)
        self.assertAlmostEqual(N01.sigma,1.0)
        Ninf = ttt.Gaussian(0,math.inf)
        self.assertAlmostEqual(Ninf.mu,0)
        self.assertAlmostEqual(Ninf.sigma,math.inf)
        N00 = ttt.Gaussian(mu=0,sigma=0)
        self.assertAlmostEqual(N00.mu,0)
        self.assertAlmostEqual(N00.sigma,0)
    def test_ppf(self):
        self.assertAlmostEqual(ttt.ppf(0.3,ttt.N01.mu, ttt.N01.sigma),-0.52440044)
        N23 = ttt.Gaussian(2.,3.)
        self.assertAlmostEqual(ttt.ppf(0.3,N23.mu, N23.sigma),0.42679866)
    def test_cdf(self):
        self.assertAlmostEqual(ttt.cdf(0.3,ttt.N01.mu,ttt.N01.sigma),0.617911409)
        N23 = ttt.Gaussian(2.,3.)
        self.assertAlmostEqual(ttt.cdf(0.3,N23.mu,N23.sigma),0.28547031)
    def test_pdf(self):    
        self.assertAlmostEqual(ttt.pdf(0.3,ttt.N01.mu,ttt.N01.sigma),0.38138781)
        N23 = ttt.Gaussian(2.,3.)
        self.assertAlmostEqual(ttt.pdf(0.3,N23.mu,N23.sigma),0.11325579)
    def test_compute_margin(self):
        self.assertAlmostEqual(ttt.compute_margin(0.25,math.sqrt(2)*25.0/6),1.8776005988)
        self.assertAlmostEqual(ttt.compute_margin(0.25,math.sqrt(3)*25.0/6),2.29958170)
        self.assertAlmostEqual(ttt.compute_margin(0.0,math.sqrt(3)*25.0/6),2.7134875810435737e-07)
        self.assertAlmostEqual(ttt.compute_margin(1.0,math.sqrt(3)*25.0/6),math.inf)
    def test_trunc(self):
        mu, sigma = ttt.trunc(*ttt.Gaussian(0,1),0.,False)
        self.assertAlmostEqual((mu,sigma) ,(0.7978845368663289,0.6028103066716792) )
        mu, sigma = ttt.trunc(*ttt.Gaussian(0.,math.sqrt(2)*(25/6) ),1.8776005988,True)
        self.assertAlmostEqual(mu,0.0) 
        self.assertAlmostEqual(sigma,1.07670, places=4)
        mu, sigma = ttt.trunc(*ttt.Gaussian(12.,math.sqrt(2)*(25/6)),1.8776005988,True)
        self.assertAlmostEqual(mu,0.3900999, places=5) 
        self.assertAlmostEqual(sigma,1.034401, places=5)
    def gaussian(self):
        N, M = ttt.Gaussian(25.0, 25.0/3), ttt.Gaussian(0.0, 1.0)
        mu, sigma = M/N
        self.assertAlmostEqual(mu,-0.365, places=3) 
        self.assertAlmostEqual(sigma, 1.007, places=3) 
        mu, sigma = N*M
        self.assertAlmostEqual(mu,0.355, places=3) 
        self.assertAlmostEqual(sigma,0.993, places=3) 
        mu, sigma = N+M
        self.assertAlmostEqual(mu,25.000, places=3) 
        self.assertAlmostEqual(sigma,8.393, places=3) 
        mu, sigma = N - ttt.Gaussian(1.0, 1.0)
        self.assertAlmostEqual(mu,24.000, places=3) 
        self.assertAlmostEqual(sigma,8.393, places=3) 
    def test_1vs1(self):
        ta = [ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]
        tb = [ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]
        g = ttt.Game([ta,tb],[1,0], 0.0)
        [a], [b] = g.posteriors
        self.assertAlmostEqual(a.mu,20.79477925612302,4)
        self.assertAlmostEqual(b.mu,29.20522074387697,4)
        self.assertAlmostEqual(a.sigma,7.194481422570443 ,places=4)
        
        g = ttt.Game([[ttt.Rating(29.,1.,25.0/6)] ,[ttt.Rating(25.0,25.0/3,25.0/6)]], [1,0])
        [a], [b] = g.posteriors
        self.assertAlmostEqual(a.mu,28.896, places=2)
        self.assertAlmostEqual(a.sigma,0.996, places=2)
        self.assertAlmostEqual(b.mu,32.189, places=2)
        self.assertAlmostEqual(b.sigma,6.062, places=2)
    def test_1vs1vs1(self):
        [a], [b], [c] = ttt.Game([[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]], [1,0,2]).posteriors
        self.assertAlmostEqual(a.mu,25.000000,5)
        self.assertAlmostEqual(a.sigma,6.238469796,5)
        self.assertAlmostEqual(b.mu,31.3113582213,5)
        self.assertAlmostEqual(b.sigma,6.69881865,5)
        self.assertAlmostEqual(c.mu,18.6886417787,5)
    
        [a], [b], [c] = ttt.Game([[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]], [1,0,2],0.5).posteriors
        self.assertAlmostEqual(a.mu,25.000,3)
        self.assertAlmostEqual(a.sigma,6.093,3)
        self.assertAlmostEqual(b.mu,33.379,3)
        self.assertAlmostEqual(b.sigma,6.484,3)
        self.assertAlmostEqual(c.mu,16.621,3)
    def test_1vs1_draw(self):
        [a], [b] = ttt.Game([[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]], [0,0], 0.25).posteriors
        self.assertAlmostEqual(a.mu,25.000,2)
        self.assertAlmostEqual(a.sigma,6.469,2)
        self.assertAlmostEqual(b.mu,25.000,2)
        self.assertAlmostEqual(b.sigma,6.469,2)
        
        ta = [ttt.Rating(25.,3.,25.0/6,25.0/300)]
        tb = [ttt.Rating(29.,2.,25.0/6,25.0/300)]
        [a], [b] = ttt.Game([ta,tb], [0,0], 0.25).posteriors
        self.assertAlmostEqual(a.mu,25.736,2)
        self.assertAlmostEqual(a.sigma,2.710,2)
        self.assertAlmostEqual(b.mu,28.672,2)
        self.assertAlmostEqual(b.sigma,1.916,2)
        
        [b], [a] = ttt.Game([tb,ta], [0,0], 0.25).posteriors
        self.assertAlmostEqual(a.mu,25.736,2)
        self.assertAlmostEqual(a.sigma,2.710,2)
        self.assertAlmostEqual(b.mu,28.672,2)
        self.assertAlmostEqual(b.sigma,1.916,2)
    def test_1vs1vs1_draw(self):
        [a], [b], [c] = ttt.Game([[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)],[ttt.Rating(25.0,25.0/3,25.0/6,25.0/300)]], [0,0,0],0.25).posteriors
        self.assertAlmostEqual(a.mu,25.000,3)
        self.assertAlmostEqual(a.sigma,5.729,3)
        self.assertAlmostEqual(b.mu,25.000,3)
        self.assertAlmostEqual(b.sigma,5.707,3)

        ta = [ttt.Rating(25.,3.,25.0/6,25.0/300)]
        tb = [ttt.Rating(25.,3.,25.0/6,25.0/300)]
        tc = [ttt.Rating(29.,2.,25.0/6,25.0/300)]
        [a], [b], [c] = ttt.Game([ta,tb,tc], [0,0,0],0.25).posteriors
        self.assertAlmostEqual(a.mu,25.489,3)
        self.assertAlmostEqual(a.sigma,2.638,3)
        self.assertAlmostEqual(b.mu,25.511,3)
        self.assertAlmostEqual(b.sigma,2.629,3)
        self.assertAlmostEqual(c.mu,28.556,3)
        self.assertAlmostEqual(c.sigma,1.886,3)
    def test_NvsN_Draw(self):
        ta = [ttt.Rating(15.,1.,25.0/6,25.0/300),ttt.Rating(15.,1.,25.0/6,25.0/300)]
        tb = [ttt.Rating(30.,2.,25.0/6,25.0/300)]
        [a,b], [c] = ttt.Game([ta,tb], [0,0], 0.25).posteriors
        self.assertAlmostEqual(a.mu,15.000,3)
        self.assertAlmostEqual(a.sigma,0.9916,3)
        self.assertAlmostEqual(b.mu,15.000,3)
        self.assertAlmostEqual(b.sigma,0.9916,3)
        self.assertAlmostEqual(c.mu,30.000,3)
        self.assertAlmostEqual(c.sigma,1.9320,3)
    def test_NvsNvsN_mixt(self):
        ta = [ttt.Rating(12.,3.,25.0/6,25.0/300)
             ,ttt.Rating(18.,3.,25.0/6,25.0/300)]
        tb = [ttt.Rating(30.,3.,25.0/6,25.0/300)]
        tc = [ttt.Rating(14.,3.,25.0/6,25.0/300)
             ,ttt.Rating(16.,3.,25.0/6,25.0/300)]
        [a,b], [c], [d,e]  = ttt.Game([ta,tb, tc], [0,1,1], 0.25).posteriors
        self.assertAlmostEqual(a.mu,13.051,3)
        self.assertAlmostEqual(a.sigma,2.864,3)
        self.assertAlmostEqual(b.mu,19.051,3)
        self.assertAlmostEqual(b.sigma,2.864,3)
        self.assertAlmostEqual(c.mu,29.292,3)
        self.assertAlmostEqual(c.sigma,2.764,3)
        self.assertAlmostEqual(d.mu,13.658,3)
        self.assertAlmostEqual(d.sigma,2.813,3)
        self.assertAlmostEqual(e.mu,15.658,3)
        self.assertAlmostEqual(e.sigma,2.813,3)
    def test_evidence_1vs1(self):
        ta = [ttt.Rating(25.,1e-7,25.0/6,25.0/300)]
        tb = [ttt.Rating(25.,1e-7,25.0/6,25.0/300)]
        g = ttt.Game([ta,tb], [0,0], 0.25)
        self.assertAlmostEqual(g.evidence,0.25,3)
        g = ttt.Game([ta,tb], [0,1], 0.25)
        self.assertAlmostEqual(g.evidence,0.375,3)
    def test_1vs1vs1_margin_0(self):
        ta = [ttt.Rating(25.,1e-7,25.0/6,25.0/300)]
        tb = [ttt.Rating(25.,1e-7,25.0/6,25.0/300)]
        tc = [ttt.Rating(25.,1e-7,25.0/6,25.0/300)]
        
        g_abc = ttt.Game([ta,tb,tc], [1,2,3], 0.)
        g_acb = ttt.Game([ta,tb,tc], [1,3,2], 0.)
        g_bac = ttt.Game([ta,tb,tc], [2,1,3], 0.)
        g_bca = ttt.Game([ta,tb,tc], [3,1,2], 0.)
        g_cab = ttt.Game([ta,tb,tc], [2,3,1], 0.)
        g_cba = ttt.Game([ta,tb,tc], [3,2,1], 0.)
        
        proba = 0
        proba += g_abc.evidence
        proba += g_acb.evidence
        proba += g_bac.evidence
        proba += g_bca.evidence
        proba += g_cab.evidence
        proba += g_cba.evidence
        
        print("Corregir la evidencia multiequipos para que sume 1")
        self.assertAlmostEqual(proba, 1.49999991)
    def test_forget(self):
        gamma = 0.15*25.0/3
        N = ttt.Gaussian(25.,1e-7)
        _, sigma = N.forget(gamma,5)
        self.assertAlmostEqual(sigma, math.sqrt(5*gamma**2))
        _, sigma = N.forget(gamma,1)
        self.assertAlmostEqual(sigma, math.sqrt(1*gamma**2))
    def test_one_event_each(self):
        agents = dict()
        for k in ["a", "b", "c", "d", "e", "f"]:
            agents[k] = ttt.Agent(ttt.Rating(25., 25.0/3, 25.0/6, 25.0/300 ) , ttt.Ninf, -ttt.inf)
        b = ttt.Batch(composition=[ [["a"],["b"]], [["c"],["d"]] , [["e"],["f"]] ], results= [[0,1],[1,0],[0,1]], time = 0, agents=agents)
        post = b.posteriors()
        self.assertAlmostEqual(post["a"].mu,29.205,3)
        self.assertAlmostEqual(post["a"].sigma,7.194,3)
        
        self.assertAlmostEqual(post["b"].mu,20.795,3)
        self.assertAlmostEqual(post["b"].sigma,7.194,3)
        self.assertAlmostEqual(post["c"].mu,20.795,3)
        self.assertAlmostEqual(post["c"].sigma,7.194,3)
        self.assertEqual(b.convergence(),1)
    def test_batch_same_strength(self):
        agents = dict()
        for k in ["a", "b", "c", "d", "e", "f"]:
            agents[k] = ttt.Agent(ttt.Rating(25., 25.0/3, 25.0/6, 25.0/300 ) , ttt.Ninf, -ttt.inf)
        b = ttt.Batch([ [["a"],["b"]], [["a"],["c"]] , [["b"],["c"]] ], [[0,1],[1,0],[0,1]], 2, agents)
        post = b.posteriors()
        self.assertAlmostEqual(post["a"].mu,24.96097,3)
        self.assertAlmostEqual(post["a"].sigma,6.299,3)
        self.assertAlmostEqual(post["b"].mu,27.09559,3)
        self.assertAlmostEqual(post["b"].sigma,6.01033,3)
        self.assertAlmostEqual(post["c"].mu,24.88968,3)
        self.assertAlmostEqual(post["c"].sigma,5.86631,3)
        self.assertEqual(b.convergence()>0, True)    
        post = b.posteriors()
        self.assertAlmostEqual(post["a"].mu,25.000,3)
        self.assertAlmostEqual(post["a"].sigma,5.419,3)
        self.assertAlmostEqual(post["b"].mu,25.000,3)
        self.assertAlmostEqual(post["b"].sigma,5.419,3)
        self.assertAlmostEqual(post["c"].mu,25.000,3)
        self.assertAlmostEqual(post["c"].sigma,5.419,3)
if False:
    def test_history_init(self):
        events = [ [["a"],["b"]], [["a"],["c"]] , [["b"],["c"]] ]
        results = [[0,1],[1,0],[0,1]]
        h = ttt.History(events, results, [1,2,3])

        self.assertEqual(not ttt.gr_tuple(h.batches[1].max_step, 1e-6) and  not ttt.gr_tuple(h.batches[1].max_step, 1e-6), True)
        p0 = h.batches[0].posteriors()
        self.assertAlmostEqual(p0["a"].mu,29.205,3)
        self.assertAlmostEqual(p0["a"].sigma,7.19448,3)
        observed = h.batches[1].prior_forward["a"].N.sigma 
        expected = math.sqrt((ttt.GAMMA*1)**2 +  h.batches[0].posterior("a").sigma**2)
        self.assertAlmostEqual(observed, expected)
        observed = h.batches[1].posterior("a")
        g = ttt.Game([[h.batches[1].prior_forward["a"]],[h.batches[1].prior_forward["c"]]],[1,0])
        [expected], [c] = g.posteriors
        self.assertAlmostEqual(observed.mu, expected.mu, 3)
        self.assertAlmostEqual(observed.sigma, expected.sigma, 3)
    def test_trueSkill_Through_Time(self):
        events = [ [["a"],["b"]], [["a"],["c"]] , [["b"],["c"]] ]
        results = [[0,1],[1,0],[0,1]]
        h = ttt.History(events, results, [1,2,3])
        h.batches[0].posteriors()
        step , i = h.convergence()
        self.assertAlmostEqual(h.batches[0].posterior("a").mu,25.0002673,5)
        self.assertAlmostEqual(h.batches[0].posterior("a").sigma,5.41950697,5)
        self.assertAlmostEqual(h.batches[0].posterior("b").mu,24.9986633,5)
        self.assertAlmostEqual(h.batches[0].posterior("b").sigma,5.41968377,5)
        self.assertAlmostEqual(h.batches[2].posterior("b").mu,25.0029304,5)
        self.assertAlmostEqual(h.batches[2].posterior("b").sigma,5.42076739,5)
    def test_one_batch_history(self):
        composition = [ [['aj'],['bj']],[['bj'],['cj']], [['cj'],['aj']] ]
        results = [[0,1],[0,1],[0,1]]
        bache = [1,1,1]
        h1 = ttt.History(composition,results, bache)
        self.assertAlmostEqual(h1.batches[0].posterior("aj").mu,22.904,2)
        self.assertAlmostEqual(h1.batches[0].posterior("aj").sigma,6.010,2)
        self.assertAlmostEqual(h1.batches[0].posterior("cj").mu,25.110,2)
        self.assertAlmostEqual(h1.batches[0].posterior("cj").sigma,5.866,2)
        step , i = h1.convergence()
        self.assertAlmostEqual(h1.batches[0].posterior("aj").mu,25.000,2)
        self.assertAlmostEqual(h1.batches[0].posterior("aj").sigma,5.419,2)
        self.assertAlmostEqual(h1.batches[0].posterior("cj").mu,25.000,2)
        self.assertAlmostEqual(h1.batches[0].posterior("cj").sigma,5.419,2)
    
        h2 = ttt.History(composition,results, [1,2,3])
        self.assertAlmostEqual(h2.batches[2].posterior("aj").mu,22.904,2)
        self.assertAlmostEqual(h2.batches[2].posterior("aj").sigma,6.012,2)
        self.assertAlmostEqual(h2.batches[2].posterior("cj").mu,25.110,2)
        self.assertAlmostEqual(h2.batches[2].posterior("cj").sigma,5.867,2)
        step2 , i2 = h2.convergence()
        self.assertAlmostEqual(h2.batches[2].posterior("aj").mu,24.997,2)
        self.assertAlmostEqual(h2.batches[2].posterior("aj").sigma,5.421,2)
        self.assertAlmostEqual(h2.batches[2].posterior("cj").mu,25.000,2)
        self.assertAlmostEqual(h2.batches[2].posterior("cj").sigma,5.420,2)
    def test_learning_curve(self):
        composition = [ [['aj'],['bj']],[['bj'],['cj']], [['cj'],['aj']] ]
        results = [[0,1],[0,1],[0,1]]    
        h = ttt.History(composition,results, [5,6,7])
        h.convergence()
        lc = h.learning_curves()
        for a in lc:
            self.assertEqual(all(lc[a][i][0] < lc[a][i+1][0] for i in range(len(lc[a])-1)), True)
        self.assertEqual(lc["aj"][0][0],5)
        self.assertEqual(lc["aj"][-1][0],7)
        self.assertAlmostEqual(lc["aj"][-1][1].mu,24.997,2)
        self.assertAlmostEqual(lc["aj"][-1][1].sigma,5.421,2)
        self.assertAlmostEqual(lc["cj"][-1][1].mu,25.000,2)
        self.assertAlmostEqual(lc["cj"][-1][1].sigma,5.420,2)
    
        
        
        
if __name__ == "__main__":
    unittest.main()


