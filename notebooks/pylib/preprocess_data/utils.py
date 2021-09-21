import os
import sys

from pathlib import Path
from enum import Enum
from typing import Union, Tuple, Dict, List

import numpy as np
import pandas as pd

SeasonName = Enum(
    value='Season name',
    names=['HIGH11', 'HIGH12', 'HIGH17', 'HIGH19', 'HIGH20', 'HIGH21'],
)

def get_script_path():
    return Path(__file__)

def bad_runs() -> List[int]:
    """Returns list of bad runs
    
    Returns
    -------
    List[int]
        list of bad runs
    """
    
    with open('/storeA/ryzhenenkov/badruns.dat') as f:
        bads = f.read()
    return list(map(int, bads.strip().split('\n')))

def two_body_decay_angle(Eb: float = 550, bins: int = 100):
    """Returns angles between pions from KS decay vs one pion different momenta.
    It's now for e+ e- -> KSKL.
    
    Parameters
    ----------
    Eb : float
        beam energy, MeV
    bins : int
        length of the output arrays
        
    Returns
    -------
    Tuple[np.array, np.array]
        array containing momentums of the pion, array containing angles between pions
    """
    
    Mk = 497.6
    Mp = 139.6
    V = np.sqrt(Eb**2 - Mk**2)/Eb
        
    e0 = Mk/2
    p0 = np.sqrt(e0**2 - Mp**2)
    v0 = p0/e0
    emin, emax = (e0 - V*p0)/np.sqrt(1 - V**2), (e0 + V*p0)/np.sqrt(1 - V**2)
    pmin, pmax = np.sqrt(emin**2 - Mp**2), np.sqrt(emax**2 - Mp**2)
    momentums = np.linspace(pmin, pmax, bins)
    
    cos_th = lambda e: (e*np.sqrt(1 - V**2) - e0)/(V*p0)
    ctg = lambda th: np.arctan2(2*V*v0*np.sqrt(1-V**2)*np.sin(th), V**2 - v0**2 + (V*v0*np.sin(th))**2)
    
    energies = np.sqrt(momentums**2 + Mp**2)
    theta = np.arccos(cos_th(energies).round(6))
    return momentums, ctg(theta)

def cut_two_body_decay_angle(tptot: Union[np.array, pd.Series], ksdpsi: Union[np.array, pd.Series], ebeam_band: Tuple[float, float]) -> Union[np.array, pd.Series]:
    """Pion (from KS decay) momentum (`tptot`) vs angle between two pions (`ksdpsi`) filter
    
    Parameters
    ----------
    tptot : Union[np.array, pd.Series]
        pion momentums, MeV
    ksdpsi : Union[np.array, pd.Series]
        angles between pions, rad
    ebeam_band : Tuple[float, float]
        KS energy deviation, MeV
    
    Returns
    -------
    Union[np.array, pd.Series]
        filtering mask
    """
    
    mmin, amin = two_body_decay_angle(ebeam_band[0], bins=500)
    mmax, amax = two_body_decay_angle(ebeam_band[1], bins=500)
    right_band = np.interp(tptot, mmin, amin)
    left_band = np.interp(tptot, mmax, amax, left=np.pi, right=np.pi)
    return (left_band < ksdpsi) & (ksdpsi < right_band)

def get_x(ksminv: pd.Series, ksptot: pd.Series, ebeam: float) -> Tuple[pd.Series, pd.Series]:
    """
    Returns x1, x2 coordinates from pd.DataFrame
    
    Parameters
    ----------
    ksminv : pd.Series
        invariant mass column
    ksptot : pd.Series
        KS momentum column 
    ebeam : float
        beam energy
    
    Returns
    -------
    Tuple[pd.Series, pd.Series]
        x1, x2 coordinates respectively
    """
    
    rotate_f = lambda e: 0.205/(e*2e-3-0.732) + 0.14
    mKs, p = 497.6, rotate_f(ebeam)
    p0 = np.sqrt(ebeam**2 - mKs**2)
    dE = ksminv - mKs
    dP = ksptot - p0
    x1 =  dE*np.cos(p) - dP*np.sin(p)
    x2 =  dE*np.sin(p) + dP*np.cos(p)
    return x1, x2

def efficiency(numerator: np.array, denominator: np.array) -> Tuple[np.array, np.array]:
    """Calculates efficiencies and them errors
    
    Parameters
    ----------
    numerator : np.array
        passed number of entries
    denominator : np.array
        total number of entries
    
    Returns
    -------
    Tuple[np.array, np.array]
        efficiency mean and error
    """
    
    mean = (numerator + 1) / (denominator + 2)
    error = np.sqrt( (numerator + 1)*(numerator + 2)/(denominator + 2)/(denominator + 3) - ((numerator + 1)/(denominator + 2))**2)
    return (mean, error)

def trigger_efficiency(trigbits: pd.Series) -> Dict[str, Tuple[float, float]]:
    """Returns trigger efficiency
    
    Parameters
    ----------
    trigbits : pd.Series
        column containing trigger bits
        
    Returns
    -------
    Dict[str, Tuple[float, float]]
        dictionary containing trigger efficiencies and errors
    """
    
    tb = trigbits.value_counts()
    T = tb[1] if 1 in tb else 0
    C = tb[2] if 2 in tb else 0
    TC = tb[3] if 3 in tb else 0
    eff_T = efficiency(TC, C + TC)
    eff_C = efficiency(TC, T + TC)
    eff_TC = (1 - (1 - eff_T[0])*(1 - eff_C[0]), np.sqrt((eff_T[1]*(1 - eff_C[0]))**2 + (eff_C[1]*(1 - eff_T[0]))**2))
    
    eff_dict = dict(T=eff_T, C=eff_C, TC=eff_TC)
    return eff_dict

def kde_plot(x: np.array, y: np.array, bins: tuple = (100, 100), range: tuple = None, cmap: str = None):
    """KDE plot
    
    Parameters
    ----------
    x : np.array
        x values array
    y : np.array
        y values array
    bins : tuple
        number of bins
    range : tuple
        range of plot
    cmap : str
        color scheme
    """
    from scipy.stats import kde
    import matplotlib.pyplot as plt
    k = kde.gaussian_kde([x, y])
    if range is None:
        range = ((x.min(), x.max()), (y.min(), y.max()))
    xi, yi = np.mgrid[range[0][0]:range[0][1]:bins[0]*1j, range[1][0]:range[1][1]:bins[1]*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto', cmap=cmap)