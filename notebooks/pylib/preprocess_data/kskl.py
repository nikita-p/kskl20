"""This file contains preprocessing data functions to extract $e^+ e^- \to K_S K_L$ process
"""

import os
import numpy as np
import pandas as pd

import uproot
import awkward as ak

import warnings
from typing import NewType, Tuple

from .utils import SeasonName, get_script_path

# useful utils
from .utils import bad_runs
from .utils import cut_two_body_decay_angle, two_body_decay_angle
from .utils import get_x
from .utils import kde_plot
from .utils import trigger_efficiency

def season_csv_table(season: str) -> pd.DataFrame:
    """Season csv table containing total information about exp points and MC
    
    Parameters
    ----------
    season : str
        season name
    
    Returns
    -------
    pd.DataFrame
        total season information table   
    """
    
    if season not in SeasonName._member_names_:
        raise TypeError(f'Use the season from {SeasonName._member_names_}')
    script_path = get_script_path()
    csv_path = script_path.parents[2].joinpath(f'data/{season}.csv')
    
    df_season_info = pd.read_csv(csv_path)
    return df_season_info

def open_tree(tree_path: str) -> uproot.TTree:
    """Opens root tree
    
    Parameters
    ----------
    tree_path : str
        absolute path to tree
        
    Returns
    -------
    tr_ph : uproot.TTree
        tr_ph tree from root file
    """
    
    tr_ph = uproot.open(tree_path, timeout=500)['tr_ph']
    return tr_ph

def good_tracks_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns good tracks DataFrame
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
    
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing good tracks information
    """
    e_meas = tr_ph['emeas'].array()[0]
    pidedx = '5.58030e+9 / (tptot + 40.)**3 + 2.21228e+3 - 3.77103e-1 * tptot - tdedx'
    cut = f'(nt>=2)&(nks>0)&(tnhit>6)&(abs(pidedx)<2200)&(tchi2r<30)&(tchi2z<30)&(abs(tz)<12)&(tptot>40)&(tptot<{e_meas})'
    arrs = tr_ph.arrays(['tz', 'tptot', 'tdedx', 'tcharge', 'trho', 'tth', 'tphi'],
                        cut=cut, aliases={'pidedx': pidedx})
    dat_tracks = ak.to_pandas(arrs)
    dat_tracks_groups = dat_tracks.groupby('entry').agg(uniques=('tz', 'count'), charge=('tcharge', 'sum'))
    idx = dat_tracks_groups.query('(uniques==2)&(charge==0)').index
    dat_tracks = dat_tracks.loc[idx]
    dat_tracks = dat_tracks.reset_index(level=['subentry']).rename({'subentry': 'ksvind'}, axis=1)
    dat_tracks = dat_tracks.reset_index().pivot(index='entry', columns='tcharge', values=['ksvind', 'tz', 'tptot', 'tdedx', 'trho', 'tth', 'tphi'])
    columns_name = lambda current_name: f'{current_name[0]}_{"p" if current_name[1]==1 else "n"}'
    dat_tracks.columns = [columns_name(col) for col in dat_tracks.columns.values]
    dat_tracks[['ksvind_n', 'ksvind_p']] = dat_tracks[['ksvind_n', 'ksvind_p']].astype(int)
    dat_tracks['ksvind_min'] = dat_tracks[['ksvind_n', 'ksvind_p']].min(axis=1)
    dat_tracks['ksvind_max'] = dat_tracks[['ksvind_n', 'ksvind_p']].max(axis=1)
    dat_tracks.drop(['ksvind_n', 'ksvind_p'], axis=1, inplace=True)
    
    return dat_tracks

def good_kaons_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns good kaons DataFrame
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
        
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing good kaons information
    """
    
    dlt_mass = 'abs(ksminv-497.6)'
    cut = '(nt>=2)&(nks>0)&(ksdpsi<3)&(kslen<10)'
    arrs = tr_ph.arrays(['ksptot', 'ksminv', 'ksalign', 'dlt_mass', 'ksdpsi', 'kslen', 'ksth', 'ksphi'], 
                        cut=f'{cut}&(dlt_mass<200)', aliases={'dlt_mass': dlt_mass})
    dat_kaons = ak.to_pandas(arrs)
    dat_kaons = dat_kaons[~dat_kaons.index.droplevel(1).duplicated(keep='first')]
    
    arr_ksvind = tr_ph.arrays(['ksvind', 'kspipt'], cut=cut)
    dat_ksvind = ak.to_pandas(arr_ksvind)
    dat_ksvind = dat_ksvind.reset_index(['subsubentry']).loc[dat_kaons.index]
    dat_ksvind = dat_ksvind.reset_index().pivot(index='entry', columns='subsubentry', values=['ksvind', 'kspipt'])
    columns_name = lambda current_name: f'{current_name[0]}{current_name[1]}'
    dat_ksvind['ksvind_min'] = dat_ksvind[[('ksvind', 0), ('ksvind', 1)]].min(axis=1)
    dat_ksvind['ksvind_max'] = dat_ksvind[[('ksvind', 0), ('ksvind', 1)]].max(axis=1)
    dat_ksvind.drop([('ksvind', 0), ('ksvind', 1)], axis=1, inplace=True)
