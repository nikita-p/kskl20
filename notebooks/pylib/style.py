import matplotlib.pyplot as plt
import numpy as np
from .statistics import chi2_ndf_prob
from scipy import stats

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
    
def plot_fit(data, pdf, minuit, bins, hist_range, fit_range=None, errors=True, label=None, alpha=0.7, 
             title=None, xtitle=None, ytitle=None, gridstyle='--', xlim=None, 
             ylim=(0, None), description=True):
    """Нарисовать результат фита"""
    if fit_range is None:
        fit_range = hist_range
    fig, ax = plt.subplots()
    par_vals = minuit.values.values()
    xcoord = np.linspace(fit_range[0], fit_range[1], 200)
    ax.plot(xcoord, pdf(xcoord, *par_vals[1:])*par_vals[0]*(hist_range[1]-hist_range[0])/bins, alpha=alpha, label='Fit result')
    if errors:
        hep_histo(data, bins, hist_range, label)
    else:
        ax.hist(data, bins=bins, range=hist_range, histtype='step', label=label)
    if description:
        s = ''
        chi2, ndf = chi2_ndf_prob(data, pdf, fit_range, bins=bins, **minuit.values)
        s += f'$\\chi^2$ / ndf = {chi2:.2f} / {ndf}\n'
        s += f'p-value: {1-stats.chi2.cdf(chi2, ndf):.2f}\n'
        for var in minuit.fixed:
            val, err = minuit.values[var], minuit.errors[var] 
            if minuit.fixed[var]:
                s += f'{var} = {val:1.3f}\n'
            else:
                s += f'{var} = {val:1.3f}$\\pm${err:3.3f}\n'
        props = dict(boxstyle='square', facecolor='ivory', alpha=0.5)
        ax.text(0.05, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
    legend = (label is not None)
    my_style(title, xtitle, ytitle, gridstyle, legend, xlim, ylim)