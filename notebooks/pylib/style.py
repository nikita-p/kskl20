import matplotlib.pyplot as plt
import numpy as np

def my_style(title='', xtitle='', ytitle='', gridstyle=':', legend=False):
    """Стиль для адекватного простого отображения картинок"""
    plt.grid(linestyle=gridstyle)
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    if legend:
        plt.legend(frameon=True)
    
def hep_histo(data, bins=10, range=None, label=None):
    """Гистограмма, наиболее похожая на то, что нужно в ФЭЧ"""
    histData, histBins = np.histogram(data, range=range, bins=bins)
    plt.errorbar( np.convolve(histBins, np.ones(2, dtype=int), 'valid')/2, histData, yerr=np.sqrt(histData), fmt='.', label=label)