#     dat_ksvind.columns = dat_ksvind.columns.droplevel(1)
    dat_ksvind.columns = [columns_name(col) for col in dat_ksvind.columns]
    
    len_dat_kaons = len(dat_kaons)
    dat_kaons = dat_kaons.join(dat_ksvind)
    assert len_dat_kaons == len(dat_kaons)
    return dat_kaons

def runnum_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Retruns runnum column
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
        
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing run numbers
    """
    
    runnum_df = ak.to_pandas(tr_ph.arrays(['runnum']))
    return runnum_df

def finalstateid_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns finalstate_id column.
    Helpful for multihadrons MC
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
        
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing finalstate indices
    """
    
    finalstate_df = ak.to_pandas(tr_ph.arrays(['finalstate_id']))
    return finalstate_df

def simphoton_energy_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns total radiative photons energies for MC
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph file
    
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing simulated radiative photons energy for each event
    """
    
    simphoton_energy_df = ak.to_pandas(tr_ph.arrays(['simtype', 'simorig', 'simmom']))
    simphoton_energy_df = simphoton_energy_df.query('(simtype==22)&(simorig==0)').groupby('entry').agg(sim_gamma_energy=('simmom', 'sum'))
    return simphoton_energy_df

def tracks_mom_vector_sum_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns vector sums of the momentums of the tracks in the event column.
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
        
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing vector sums of the momentums of the tracks in the event
    """
    
    psumch_df = ak.to_pandas(tr_ph.arrays(['psumch']))
    return psumch_df

def trigbits_df(tr_ph: uproot.TTree) -> pd.DataFrame:
    """Returns trigbits column.
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
        
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing trigbits column
    """
    
    trigbits_df = ak.to_pandas(tr_ph.arrays(['trigbits']))
    return trigbits_df

def selection_df(tr_ph: uproot.TTree, finalstate_id: bool = False, radiative_photons: bool = False, 
                trigbits: bool = False, remove_badruns: bool = False) -> pd.DataFrame:
    """Returns all selections DataFrame
    
    Parameters
    ----------
    tr_ph : uproot.TTree
        tr_ph tree
    finalstate_id : bool
        add finalstate_id column into resulting DataFrame or not
    radiative_photons : bool
        add column with total radiative photons energies for MC or not
    trigbits : bool
        add column with triggers
    remove_badruns : bool
        delete badruns from resulting table
    
    Returns
    -------
    pd.DataFrame
        pandas DataFrame containing all available information about selected events
    """
    
    dat_tracks = good_tracks_df(tr_ph)
    dat_kaons = good_kaons_df(tr_ph)
    
    merged_df = pd.merge(dat_tracks, dat_kaons, on=['entry', 'ksvind_min', 'ksvind_max'], how='inner')
    merged_df.drop(['ksvind_max', 'ksvind_min'], axis=1, inplace=True)
    
    psumch_df = tracks_mom_vector_sum_df(tr_ph)
    merged_df = merged_df.join(psumch_df)
    
    if remove_badruns:
        runnumbers_df = runnum_df(tr_ph)
        bad_runs_df = runnumbers_df.runnum.isin(bad_runs())
        good_runs_index = bad_runs_df[~bad_runs_df].index
        merged_df = merged_df.loc[good_runs_index.intersection(merged_df.index)]
    
    if finalstate_id:
        finalstate_df = finalstateid_df(tr_ph)
        merged_df = merged_df.join(finalstate_df)
        
    if radiative_photons:
        radiative_df = simphoton_energy_df(tr_ph)
        merged_df = merged_df.join(radiative_df)
    
    if trigbits:
        trig_df = trigbits_df(tr_ph)
        merged_df = merged_df.join(trig_df)
        
    return merged_df