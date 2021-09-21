import matplotlib.pyplot as plt
import numpy as np
from .statistics import chi2_ndf_prob
from scipy import stats
import pyik.numpyext

def my_style(title=None, xtitle=None, ytitle=None, gridstyle='--', legend=False, xlim=None, ylim=None, minorgrid=True, grid_alpha: tuple = (0.5, 0.3)):
    """Стиль для адекватного простого отображения картинок"""
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(which='major', linestyle=gridstyle, alpha=grid_alpha[0])
    if minorgrid:
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', alpha=grid_alpha[1])
    plt.xlim(xlim)
    plt.ylim(ylim)
    if legend:
        plt.legend(frameon=True)
    plt.tight_layout()
    
def hep_histo(data, bins=10, range=None, label=None, roll_bins=0, alpha=1, color=None):
    """Гистограмма, наиболее похожая на то, что нужно в ФЭЧ"""
    histData, histBins = np.histogram(data, range=range, bins=bins)
    histData = np.roll(histData, roll_bins)
    yerr = np.nan_to_num(pyik.numpyext.poisson_uncertainty(histData))
    plt.errorbar( np.convolve(histBins, np.ones(2, dtype=int), 'valid')/2, histData, yerr=yerr, fmt='.', label=label, alpha=alpha, color=color)
    
def plot_fit(data, cost, minuit, bins, hist_range, fit_range=None, errors=True, label=None, alpha=0.7, lw=1,
             title=None, xtitle=None, ytitle=None, gridstyle='--', xlim=None,
             ylim=(0, None), description=True, fill_errors=False, plot_bkg=False, bbox_color='ivory', fit_color=None, data_color=None, fit_func=None,
             print_fixed_vals=True):
    """Нарисовать результат фита"""
    if fit_range is None:
        fit_range = hist_range
    fig, ax = plt.subplots()
    xcoord = np.linspace(fit_range[0], fit_range[1], 200)
    
    par_vals = np.array(minuit.values)
    if plot_bkg:
        par_vals_bkg = par_vals.copy()
        par_vals_bkg[0] = 0
        ax.plot(xcoord, cost.scaled_pdf(xcoord, *par_vals_bkg)[1]*(hist_range[1] - hist_range[0])/bins,
               alpha=alpha, label='Background', color=fit_color, zorder=3 ,lw=lw, ls='--')
    ax.plot(xcoord, cost.scaled_pdf(xcoord, *par_vals)[1]*(hist_range[1] - hist_range[0])/bins,
           alpha=alpha, label='Total fit', color=fit_color, zorder=3 ,lw=lw)
    if fill_errors:
        s1 = [i+j for i,j in zip(minuit.values, minuit.errors)]
        s2 = [i-j for i,j in zip(minuit.values, minuit.errors)]
        ax.fill_between(xcoord, cost.scaled_pdf(xcoord, *s2)[1]*(hist_range[1] - hist_range[0])/bins, cost.scaled_pdf(xcoord, *s1)[1]*(hist_range[1] - hist_range[0])/bins, alpha=0.3)
    if errors:
        hep_histo(data, bins, hist_range, label, color=data_color)
    else:
        ax.hist(data, bins=bins, range=hist_range, histtype='step', label=label, color=data_color)
    if description:
        s = ''
        values_dict = dict(zip(minuit.parameters, minuit.values))
        chi2, ndf = chi2_ndf_prob(data, cost, minuit, fit_range, int(bins*(fit_range[1]-fit_range[0])/(hist_range[1]-hist_range[0])))
        s += f'$\\chi^2$ / ndf = {chi2:.2f} / {ndf}\n'
        s += f'p-value: {1-stats.chi2.cdf(chi2, ndf):.2f}\n'
        for var, val, err, fixed in zip(minuit.parameters, minuit.values, minuit.errors, minuit.fixed):
            if fixed:
                if print_fixed_vals:
                    s += f'{var} = {val:1.3f}\n'
            else:
                s += f'{var} = {val:1.3f}$\\pm${err:3.3f}\n'
        props = dict(boxstyle='square', facecolor=bbox_color, alpha=0.8)
        ax.text(0.05, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
    legend = (label is not None)
    my_style(title, xtitle, ytitle, gridstyle, legend, xlim, ylim, grid_alpha=(0.3, 0.1))