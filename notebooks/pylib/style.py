import matplotlib.pyplot as plt
import numpy as np
from .statistics import chi2_ndf_prob
from scipy import stats

def my_style(title=None, xtitle=None, ytitle=None, gridstyle='--', legend=False, xlim=None, ylim=None, minorgrid=True):
    """Стиль для адекватного простого отображения картинок"""
    plt.title(title)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid(which='major', linestyle=gridstyle, alpha=0.5)
    if minorgrid:
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', alpha=0.3)
    plt.xlim(xlim)
    plt.ylim(ylim)
    if legend:
        plt.legend(frameon=True)
    plt.tight_layout()
    
def hep_histo(data, bins=10, range=None, label=None, roll_bins=0, alpha=1, color=None):
    """Гистограмма, наиболее похожая на то, что нужно в ФЭЧ"""
    histData, histBins = np.histogram(data, range=range, bins=bins)
    histData = np.roll(histData, roll_bins)
    plt.errorbar( np.convolve(histBins, np.ones(2, dtype=int), 'valid')/2, histData, yerr=np.sqrt(histData), fmt='.', label=label, alpha=alpha, color=color)
    
def plot_fit(data, cost, minuit, bins, hist_range, fit_range=None, errors=True, label=None, alpha=0.7, 
             title=None, xtitle=None, ytitle=None, gridstyle='--', xlim=None, 
             ylim=(0, None), description=True, fill_errors=False, bbox_color='ivory', fit_color=None, data_color=None, fit_func=None):
    """Нарисовать результат фита"""
    if fit_range is None:
        fit_range = hist_range
    fig, ax = plt.subplots()
    par_vals = minuit.values
    xcoord = np.linspace(fit_range[0], fit_range[1], 200)
#     ax.plot(xcoord, pdf(xcoord, *par_vals, fit_range)*(hist_range[1]-hist_range[0])/bins, alpha=alpha, label='Fit result')
    N = minuit.values['n_sig'] if 'n_bkg' not in minuit.parameters else minuit.values['n_sig'] + minuit.values['n_bkg']
    ax.plot(xcoord, cost.scaled_pdf(xcoord, *par_vals)[1]*(hist_range[1] - hist_range[0])/bins,
           alpha=alpha, label='Fit result', color=fit_color, zorder=3)
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
                s += f'{var} = {val:1.3f}\n'
            else:
                s += f'{var} = {val:1.3f}$\\pm${err:3.3f}\n'
        if fit_func is not None:
            n_bkg, n_bkg_err = fit_func.get_nbkg(minuit)
            if n_bkg is not None:
                s += f'n_bkg = {n_bkg:1.3f}$\\pm${n_bkg_err:3.3f}\n'
#         if ('y0' in minuit.parameters) and not( (minuit.values['y0'] == 0) and (minuit.values['dy'] == 0) ):
#             width = (fit_range[1] - fit_range[0])
#             n_bkg = width*(2*minuit.values['y0'] + minuit.values['dy'])/2
#             n_bkg_err = width*np.sqrt(2*minuit.errors['y0']**2 + minuit.errors['dy']**2)/2
#             s += f'n_bkg = {n_bkg:1.3f}$\\pm${n_bkg_err:3.3f}\n'
        props = dict(boxstyle='square', facecolor=bbox_color, alpha=0.5)
        ax.text(0.05, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
    legend = (label is not None)
    my_style(title, xtitle, ytitle, gridstyle, legend, xlim, ylim)