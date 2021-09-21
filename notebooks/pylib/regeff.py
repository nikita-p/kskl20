from scipy.special import erfc, expit
from iminuit import Minuit
from iminuit.cost import LeastSquares
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import uproot
import re
from progressbar import progressbar
from .style import my_style
from .preprocess import read_tree
from scipy import stats
import warnings

class RegEff():
    def __init__(self, df_mc, data_file, dc_corr_file=None):
        self.df = df_mc[['emeas', 'x1', 'sim_energy', 'tth[0]', 'tth[1]']].sort_index().copy() if df_mc is not None else None
        file = list(map(lambda x: x.strip(), open(data_file).readlines()[1:])) if data_file is not None else None
        if self.df is not None:
            alldat = lambda x: uproot.open(x)['tr_ph'].arrays(filter_name=['simmom'], library='pd', cut='(simtype==22)&(simorig==0)').groupby('entry').sum().values.ravel()
            self.full_values = {float(re.findall(r'_(\d+\.?\d*)_', x)[0]) : alldat(x) for x in progressbar(file)}
            self.uniques = self.df.index.unique()
        else:
            self.full_values = None
            self.uniques = None
        self.histos = None
        self.fit_name = None
        self.fit_results = None
    def __variance(self, k, n):
        return (k+1)*(k+2)/(n+2)/(n+3) - (k+1)**2/(n+2)**2
#     def __chi2(self, mu, s, c, N, a):
#         xedges, points, errs = self.get_histo_by_name(self.fit_name)
#         return np.sum( np.square((points - RegEff.sigFunc(xedges, mu, s, c, N, a))/errs) )
    def __len__(self):
        return self.uniques.size
    def __getitem__(self, index):
        if index>=self.__len__() or index<0:
            raise ValueError(f'Wrong index: {index}')
        return self.df.loc[self.uniques[index]]
    def sigFunc(x, mu, s, c, N):
        return N*( 1 - expit((x-mu)/s) + c)
#         return N*(c + erfc((x-mu)/s))
    def index2energy(self, index):
        if self.uniques is None:
            return 0
        return self.uniques[index]
    def get_histogram_by_index(self, index, n_bins):
        df = self.__getitem__(index)
        fulls = self.full_values[self.index2energy(index)]
        hist_range = (0, np.max(self.full_values[self.uniques[index]]))
        data1, bins = np.histogram(df.sim_energy, bins=n_bins, range=hist_range)#, weights=df.dc_corr)
        data2, bins = np.histogram(fulls, bins=n_bins, range=hist_range)
        bins = (bins[1:] + bins[:-1])/2
        data = (data1+1)/(data2+2)
        data_errs = np.sqrt(self.__variance(data1, data2))
        #Проблема! Сейчас при подсчёте ошибок не используется неопределённость dc_corr_errs
#         ind = np.digitize(df.sim_energy, bins[1:], right=True)
#         err = (df.dc_corr**2 + df.dc_corr_err**2)
#         err.index = ind
#         data_errs = np.sqrt(err.groupby(err.index).agg('sum')).reindex(index=np.arange(n_bins)).fillna(0)/data2
#         print(data_errs)
        return (data, data_errs, bins)
    def fit_data(data, data_errs, bins, data_color=None, fit_color=None, bbox_color=None, mu0=0.02, s0=1/250, name=None):
        parameters = {
            'mu' : mu0,
            's' : s0,
            'c' : 0.004,
            'N' : 0.35,
        }
        parameters_options = {
            'mu' : ([0, 1], 0.01),
            's' : ([0,1], 1/250),
            'c' : ([0,1], 0.01),
            'N' : ([0,1], 0.05),
        }
        m = Minuit(LeastSquares(bins, data, data_errs, RegEff.sigFunc), **parameters)
