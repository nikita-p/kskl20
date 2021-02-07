import numba as nb
import numpy as np
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL, ExtendedUnbinnedNLL, NormalConstraint 
from scipy.integrate import quad
from scipy.stats import poisson

def sig_pdf(x, m, sL, sR, aL, aR, fit_range):
    return cruijff_norm(x, m, sL, sR, aL, aR, fit_range)

def pdf(x, n_sig, m, sL, sR, aL, aR, y0, dy, fit_range):
    return n_sig*cruijff_norm(x, m, sL, sR, aL, aR, fit_range) + linear(x, y0, dy, fit_range)

def fitter(data, fit_range, params, mc=False):
    params = params.copy()
    xmin, xmax = fit_range
    width = xmax - xmin
    data = data[(data>=xmin)&(data<=xmax)]
#     print(len(data))
    if mc:
        cost_function0 = ExtendedUnbinnedNLL(data, lambda x, n_sig, m, sL, sR, aL, aR: 
            (n_sig, n_sig*sig_pdf(x, m, sL, sR, aL, aR, fit_range)))
        cost_function = cost_function0
        del params['y0'], params['dy'], 
    else:
        cost_function0 = ExtendedUnbinnedNLL(data, lambda x, n_sig, m, sL, sR, aL, aR, y0, dy: ( n_sig + width*(2*y0+dy)/2, pdf(x, n_sig, m, sL, sR, aL, aR, y0, dy, fit_range)))
        cost_function = cost_function0 + NormalConstraint('sL', params['sL'][0], params['sL'][1]) + NormalConstraint('sR', params['sR'][0], params['sR'][1]) + \
                NormalConstraint('aL', params['aL'][0], params['aL'][1]) + NormalConstraint('aR', params['aR'][0], params['aR'][1]) + NormalConstraint('m', params['m'][0], params['m'][1])
    parameters = {k : params[k][0] for k in params}
    m = Minuit(cost_function, **parameters)
    for par in m.parameters:
        m.limits[par] = params[par][1]
#     m.errordef= Minuit.LIKELIHOOD
    return (m, cost_function0)


@nb.njit(parallel=False, fastmath=True)
def cruijff(x, m, sL, sR, aL, aR):
    denom = 2*np.where(x<m, (sL**2 + aL*(x-m)**2), (sR**2 + aR*(x-m)**2) )
    return np.exp(-(x-m)**2/denom)

def cruijff_norm(x, m, sL, sR, aL, aR, fit_range):
    xmin, xmax = fit_range
#     try:
    I = quad(cruijff, xmin, xmax, args=(m, sL, sR, aL, aR))[0]
    return cruijff(x, m, sL, sR, aL, aR)/I
#     except:
#         return np.ones_like(x)/(xmax-xmin)

@nb.njit(parallel=False, fastmath=True)
def linear(x, y0, dy, fit_range):
    xmin, xmax = fit_range
    y1 = y0 + dy
    return (y1 - y0)*(x - xmin)/(xmax - xmin) + y0

@nb.njit(parallel=False, fastmath=True)
def linear_norm(x, k, fit_range):
    xmin, xmax = fit_range
    w = xmax - xmin
    f = (1/w)*((k*(x-xmin)+1)/((k*w)/2+1))
    return f #np.where(f<0, 0, f)