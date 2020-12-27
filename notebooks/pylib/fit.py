import numba as nb
import numpy as np
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL, BinnedNLL, ExtendedUnbinnedNLL, ExtendedBinnedNLL, LeastSquares
from scipy.integrate import quad

def pdf(x, n_sig, n_bkg, m, sL, sR, aL, aR, k, fit_range):
    return n_sig * cruijff_norm(x, m, sL, sR, aL, aR, fit_range) + \
             n_bkg * linear_norm(x, k, fit_range)

def sig_pdf(x, n_sig, m, sL, sR, aL, aR, fit_range):
    return n_sig * cruijff_norm(x, m, sL, sR, aL, aR, fit_range)

def fitter(data, fit_range, params, mc=False):
    params = params.copy()
    xmin, xmax = fit_range
    data = data[(data>xmin)&(data<xmax)]
    if mc:
        cost_function = ExtendedUnbinnedNLL(data, lambda x, n_sig, m, sL, sR, aL, aR: 
            (n_sig, sig_pdf(x, n_sig, m, sL, sR, aL, aR, fit_range)))
        del params['n_bkg'], params['k']
    else:
        cost_function = ExtendedUnbinnedNLL(data, lambda x, n_sig, n_bkg, m, sL, sR, aL, aR, k: 
            (n_sig + n_bkg, pdf(x, n_sig, n_bkg, m, sL, sR, aL, aR, k, fit_range)))
    parameters = {k : params[k][0] for k in params}
    m = Minuit(cost_function, **parameters)
    for par in m.parameters:
        m.limits[par] = params[par][1]
    m.errordef=Minuit.LIKELIHOOD
    return m


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

# def full_pdf(x, m, sL, sR, aL, aR, k, f, **kwargs):
#     return f*cruijff_norm(x, m, sL, sR, aL, aR, kwargs['fit_range']) + (1-f)*linear_norm(x, k, kwargs['fit_range'])
       
# def fit_data(data, fit_range, params, limits, mc=False):
#     if mc:
#         limits = limits.copy()
#         limits[-2] = (0, 0)
#         limits[-1] = (1, 1)
#     xmin, xmax = fit_range
#     data = data[(data>xmin)&(data<xmax)]
#     m = Minuit(ExtendedUnbinnedNLL(data, lambda x, n, m, sL, sR, aL, aR, k, f: 
#                                (n, n * full_pdf(x, m, sL, sR, aL, aR, k, f, fit_range=fit_range))), **params)
#     m.limits=limits
#     m.errordef=Minuit.LIKELIHOOD
#     return m   