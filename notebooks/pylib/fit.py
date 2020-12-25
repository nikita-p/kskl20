import numba as nb
import numpy as np
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL, BinnedNLL, ExtendedUnbinnedNLL, ExtendedBinnedNLL, LeastSquares
from scipy.integrate import quad

# kwd = {"parallel": False, "fastmath": True}

@nb.njit(parallel=False, fastmath=True)
def cruijff(x, m, sL, sR, aL, aR):
    denom = 2*np.where(x<m, (sL**2 + aL*(x-m)**2), (sR**2 + aR*(x-m)**2) )
    return np.exp(-(x-m)**2/denom)

def cruijff_norm(x, m, sL, sR, aL, aR, fit_range):
    xmin, xmax = fit_range
    I = quad(cruijff, xmin, xmax, args=(m, sL, sR, aL, aR))[0]
    return cruijff(x, m, sL, sR, aL, aR)/I

@nb.njit(parallel=False, fastmath=True)
def linear_norm(x, k, fit_range):
    xmin, xmax = fit_range
    w = xmax - xmin
    f = (1/w)*((k*(x-xmin)+1)/((k*w)/2+1))
    return f #np.where(f<0, 0, f)

def full_pdf(x, m, sL, sR, aL, aR, k, f, **kwargs):
    return f*cruijff_norm(x, m, sL, sR, aL, aR, kwargs['fit_range']) + (1-f)*linear_norm(x, k, kwargs['fit_range'])
    
def plot_bkg(m, bins):
    xs = np.linspace(fit_range[0], fit_range[1], 10)
    plt.fill_between(xs, linear_norm(xs,m.values['k'])*m.values['n']*\
                     (1 -m.values['f'])*(hist_range[1]-hist_range[0])/bins, alpha=0.3, color='tomato', label='Background' )
    
def fit_data(data, fit_range, params, limits, mc=False):
    if mc:
        limits = limits.copy()
        limits[-2] = (0, 0)
        limits[-1] = (1, 1)
    xmin, xmax = fit_range
    data = data[(data>xmin)&(data<xmax)]
    m = Minuit(ExtendedUnbinnedNLL(data, lambda x, n, m, sL, sR, aL, aR, k, f: 
                               (n, n * full_pdf(x, m, sL, sR, aL, aR, k, f, fit_range=fit_range))), **params)
    m.limits=limits
    m.errordef=Minuit.LIKELIHOOD
    return m   