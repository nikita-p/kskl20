import numpy as np

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