import numpy as np
import pandas as pd
import uproot
import warnings
import awkward as ak

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
        try:
            df['runnum'] = df.name.str.extract(r'_(\d+\.?\d*)\.root')[0].astype(int)
        except:
            warnings.warn("Runnum warning", UserWarning)
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


class Handler:
    def __init__(self, tree, cut_dedx=2500, cut_z=12, cut_align=0.8):
        self.tree = tree
        self.cut_dedx = cut_dedx
        self.cut_z = cut_z
        self.cut_align = cut_align
    def get_dat_tracks(self):
        e0 = self.tree['emeas'].array()[0]
        pidedx = '5.58030e+9 / (tptot + 40.)**3 + 2.21228e+3 - 3.77103e-1 * tptot - tdedx'
        arrs = self.tree.arrays(['tz', 'tptot', 'tdedx', 'tcharge', 'trho'], 
                         f'(nt>=2)&(nks>0)&(tnhit>6)&(abs(pidedx)<{self.cut_dedx})&(tchi2r<20)&(tchi2z<20)&(abs(tz)<{self.cut_z})&(tptot<{e0})&(tptot>40)', 
                         aliases={'pidedx': pidedx})
        dat_tracks = ak.to_pandas(arrs)
        dat_tracks_groups = dat_tracks.groupby('entry').agg(uniques=('tz', 'count'), charge=('tcharge', 'sum'))
        idx = dat_tracks_groups.query('(uniques==2)&(charge==0)').index
        return dat_tracks.loc[idx]#.drop('tcharge', axis=1)
    def get_dat_kaons(self):
        dlt_mass = 'abs(ksminv-497.6)'
        cuts = f'(nt>=2)&(ksalign>{self.cut_align})&(dlt_mass<100)'
        dat_kaons = ak.to_pandas(self.tree.arrays(['ksptot', 'ksminv', 'ksalign', 'dlt_mass', 'ksvind', 'ksdpsi'], 
                           cuts, aliases={'dlt_mass': dlt_mass})).loc[:, :, :1]
        dat_kaons = dat_kaons.reset_index().drop('subsubentry', axis=1).set_index(['entry', 'subentry'])
        kaons = dat_kaons.sort_values(by=['dlt_mass']).reset_index().drop_duplicates(subset=['entry'], keep='first').set_index(['entry', 'subentry']).index
        dat_kaons = dat_kaons.loc[kaons]
        return dat_kaons.reset_index().drop(['subentry'], axis=1).rename({'ksvind': 'subentry'}, axis=1).set_index(['entry', 'subentry'])
    def get_good_kaons(self):
        dat_tracks = self.get_dat_tracks()
        dat_kaons = self.get_dat_kaons()
        dat_glob = self.get_dat_glob()

        dat_goods = dat_tracks.join(dat_kaons, how='inner')
        goods = dat_goods.groupby('entry').agg(num=('tz', 'count')).query('num==2').index
        dat_goods = dat_goods.reset_index().set_index('entry').loc[goods].reset_index().set_index(['entry', 'subentry'])

        dat_goods['tcharge'] = np.where(dat_goods['tcharge']>0, 'p', 'n')
        dat_goods = pd.pivot_table(dat_goods.reset_index(), values=['trho', 'tz', 'tdedx', 
                    'tptot', 'ksminv', 'ksalign', 'ksptot', 'ksdpsi'], 
               index=['entry'], columns=['tcharge'])
        dat_goods.columns = ['_'.join(map(lambda x: str(x), col)) for col in dat_goods.columns]
        dat_goods.drop(['ksalign_n', 'ksminv_n', 'ksptot_n', 'ksdpsi_n'], axis=1, inplace=True)
        
        #kick badruns
        dat_glob = dat_glob.query('badrun==False')
        dat_goods = dat_goods.join(dat_glob, how='inner')
        
        #add x1, x2
        dat_goods = dat_goods.rename({'ksalign_p': 'kalign', 'ksminv_p': 'ksminv',
                                     'ksptot_p': 'ksptot', 'ksdpsi_p': 'ksdpsi'}, axis=1)
        dat_goods['x1'], dat_goods['x2'] = get_x(dat_goods)
        return dat_goods
    def get_dat_glob(self):
        dat_glob = ak.to_pandas(self.tree.arrays(['ebeam', 'emeas', 'lumoff', 'lumofferr', 'runnum', 'finalstate_id']))
        badruns = np.loadtxt('pylib/badruns.dat')
        dat_glob['badrun'] = dat_glob.runnum.isin(badruns)
        return dat_glob