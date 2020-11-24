import matplotlib.pyplot as plt
import numpy as np

def my_style(title=None, xtitle=None, ytitle=None, gridstyle='--', legend=False, xlim=None, ylim=None):
    """Стиль для адекватного простого отображения картинок"""
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(which='major', linestyle=gridstyle)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', alpha=0.5)
    plt.xlim(xlim)
    plt.ylim(ylim)
    if legend:
        plt.legend(frameon=True)
    plt.tight_layout()
    
def hep_histo(data, bins=10, range=None, label=None, roll_bins=0):
    """Гистограмма, наиболее похожая на то, что нужно в ФЭЧ"""
    histData, histBins = np.histogram(data, range=range, bins=bins)
    histData = np.roll(histData, roll_bins)
    plt.errorbar( np.convolve(histBins, np.ones(2, dtype=int), 'valid')/2, histData, yerr=np.sqrt(histData), fmt='.', label=label)
    
def plot_fit(data, pdf, minuit, bins, range, errors=True, label=None, alpha=0.7, 
             title=None, xtitle=None, ytitle=None, gridstyle='--', xlim=None, 
             ylim=(0, None), description=True):
    """Нарисовать результат фита"""
    fig, ax = plt.subplots()
    par_vals = minuit.values.values()
    xcoord = np.linspace(range[0], range[1], 200)
    ax.plot(xcoord, pdf(xcoord, *par_vals[1:])*par_vals[0]*(range[1]-range[0])/bins, alpha=alpha, label='Fit result')
    if errors:
        hep_histo(data, bins, range, label)
    else:
        ax.hist(data, bins=bins, range=range, histtype='step', label=label)
    if description:
        s = ''
        for var in minuit.values:
            val, err = minuit.values[var], minuit.errors[var] 
            s += f'{var} = {val:1.3f}$\\pm${err:3.3f}\n'
        props = dict(boxstyle='square', facecolor='ivory', alpha=0.5)
        ax.text(0.05, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
    legend = (label is not None)
    my_style(title, xtitle, ytitle, gridstyle, legend, xlim, ylim)