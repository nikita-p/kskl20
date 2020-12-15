import numpy as np
from inspect import signature

def chi2_ndf(data1, data2, range, bins, weights1=None, weights2=None, roll_bins=0):
    """Проверяю две гистограммы на соответствие друг другу через хи-квадрат.
    data2, weights2 - относятся к MC и должны быть много больше data1"""
    d1Hist, d1Bins = np.histogram(data1, bins=bins, range=range, weights=weights1)
    d1Hist = np.roll(d1Hist, roll_bins)
    d2Hist, d2Bins = np.histogram(data2, bins=bins, range=range, weights=weights2)
    difference = d1Hist - d2Hist
    errDifference = np.sqrt(d1Hist)
    difference = difference[errDifference>0]
    errDifference = errDifference[errDifference>0]
    chi2 = np.sum(np.square(difference/errDifference))
    ndf = len(errDifference) - 1
    return (chi2, ndf)

def chi2_ndf_prob(data, pdf, fit_range, bins=50, **kwargs):
    """Проверить на соответствие гистрограмму и фит. Нулевые бины игнорируются
    """
    d_hist, d_bins = np.histogram(data, bins=bins, range=fit_range)
    d_errs = np.sqrt(d_hist)
    bins_centers = (d_bins[:-1] + d_bins[1:])/2
    d_hist, d_errs = np.ma.masked_array(d_hist, mask=(d_hist==0)), np.ma.masked_array(d_errs, mask=(d_hist==0))
    scale_factor = d_hist.sum()*((fit_range[1] - fit_range[0])/bins)
    d_hist, d_errs = d_hist/scale_factor, d_errs/scale_factor
    d_hist = d_hist - pdf(bins_centers, **kwargs)
    n_pars = len(signature(pdf).parameters) - 1 # x as -1
    return ( ((d_hist/d_errs)**2).sum(), (~d_hist.mask).sum() - n_pars - 1)