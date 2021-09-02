import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uproot
import os
from .preprocess import HandlerKSKS
from .statistics import efficiency_error

def preprocess_point(row, df_4pic, season='19', force_process=False, print_log=True):
    """
    Предварительно обработать строку `row`
    df_4pic - данные для 4pi
    force_process - не искать уже сохранённые файлы, а обработать заново
    print_log - показывать логи
    """
    filename_exp = f'../csv/ksks/data/df_cut_exp_{row["elabel"]}.csv'
    filename_mlt = f'../csv/ksks/data/df_cut_mlt_{row["elabel"]}.csv'
    filename_4pi = f'../csv/ksks/data/df_cut_4pi_{row["elabel"]}.csv'
    
    tr_exp = uproot.open(row['exp_tree'])['tr_ph']
    
    tr_mlt = None
    if not(np.isnan(row['mlt_raw'])):
        tr_mlt = uproot.open(
            f'/store17/petrov/data/kskl20/tr_ph/multi/{season}/tr_ph_run0{row["mlt_raw"]:.0f}.root')['tr_ph']
    tr_4pi = None
    if not(np.isnan(row['4pi_raw'])):
        tr_4pi = uproot.open(
            f'/store17/petrov/data/kskl20/tr_ph/4pi/{season}/tr_ph_run0{row["4pi_raw"]:.0f}.root')['tr_ph']
            
    def preprocess_one_file(tr, filename):
        if tr is None:
            return None
        hd = HandlerKSKS(tr)
        df = hd.get_good_kaons()
        df_cut = HandlerKSKS.collinear_cut(df, 0.4, 0.4, plot=False)
        df_cut = HandlerKSKS.sum_energy_cut(df_cut, cut_en=250, plot=False)
        df_cut = HandlerKSKS.kaon_mom_cut(df_cut, cut_mom=120, plot=False)
        df_cut.to_csv(filename)
        return df_cut
    
    if not(os.path.isfile(filename_exp)) or force_process:
        df_cut_exp = preprocess_one_file(tr_exp, filename_exp)
    else:
        df_cut_exp = pd.read_csv(filename_exp, index_col=['entry', 'subentry'])
    if not(os.path.isfile(filename_mlt)) or force_process:
        df_cut_mlt = preprocess_one_file(tr_mlt, filename_mlt)
    else:
        df_cut_mlt = pd.read_csv(filename_mlt, index_col=['entry', 'subentry'])
    if not(os.path.isfile(filename_4pi)) or force_process:
        df_cut_4pi = preprocess_one_file(tr_4pi, filename_4pi)
    else:
        df_cut_4pi = pd.read_csv(filename_4pi, index_col=['entry', 'subentry'])
        
    cs_vis = np.interp(row['emeas'], df_4pic['ebeam'], df_4pic['cs_vis'])
    
    n_4pi_bkg, n_bkg, n_4pi = 0, 0, 0
    part_4pic, part_4pic_err = np.nan, np.nan
    
    if df_cut_4pi is not None:
        n_4pi_bkg += df_cut_4pi.index.droplevel(1).nunique()
        n_bkg += df_cut_4pi.index.droplevel(1).nunique()
        n_4pi += len(tr_4pi.arrays(['finalstate_id']))
        
    if df_cut_mlt is not None:
        n_4pi_bkg_mlt = df_cut_mlt.query('finalstate_id==2').index.droplevel(1).nunique()
        n_bkg_mlt = df_cut_mlt.index.droplevel(1).nunique()
        n_4pi_bkg += n_4pi_bkg_mlt
        n_bkg += n_bkg_mlt
        n_4pi += len(tr_mlt.arrays(['finalstate_id'], 'finalstate_id==2'))
        part_4pic = (n_4pi_bkg_mlt + 1)/(n_bkg_mlt + 2)
        part_4pic_err = efficiency_error(n_4pi_bkg_mlt, n_bkg_mlt)
        
    real_events = df_cut_exp.index.droplevel(1).nunique()
    
    eff_4pic = (n_4pi_bkg + 1)/(n_4pi + 2)
    N_events = row['lum_exp']*eff_4pic*cs_vis
    N_events_err = (N_events/eff_4pic)*efficiency_error(n_4pi_bkg + 1, n_4pi + 2)
    eff_err = efficiency_error(n_4pi_bkg, n_4pi)
    
    if print_log:
        s = f'elabel = {row["elabel"]}, eff_4pic = {eff_4pic:.2%}, '
        s += f'part_4pic = {part_4pic:.1%}, n_expect = {N_events:.1f}, '
        s += f'n_real = {real_events}'
        print(s)
    d0 = {
        'emeas' : row['emeas'],
        'eff_4pic' : eff_4pic,
        'eff_err' : eff_err,
        'n_events' : N_events,
        'n_events_err' : N_events_err,
        'real_events': real_events,
        'part_4pic': part_4pic,
        'part_4pic_err': part_4pic_err,        
    }
    return d0

