import matplotlib.pyplot as plt
import numpy as np

def my_style(title='', xtitle='', ytitle='', gridstyle='--', legend=False):
    """Стиль для адекватного простого отображения картинок"""
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(which='major', linestyle=gridstyle)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.5)
    if legend:
        plt.legend(frameon=True)
    plt.tight_layout()
    
def hep_histo(data, bins=10, range=None, label=None):
    """Гистограмма, наиболее похожая на то, что нужно в ФЭЧ"""
    histData, histBins = np.histogram(data, range=range, bins=bins)
    plt.errorbar( np.convolve(histBins, np.ones(2, dtype=int), 'valid')/2, histData, yerr=np.sqrt(histData), fmt='.', label=label)