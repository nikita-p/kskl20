import numba as nb
import numpy as np
import pandas as pd
from .style import plot_fit
import iminuit
from iminuit import Minuit
from iminuit.cost import UnbinnedNLL, ExtendedUnbinnedNLL, NormalConstraint
from scipy.integrate import quad
from scipy.stats import poisson

import os
import warnings
from typing import Callable, Union, Tuple, List, Dict

class Fitter():
    """
    Класс, предназначенный для фитирования гистограмм
    """
    
    def __init__(self, data: Union[np.array, pd.Series], fit_func: callable, pars: Dict[str, float], lims: Dict[str, Tuple[float, float]], fit_range: Tuple[float, float], sigmas: Dict[str, float] = {}):
        """
        Parameters
        ----------
        data : Union[np.array, pd.Series]
            данные для фита
        fit_func : callable
            функция фита (зависит x и фитируемых параметров) из классов ниже
        pars : Dict[str, float]
            словарь с начальными значениями параметров
        lims : Dict[str, Tuple[float, float]]
            словарь с ограничениями на параметры
        fit_range : Tuple[float, float]
            кортеж (xmin, xmax) с областью фитирования
        sigmas : Dict[str, float]
            словарь с отклонением параметров для регуляризации (может использоваться в эксперименте, чтоб мягко ограничить параметры) (default is {})
        """
        
        xmin, xmax = fit_range
        self.fit_range = fit_range
        self.fit_func = fit_func
        self.data = data
        self.cost = ExtendedUnbinnedNLL(data[(data>xmin)&(data<xmax)], self.fit_func)
        parnames = iminuit.util.describe(self.cost) 
        clear_dict = lambda dic: { p: dic[p] for p in set(parnames)&set(dic.keys())} #вытащить только необходимое из словаря
        self.pars, self.lims = clear_dict(pars), clear_dict(lims)
        cost0 = self.cost
        for s in clear_dict(sigmas):
            cost0 += NormalConstraint(s, self.pars[s], sigmas[s])
        self.m = Minuit(cost0, **self.pars)
        for par in self.m.parameters:
            if par in self.lims:
                self.m.limits[par] = self.lims[par]
    
    def fit(self):
        """
        Фитировать распределение
        """
        
        self.m.simplex().migrad()
        if not(self.m.valid):
            warnings.warn("Fit is not valid", UserWarning)
    
    def plot(self, hist_range: Tuple[float, float], bins: int, title: str = '', label: str = '', xtitle: str = '', ytitle: str = '', 
             errors: bool = True, alpha: float = 0.8, lw: int = 1, description: bool = True, fill_errors: bool = False,
             plot_bkg: bool = False, bbox_color: str = 'ivory', fit_color: str = None, data_color: str = None, print_fixed_vals: bool = True):
        """
        Нарисовать фит
        
        Parameters
        ----------
        hist_range : Tuple[float, float]
            диапазон, на котором будет изображаться результат
        bins : int
            количество бинов в диапазоне
        title : str
            название картинки (default is '')
        label : str
            подпись данных (default is '')
        xtitle : str
            подпись оси x (default is '')
        ytitle : str
            подпись оси y (default is '')
        errors : bool
            изображать ли усы для даных (default is True)
        alpha : float
            прозрачность линии фита в диапазоне [0, 1] (default is 0.8)
        lw : int
            толщина линии фита (default is 1)
        description : bool 
            добавить описание (default is True)
        fill_errors : bool
            закрасить область одной ошибки для фита (default is False)
        plot_bkg : bool
            изобразить фит фона
        bbox_color : str
            цвет bbox
        fit_color : Optional[str]
            цвет линии фита
        data_color : Optional[str]
            цвет линии данных
        print_fixed_vals : bool
            печатать фиксированные значения фита
        """
        
        plot_fit(self.data, self.cost, self.m, bins, hist_range, self.fit_range, errors=errors, label=label, xtitle=xtitle, alpha=alpha, lw=lw,
                   ytitle=ytitle, title=title, description=description, fill_errors=fill_errors, fit_func=self.fit_func, plot_bkg=plot_bkg,
                 bbox_color=bbox_color, fit_color=fit_color, data_color=data_color, print_fixed_vals=print_fixed_vals)
        
    def get_fitfunc(self) -> callable:
        """
        Вернуть функцию фита
        """
        
        return self.fit_func
    def get_params(self) -> dict:
        """
        Вернуть значения параметров фита
        """
        
        return {v : self.m.values[v] for v in self.m.parameters}
    
    def get_limits(self, n_sigmas: float = 2, include: List[str] = ['m', 'sL'], my_lims: Dict[str, Tuple[float, float]] = {}) -> Dict[str, Tuple[float, float]]:
        """
        Вернуть ограничения на параметры фита
        
        Parameters
        ----------
        n_sigmas : float
            количество сигм для ограничения
        include : list
            список параметров, к которым будет применено ограничение на сигмы
        my_lims : Dict[str, Tuple[float, float]]
            список кортежей с собственными ограничениями на параметры
        
        Returns
        -------
        Dict[str, Tuple[float, float]]
            ограничения на параметры фита
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
        
    def get_sigmas(self, exclude: List[str] = ['n_sig']) -> dict:
        """
        Вернуть стандартные отклонения для параметров фита
        
        Parameters
        ----------
        exclude : List[str]
            список параметров, которые не нужно возвращать (default is `['n_sig']`)
            
        Returns
        -------
        Dict[str, float]
            стандартные отклонения для параметров фита
        """
        
        sigmas_dict = {v : self.m.errors[v] for v in self.m.parameters}
        for ex in exclude:
            sigmas_dict.pop(ex, None)
        return sigmas_dict
    
class Fit1():
    def __init__(self, fit_range):
        self.fit_range = fit_range
        self.w = fit_range[1] - fit_range[0]
    def __call__(self, x, n_sig, m, sL, sR, aL, aR, y0, dy):
        return (n_sig + self.w*(2*y0+dy)/2, pdf(x, n_sig, m, sL, sR, aL, aR, y0, dy, self.fit_range))
    def get_nsig(self, minuit):
        return (minuit.values['n_sig'], minuit.errors['n_sig'])
    def get_nbkg(self, minuit):
        if minuit.fixed['y0'] and minuit.fixed['dy']:
            return (None, None)
        v = self.w*(2*minuit.values['y0']+minuit.values['dy'])/2
        e = self.w*np.sqrt(2*minuit.errors['y0']**2 + minuit.errors['dy']**2)/2
        return (v, e)
    
class Fit2():
    def __init__(self, fit_range):
        self.fit_range = fit_range
        self.xmin, self.xmax = fit_range
        self.w = fit_range[1] - fit_range[0]
    def __call__(self, x, n_sig, m, sL, sR, aL, aR, y0, dy, x0):
        return (n_sig + self.w*y0 + (dy/3)*( (self.xmax-x0)**3 - (self.xmin-x0)**3 ), n_sig*sig_pdf(x, m, sL, sR, aL, aR, self.fit_range) + self.poly2(x, dy, x0, y0))
    def poly2(self, x, k, x0, c):
        """
        k >= 0, x0 <= x_min, c >=0
        """
        return k*((x-x0)**2) + c
    def get_nsig(self, minuit):
        return (minuit.values['n_sig'], minuit.errors['n_sig'])
    def get_nbkg(self, minuit):
        if minuit.fixed['y0'] and minuit.fixed['dy']:
            return (None, None)
        x0, x0_err = minuit.values['x0'], minuit.errors['x0']
        y0, y0_err = minuit.values['y0'], minuit.errors['y0']
        dy, dy_err = minuit.values['dy'], minuit.errors['dy']
        v = self.w*y0 + (dy/3)*( (self.xmax-x0)**3 - (self.xmin-x0)**3 )
        e = 0 # написать правильно
        return (v, e)

class FitPoly2():
    def __init__(self, fit_range):
        self.fit_range = fit_range
        self.xmin, self.xmax = fit_range
        self.w = fit_range[1] - fit_range[0]
    def __call__(self, x, n_sig, m, sL, sR, aL, aR, n_bkg, b, c):
        return (n_bkg+n_sig, n_sig*sig_pdf(x, m, sL, sR, aL, aR, self.fit_range) + n_bkg*self.poly2(x, b, c))
    def poly2(self, x, b, c):
        P1 = 1
        P2 = lambda x: x
        P3 = lambda x: (3*(x**2) - 1)/2
        xn = 2*(x - self.xmin)/(self.xmax - self.xmin) - 1
        norm = (self.xmax - self.xmin)
        return (P1 + b*P2(xn) + c*P3(xn)) / norm
    def get_nsig(self, minuit):
        return (minuit.values['n_sig'], minuit.errors['n_sig'])
    def get_nbkg(self, minuit):
        return (minuit.values['n_bkg'], minuit.errors['n_bkg'])
    
class FitGauss():
    def __init__(self):
        pass
    def __call__(self, x, m, s, n_sig):
        return (n_sig, n_sig*np.exp( -(x - m)**2/2/(s**2))/np.sqrt(2*np.pi*(s**2)))
    def get_nsig(self, minuit):
        return (minuit.values['n_sig'], minuit.errors['n_sig'])
    def get_nbkg(self, minuit):
        return (0, 0)

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