def process_point(row, df_4pic: pd.DataFrame, season: str = '19', print_log: bool = True) -> dict:
    """
    Дообработать строку `row`
    df_4pic - данные для 4pi
    print_log - показывать логи
    """
    filename_exp = f'../csv/ksks/data/df_cut_exp_{row["elabel"]}.csv'
    filename_mlt = f'../csv/ksks/data/df_cut_mlt_{row["elabel"]}.csv'
    filename_4pi = f'../csv/ksks/data/df_cut_4pi_{row["elabel"]}.csv'
    
    
    tr_exp = uproot.open(row['exp_tree'])['tr_ph']
    
    tr_mlt = None
    if not(np.isnan(row['mlt_raw'])):
        tr_mlt = uproot.open(
            f'/store17/petrov/data/kskl20/tr_ph/multi/{season}/tr_ph_run0{row["mlt_raw"]:.0f}.root')['tr_ph']
    tr_4pi = None
    if not(np.isnan(row['4pi_raw'])):
        tr_4pi = uproot.open(
            f'/store17/petrov/data/kskl20/tr_ph/4pi/{season}/tr_ph_run0{row["4pi_raw"]:.0f}.root')['tr_ph']
            
    
    def process_one_file(df):
        if df is None:
            return None
        df_cut = HandlerKSKS.collinear_cut(df, 0.25, 0.15)
        df_cut = HandlerKSKS.sum_energy_cut(df_cut, cut_en=100)
        df_cut = HandlerKSKS.kaon_mom_cut(df_cut, cut_mom=60)
        df_cut = HandlerKSKS.flight_cut(df_cut, cut_flight=0.1)
        df_cut = HandlerKSKS.ksminv_cut(df_cut, cut_mass=25)
        return df_cut
    
    df_cut_exp = process_one_file(
        pd.read_csv(filename_exp, index_col=['entry', 'subentry'])
    ) if os.path.isfile(filename_exp) else None
    df_cut_mlt = process_one_file(
        pd.read_csv(filename_mlt, index_col=['entry', 'subentry'])
    ) if os.path.isfile(filename_mlt) else None
    df_cut_4pi = process_one_file(
        pd.read_csv(filename_4pi, index_col=['entry', 'subentry'])
    ) if os.path.isfile(filename_4pi) else None
    
    cs_vis = np.interp(row['emeas'], df_4pic['ebeam'], df_4pic['cs_vis'])
    
    n_4pi_bkg, n_bkg, n_4pi = 0, 0, 0
    part_4pic, part_4pic_err = np.nan, np.nan
    
    if df_cut_4pi is not None:
        n_4pi_bkg += df_cut_4pi.index.droplevel(1).nunique()
        n_bkg += df_cut_4pi.index.droplevel(1).nunique()
        n_4pi += len(tr_4pi.arrays(['finalstate_id']))
        
    if df_cut_mlt is not None:
#         n_4pi_bkg += df_cut_mlt.query('finalstate_id==2').index.droplevel(1).nunique()
#         n_bkg += df_cut_mlt.index.droplevel(1).nunique()
#         n_4pi += len(tr_mlt.arrays(['finalstate_id'], 'finalstate_id==2'))
        n_4pi_bkg_mlt = df_cut_mlt.query('finalstate_id==2').index.droplevel(1).nunique()
        n_bkg_mlt = df_cut_mlt.index.droplevel(1).nunique()
        n_4pi_bkg += n_4pi_bkg_mlt
        n_bkg += n_bkg_mlt
        n_4pi += len(tr_mlt.arrays(['finalstate_id'], 'finalstate_id==2'))
        part_4pic = (n_4pi_bkg_mlt + 1)/(n_bkg_mlt + 2)
        part_4pic_err = efficiency_error(n_4pi_bkg_mlt, n_bkg_mlt)
        
    real_events = df_cut_exp.index.droplevel(1).nunique()
    
    eff_4pic = (n_4pi_bkg + 1)/(n_4pi + 2)
    N_events = row['lum_exp']*eff_4pic*cs_vis
    N_events_err = (N_events/eff_4pic)*efficiency_error(n_4pi_bkg + 1, n_4pi + 2)
    eff_err = efficiency_error(n_4pi_bkg, n_4pi)
    
    if print_log:
        s = f'elabel = {row["elabel"]}, eff_4pic = {eff_4pic:.2%}, '
        s += f'part_4pic = {part_4pic:.1%}, n_expect = {N_events:.1f}, '
        s += f'n_real = {real_events}'
        print(s)
    d0 = {
        'elabel' : row['elabel'],
        'emeas' : row['emeas'],
        'eff_4pic' : eff_4pic,
        'eff_err' : eff_err,
        'n_events' : N_events,
        'n_events_err' : N_events_err,
        'real_events': real_events,
        'part_4pic': part_4pic,
        'part_4pic_err': part_4pic_err,        
    }
    return d0