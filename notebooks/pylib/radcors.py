import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
from scipy.integrate import quad
from .regeff import RegEff

class RadCor:
    """
    Класс для вычисления радпоправок
    """
    alpha = 7.297e-3
    me = 0.511 #MeV
    data = None
    x, y = None, None
    radcors = None

    def __init__(self, energies, cross_sections, e_threshold=497.6):
        """
        energies - энергии пучка, в МэВ; cross_sections - сечения, в нб;
        e_theshold - пороговая энергия пучка реакции, в МэВ
        """
        data = np.array([energies, cross_sections]).T 
        self.data = data[data[:,0].argsort()]
        spline = make_interp_spline(self.data[:, 0], self.data[:, 1], k=2)
        self.x = np.linspace(e_threshold-10, max(energies), 10000)
        self.y = spline(self.x)
        self.y = np.where(self.x<=e_threshold, 0, self.y)
    def L(self, s):
        me = self.me
        return np.log(s/(me**2))
    def beta(self, s):
        a = self.alpha
        p = np.pi
        return (2*a/p)*(self.L(s) - 1)
    def F(self, x, s):
        a = self.alpha
        b = self.beta(s)
        p = np.pi
        L = self.L(s)
        m = self.me
        E = np.sqrt(s)/4

        s1 = (a/p)*( (p**2)/3 - 1/2 ) + 3*b/4
        s2 = (-(b**2)/24)*(L/3 + 2*(p**2) - 37/4 )
        s3 = -b*(1-x/2)
        s4 = 4*(2-x)*np.log(1/x)
        s5 = (1/x)*(1+3*((1-x)**2))*np.log(1/(1-x))
        s6 = - 6 + x

        s7 = 0 if x<(2*m/E) else (1/(6*x))*((x - 2*m/E)**b)*\
            ((np.log(s*(x**2)/(m**2)) - 5/3)**2)*\
            (2 - 2*x + x**2 + (b/3)*(np.log(s*(x**2)/(m**2)) - 5/3))
        s8 = 0 if x<(2*m/E) else ((L**2)/2)*((2/3)*((1-(1-x)**3)/(1-x)) -\
            (2-x)*np.log(1/(1-x)) + x/2 )


        result = b*(x**(b-1))*( 1 + s1 + s2 ) + s3 + \
        (1/8)*(b**2)*(s4 + s5 + s6) + \
        ((a/p)**2)*(s7 + s8)
        return result
    def F_Integral(self, e_beam, params, Xmax=1, use_efficiency=True):
        s = 4*(e_beam**2)
        sx = 4*(self.x**2)
        if not( np.all(np.diff(sx) > 0) ):
            raise Exception('Problem')
        regeff = lambda x: RegEff.sigFunc(np.sqrt(s/4)*x*1e-3, *params) if use_efficiency else lambda x: 1
        return quad( lambda x: self.F(x, s)*np.interp(s*(1-x), sx, self.y)*regeff(x),
                    0., Xmax, points=[0, 1], limit=50000, epsrel=0.0001)
    def F_Radcor(self, e_beam, params, Xmax=1, use_efficiency=True):
        integral = self.F_Integral(e_beam, params, Xmax, use_efficiency)
        return ( integral[0]/np.interp(e_beam, self.x, self.y), integral[1]/np.interp(e_beam, self.x, self.y) )
#     def Calc(self, e_beams=None, rounds=1):
#         if e_beams is None:
#             e_beams = self.data[:,0]
#         if self.radcors is None:
#             self.radcors = pd.Series(np.ones(e_beams.size), index=e_beams)
#         for e_beam in e_beams:
#             rc, drc = self.F_Radcor(e_beam)
#             self.radcors