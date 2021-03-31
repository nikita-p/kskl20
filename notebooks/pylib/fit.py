import numba as nb
import numpy as np
from .style import plot_fit
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL, ExtendedUnbinnedNLL, NormalConstraint 
from scipy.integrate import quad
from scipy.stats import poisson

import os
import warnings

class Fitter():
    def __init__(self, data, fit_func, pars:dict, lims:dict, fit_range:tuple, sigmas={}):
        """
        data - данные для фита
        fit_func - функция фита (зависит x и фитируемых параметров)
        pars - словарь с начальными значениями параметров
        lims - словарь с ограничениями на параметры
        fit_range - кортеж (xmin, xmax) с областью фитирования
        sigmas - словарь с отклонением параметров для регуляризации (может использоваться в эксперименте, чтоб мягко ограничить параметры)
        """
        xmin, xmax = fit_range
        self.fit_range = fit_range
        self.fit_func = fit_func
        self.data = data
        self.pars, self.lims = pars, lims
        self.cost = ExtendedUnbinnedNLL(data[(data>xmin)&(data<xmax)], self.fit_func)
        cost0 = self.cost
        for s in sigmas:
            cost0 += NormalConstraint(s, pars[s], sigmas[s])
        self.m = Minuit(cost0, **pars)
        for par in self.m.parameters:
            self.m.limits[par] = lims[par]
    def fit(self):
        self.m.simplex().migrad()
        if not(self.m.valid):
            warnings.warn("Fit is not valid", UserWarning)
    def plot(self, hist_range, bins, title='', label='', xtitle='', ytitle='', 
             errors=True, alpha=0.8, description=True, fill_errors=False):
        """
        Нарисовать фит
        hist_range:tuple - диапазон, на котором будет изображаться результат
        bins:int - количество бинов в диапазоне
        title:str - название картинки
        label:str - подпись данных
        xtitle:str - подпись оси x
        ytitle:str - подпись оси y
        errors:bool - изображать ли усы для даных
        alpha:float - прозрачность линии фита в диапазоне [0, 1]
        description:bool - добавить описание
        fill_errors:bool - закрасить область одной ошибки для фита
        """
        plot_fit(self.data, self.cost, self.m, bins, hist_range, self.fit_range, errors=errors, label=label, xtitle=xtitle, alpha=alpha,
                   ytitle=ytitle, title=title, description=description, fill_errors=fill_errors)
    def get_params(self) -> dict:
        """
        Вернуть значения параметров фита
        """
        return {v : self.m.values[v] for v in self.m.parameters}
    def get_limits(self, n_sigmas=2, include=['m', 'sL'], my_lims={}) -> dict:
        """
        Вернуть ограничения на параметры фита
        n_sigmas:float - количество сигм для ограничения
        include:list - список параметров, к которым будет применено ограничение на сигмы
        my_lims:dict - список кортежей с собственными ограничениями на параметры
        """
        lims_dict = self.lims.copy()
        for key in include:
            m = self.m.values[key]
            s = self.m.errors[key]
            l_min = lims_dict[key][0] if lims_dict[key][0] is not None else m-n_sigmas*s
            l_max = lims_dict[key][1] if lims_dict[key][1] is not None else m+n_sigmas*s
            lims_dict[key] = (max(l_min, m-n_sigmas*s), 
                              min(l_max, m+n_sigmas*s))
        for key in my_lims:
            lims_dict[key] = my_lims[key]
        return lims_dict
        
    def get_sigmas(self, exclude=['n_sig']) -> dict:
        """
        Вернуть стандартные отклонения для параметров фита
        exclude:list - список параметров, которые не нужно возвращать
        """
        sigmas_dict = {v : self.m.errors[v] for v in self.m.parameters}
        for ex in exclude:
            sigmas_dict.pop(ex, None)
        return sigmas_dict

def sig_pdf(x, m, sL, sR, aL, aR, fit_range):
    return cruijff_norm(x, m, sL, sR, aL, aR, fit_range)

def pdf(x, n_sig, m, sL, sR, aL, aR, y0, dy, fit_range):
    return n_sig*cruijff_norm(x, m, sL, sR, aL, aR, fit_range) + linear(x, y0, dy, fit_range)

def fitter(data, fit_range, params, mc=False):
    params = params.copy()
    xmin, xmax = fit_range
    width = xmax - xmin
    data = data[(data>=xmin)&(data<=xmax)]
#     print(len(data))
    if mc:
        cost_function0 = ExtendedUnbinnedNLL(data, lambda x, n_sig, m, sL, sR, aL, aR: 
            (n_sig, n_sig*sig_pdf(x, m, sL, sR, aL, aR, fit_range)))
        cost_function = cost_function0
        del params['y0'], params['dy'], 
    else:
        cost_function0 = ExtendedUnbinnedNLL(data, lambda x, n_sig, m, sL, sR, aL, aR, y0, dy: ( n_sig + width*(2*y0+dy)/2, pdf(x, n_sig, m, sL, sR, aL, aR, y0, dy, fit_range)))
        cost_function = cost_function0 + NormalConstraint('sL', params['sL'][0], params['sL'][1]) + NormalConstraint('sR', params['sR'][0], params['sR'][1]) + \
                NormalConstraint('aL', params['aL'][0], params['aL'][1]) + NormalConstraint('aR', params['aR'][0], params['aR'][1]) + NormalConstraint('m', params['m'][0], params['m'][1])
    parameters = {k : params[k][0] for k in params}
    m = Minuit(cost_function, **parameters)
    for par in m.parameters:
        m.limits[par] = params[par][1]
#     m.errordef= Minuit.LIKELIHOOD
    return (m, cost_function0)


@nb.njit(parallel=False, fastmath=True)
def cruijff(x, m, sL, sR, aL, aR):
    denom = 2*np.where(x<m, (sL**2 + aL*(x-m)**2), (sR**2 + aR*(x-m)**2) )
    return np.exp(-(x-m)**2/denom)

def cruijff_norm(x, m, sL, sR, aL, aR, fit_range):
    xmin, xmax = fit_range
#     try:
    I = quad(cruijff, xmin, xmax, args=(m, sL, sR, aL, aR))[0]
    return cruijff(x, m, sL, sR, aL, aR)/I
#     except:
#         return np.ones_like(x)/(xmax-xmin)

@nb.njit(parallel=False, fastmath=True)
def linear(x, y0, dy, fit_range):
    xmin, xmax = fit_range
    y1 = y0 + dy
    return (y1 - y0)*(x - xmin)/(xmax - xmin) + y0

@nb.njit(parallel=False, fastmath=True)
def linear_norm(x, k, fit_range):
    xmin, xmax = fit_range
    w = xmax - xmin
    f = (1/w)*((k*(x-xmin)+1)/((k*w)/2+1))
    return f #np.where(f<0, 0, f)