#         for par in m.parameters:
#             m.limits[par], m.errors[par] = parameters_options[par]
        m.simplex().migrad().hesse().hesse()
        
        if not(m.accurate):
            warnings.warn('Minuit troubles')

        columns = []
        columns += m.parameters
        columns += ( tuple(map(lambda x: f'{x}_err', m.parameters)) + ('eff0', 'eff0_err') )
        fit_results = pd.DataFrame(columns=columns)
        
        eff0 = RegEff.sigFunc(0, *m.values)
        eff0_err = RegEff.sigFunc(0, *(np.array(m.values)+np.array(m.errors))) - eff0
        temp_ser = pd.Series(list(m.values) + list(m.errors) + [eff0, eff0_err], index=fit_results.columns, name=name)
        fit_results = fit_results.append(temp_ser)
        
            
        fig, ax = plt.subplots()
        xx = np.linspace(0, np.max(bins), 100)
        ax.errorbar(bins, data, yerr=data_errs, fmt='.', color=data_color)
        ax.plot(xx, RegEff.sigFunc(xx, *m.values), color=fit_color)
        my_style(title=(name if name is not None else 'Registration eff. vs rad. photon energy'), xlim=(0, np.max(bins)), ylim=(0, None), 
                xtitle='$E_{\\gamma}$, GeV', ytitle='$\\varepsilon_{reg}$', grid_alpha=(0.3, 0.1))
        values_dict = dict(zip(m.parameters, m.values))
        chi2, ndf = m.fval, len(bins)-len(m.parameters)-1
        s =  f'$\\chi^2$ / ndf = {chi2:.2f} / {ndf}\n'
        s += f'p-value: {1-stats.chi2.cdf(chi2, ndf):.2f}\n'
        for var, val, err, fixed in zip(m.parameters, m.values, m.errors, m.fixed):
            if fixed:
                s += f'{var} = {val:1.3f}\n'
            else:
                s += f'{var} = {val:1.3f}$\\pm${err:.4f}\n'
        props = dict(boxstyle='square', facecolor=bbox_color, alpha=0.5)
        ax.text(0.65, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
        return fit_results
    def fit(self, index, n_bins=100, data_color=None, fit_color=None, bbox_color=None, data=None, mu0=0.02, s0=1/250):
        if data is not None:
            data, data_errs, bins = data
        else:
            data, data_errs, bins = self.get_histogram_by_index(index, n_bins)
        parameters = {
            'mu' : mu0,
            's' : s0,
            'c' : 0.004,
            'N' : 0.35,
        }
        parameters_options = {
            'mu' : ([0, 1], 0.01),
            's' : ([0,1], 1/25),
            'c' : ([0,1], 0.01),
            'N' : ([0,1], 0.05),
        }
        m = Minuit(LeastSquares(bins, data, data_errs, RegEff.sigFunc), **parameters)
        for par in m.parameters:
            m.limits[par], m.errors[par] = parameters_options[par]
        m.migrad()
        
        if not(m.accurate):
            warnings.warn('Minuit troubles')

        if self.fit_results is None:
            columns = []
            columns += m.parameters
            columns += ( tuple(map(lambda x: f'{x}_err', m.parameters)) + ('eff0', 'eff0_err') )
            self.fit_results = pd.DataFrame(columns=columns)
        eff0 = RegEff.sigFunc(0, *m.values)
        eff0_err = RegEff.sigFunc(0, *(np.array(m.values)+np.array(m.errors))) - eff0
        temp_ser = pd.Series(list(m.values) + list(m.errors) + [eff0, eff0_err], index=self.fit_results.columns, name=self.index2energy(index))
        if temp_ser.name in self.fit_results.index:
            self.fit_results.drop(temp_ser.name, axis=0, inplace=True)
        self.fit_results = self.fit_results.append(temp_ser)
            
        fig, ax = plt.subplots()
        xx = np.linspace(0, np.max(bins), 100)
        ax.errorbar(bins, data, yerr=data_errs, fmt='.', color=data_color)
        ax.plot(xx, RegEff.sigFunc(xx, *m.values), color=fit_color)
        my_style(title=f'Registration eff. vs rad. photon energy ($\sqrt{{s}}$ = {self.index2energy(index)*2e-3:.3f} GeV)', xlim=(0, np.max(bins)), ylim=(0, None), 
                xtitle='$E_{\\gamma}$, GeV', ytitle='$\\varepsilon_{reg}$')
        values_dict = dict(zip(m.parameters, m.values))
        chi2, ndf = m.fval, len(bins)-len(m.parameters)-1
        s =  f'$\\chi^2$ / ndf = {chi2:.2f} / {ndf}\n'
        s += f'p-value: {1-stats.chi2.cdf(chi2, ndf):.2f}\n'
        for var, val, err, fixed in zip(m.parameters, m.values, m.errors, m.fixed):
            if fixed:
                s += f'{var} = {val:1.3f}\n'
            else:
                s += f'{var} = {val:1.3f}$\\pm${err:.4f}\n'
        props = dict(boxstyle='square', facecolor=bbox_color, alpha=0.5)
        ax.text(0.65, 0.95, s.strip(), transform=ax.transAxes,
               verticalalignment='top', bbox=props)
        return 