import numpy as np
import pandas as pd
import uproot

def get_x(df: pd.DataFrame) -> (pd.Series, pd.Series):
    """
    Получить x1, x2 координаты из pd.DataFrame
    """
    rotate_f = lambda e: 0.205/(e*2e-3-0.732) + 0.14
    mKs, p = 497.6, rotate_f(df.emeas)
    p0 = np.sqrt(df.emeas**2 - mKs**2)
    dE = df.ksminv - mKs
    dP = df.ksptot - p0
    x1 =  dE*np.cos(p) - dP*np.sin(p)
    x2 =  dE*np.sin(p) + dP*np.cos(p)
    return x1, x2

def read_tree(root_file, mc=False, align_cut=0.8, z_cut=12, dedx_cut=2000, sim_parts=True) -> pd.DataFrame:
    """
    Прочитать дерево `root_file` в pd.DataFrame
    """
    particles_codes = {
        2212 : '$p^+$',
        -2212 : '$p^-$',
        2112 : '$n^+$',
        -2112 : '$\\bar{n}^-$',
        321 : '$K^+$',
        -321 : '$K^-$',
        211 : '$\pi^+$',
        -211 : '$\pi^-$',
        111 : '$\pi^0$',
        130 : '$K_L$',
        310 : '$K_S$',
        221 : '$\eta$',
    }
    df = root_file.arrays(library='pd', filter_typename=lambda x: not(x.startswith('std::vector')))
    if mc:
        df['ebeam'] = df.name.str.extract(r'_(\d+\.?\d*)_')[0].astype(float)
        df['runnum'] = df.name.str.extract(r'_(\d+\.?\d*)\.root')[0].astype(int)
    else:
        df['ebeam'] = df.name.astype(str).str.extract(r'_e(\d+.?\d*)_', expand=False).astype(float)
        df.drop(['sim_energy'], axis=1, errors='ignore', inplace=True)
    if ('sim_particles' in root_file) and (mc) and (sim_parts):
        sim_parts = root_file['sim_particles'].array(library='pd')
        sim_parts.name = 'sim_parts'
        sim_parts = sim_parts.apply(lambda x: particles_codes[x])
        sim_parts = sim_parts.groupby('entry').apply(lambda x: ''.join(x))#.sort_values()))
        df = df.join(sim_parts)
    df.drop(['name'], axis=1, inplace=True)
    df['x1'], df['x2'] = get_x(df)
    df['ksangle'] = np.arccos(df['ksalign'])
    if align_cut is not None:
        df = df.query('ksalign>@align_cut')
    if z_cut is not None:
        df = df.loc[(np.abs(df['tz[0]']) < z_cut) & (np.abs(df['tz[1]']) < z_cut)].copy()
    return df.set_index('ebeam')