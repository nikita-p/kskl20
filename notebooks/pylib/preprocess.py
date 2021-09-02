import numpy as np
import pandas as pd
import uproot
import warnings
import awkward as ak
import vector
import matplotlib.pyplot as plt

from typing import Tuple

def get_x(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """
    Получить x1, x2 координаты из pd.DataFrame
    
    Parameters
    ----------
    df : pd.DataFrame
        датафрейм с данными
    
    Returns
    -------
    Tuple[pd.Series, pd.Series]
        координаты x1, x2 соответственно
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
        arrs = self.tree.arrays(['tz', 'tptot', 'tdedx', 'tcharge', 'trho', 'tth', 'tphi'], 
                         f'(nt>=2)&(nks>0)&(tnhit>6)&(abs(pidedx)<{self.cut_dedx})&(tchi2r<20)&(tchi2z<20)&(abs(tz)<{self.cut_z})&(tptot<{e0})&(tptot>40)', 
                         aliases={'pidedx': pidedx})
        dat_tracks = ak.to_pandas(arrs)
        dat_tracks_groups = dat_tracks.groupby('entry').agg(uniques=('tz', 'count'), charge=('tcharge', 'sum'))
        idx = dat_tracks_groups.query('(uniques==2)&(charge==0)').index
        return dat_tracks.loc[idx]#.drop('tcharge', axis=1)
    def get_dat_kaons(self):
        dlt_mass = 'abs(ksminv-497.6)'
        cuts = f'(nt>=2)&(nks>0)&(ksalign>{self.cut_align})&(dlt_mass<200)'
        dat_kaons = ak.to_pandas(self.tree.arrays(['ksptot', 'ksminv', 'ksalign', 'dlt_mass', 'ksvind', 'ksdpsi', 'ksz0', 'kslen', 'ksth', 'ksphi'], 
                           cuts, aliases={'dlt_mass': dlt_mass})).loc[:, :, :1]
        dat_kaons = dat_kaons.reset_index().drop('subsubentry', axis=1).set_index(['entry', 'subentry'])
        kaons = dat_kaons.sort_values(by=['dlt_mass']).reset_index().drop_duplicates(subset=['entry'], keep='first').set_index(['entry', 'subentry']).index
        dat_kaons = dat_kaons.loc[kaons]
        return dat_kaons.reset_index().drop(['subentry'], axis=1).rename({'ksvind': 'subentry'}, axis=1).set_index(['entry', 'subentry'])
    def get_good_kaons(self, photons='one'):
        """
        photons : None, 'one', 'all' -- как работать с фотонами из калориметра. None -- не добавлять их в данные, 
        'one' -- только пару с лучшим соответствием pi0, 'all' -- добавить все пары
        """
        dat_tracks = self.get_dat_tracks()
        dat_kaons = self.get_dat_kaons()
        dat_glob = self.get_dat_glob()

        dat_goods = dat_tracks.join(dat_kaons, how='inner')
        goods = dat_goods.groupby('entry').agg(num=('tz', 'count')).query('num==2').index
        dat_goods = dat_goods.reset_index().set_index('entry').loc[goods].reset_index().set_index(['entry', 'subentry'])

        dat_goods['tcharge'] = np.where(dat_goods['tcharge']>0, 'p', 'n')
        dat_goods = pd.pivot_table(dat_goods.reset_index(), values=['trho', 'tz', 'tdedx', 
                    'tptot', 'tth', 'tphi', 'ksminv', 'ksalign', 'ksptot', 'ksdpsi', 'ksz0', 'kslen', 'ksth', 'ksphi'], 
               index=['entry'], columns=['tcharge'])
        dat_goods.columns = ['_'.join(map(lambda x: str(x), col)) for col in dat_goods.columns]
        dat_goods.drop(['ksalign_n', 'ksminv_n', 'ksptot_n', 'ksdpsi_n', 'ksz0_n', 'kslen_n', 'ksth_n', 'ksphi_n'], axis=1, inplace=True)
        
        #kick badruns
        dat_glob = dat_glob.query('badrun==False')
        dat_goods = dat_goods.join(dat_glob, how='inner')
        
        #add x1, x2
        dat_goods = dat_goods.rename({'ksalign_p': 'ksalign', 'ksminv_p': 'ksminv',
                                     'ksptot_p': 'ksptot', 'ksdpsi_p': 'ksdpsi', 'ksz0_p': 'ksz0', 'kslen_p': 'kslen', 'ksth_p': 'ksth',
                                     'ksphi_p': 'ksphi'}, axis=1)
        dat_goods['x1'], dat_goods['x2'] = get_x(dat_goods)
        
        #calc recoil mass
        vec = vector.array({
            'pt' : dat_goods['ksptot']*np.sin(dat_goods['ksth']),
            'theta' : dat_goods['ksth'],
            'phi' : dat_goods['ksphi'],
            'mass' : dat_goods['ksminv'],
        })
        vec0 = vector.obj(px=0, py=0, pz=0, E=dat_goods['emeas'].mean()*2)
        dat_goods['recoil'] = (vec0 - vec).mass
        del vec
        
        #add photons
        if photons is not None:
            dat_photons = self.get_dat_photons()
            dat_goods = pd.merge(dat_goods.reset_index(), dat_photons.reset_index(), on='entry', how='left')
            dat_goods['subentry'] = dat_goods['subentry'].fillna(0).astype(int)
            dat_goods = dat_goods.set_index(['entry', 'subentry'])
            if photons == 'one':
                dat_goods = dat_goods.sort_values('M', ascending=True, key=lambda x: np.abs(x-134.97)).groupby('entry').agg('first')
        
        return dat_goods
    def get_dat_photons(self):
        arrs = self.tree.arrays(['pt', 'theta', 'phi', 'mass'], cut='(nt>=2)&(nks>0)&(phen>0)', aliases={'pt': 'phen*sin(phth)', 'theta': 'phth', 
                                                                          'phi': 'phphi', 'mass': '0*phen'})
        vecs = vector.Array(arrs)

        df = ak.to_pandas(ak.combinations(vecs.px, 2))
        df = df.rename({ '0' : 'px0', '1' : 'px1'}, axis=1)
        df_len = len(df)

        df = df.join( ak.to_pandas(ak.combinations(vecs.py, 2)) )
        assert df_len == len(df)
        df_len = len(df)
        df = df.rename({ '0' : 'py0', '1' : 'py1'}, axis=1)

        df = df.join( ak.to_pandas(ak.combinations(vecs.pz, 2)) )
        assert df_len == len(df)
        df_len = len(df)
        df = df.rename({ '0' : 'pz0', '1' : 'pz1'}, axis=1)

        df = df.join( ak.to_pandas(ak.combinations(vecs.E, 2)) )
        assert df_len == len(df)
        df_len = len(df)
        df = df.rename({ '0' : 'E0', '1' : 'E1'}, axis=1)

        for coord in ('x', 'y', 'z'):
            df[f'P{coord}'] = df[f'p{coord}0'] + df[f'p{coord}1']
        df['P'] = np.sqrt( df['Px']**2 + df['Py']**2 + df['Pz']**2 )
        df['E'] = df['E0'] + df['E1']
        M2 = df['E']**2 - df['P']**2
        df['M'] = np.where(M2>0, np.sqrt( np.abs(M2) ), -np.sqrt( np.abs(M2) ))
        return df
    def get_dat_glob(self):
        """
        Работа с глобальными переменными и поиск `badruns`
        """
        dat_glob = ak.to_pandas(self.tree.arrays(['ebeam', 'emeas', 'lumoff', 'lumofferr', 'runnum', 'finalstate_id', 'trigbits']))
        badruns = np.loadtxt('pylib/badruns.dat')
        dat_glob['badrun'] = dat_glob.runnum.isin(badruns)
        return dat_glob
    
class HandlerKSKS:
    def __init__(self, tree, cut_dedx=2500, cut_z=12, cut_align=0.8):
        """
        Поиск KSKS
        """
        self.tree = tree
        self.cut_dedx = cut_dedx
        self.cut_z = cut_z
        self.cut_align = cut_align
    def get_dat_tracks(self):
        e0 = self.tree['emeas'].array()[0]
        pidedx = '5.58030e+9 / (tptot + 40.)**3 + 2.21228e+3 - 3.77103e-1 * tptot - tdedx'
        arrs = self.tree.arrays(['tz', 'tptot', 'tdedx', 'tcharge', 'trho', 'tth', 'tphi'], 
                         f'(nt>=4)&(nks==2)&(tnhit>6)&(abs(pidedx)<{self.cut_dedx})&(tchi2r<20)&(tchi2z<20)&(abs(tz)<{self.cut_z})&(tptot<{e0})&(tptot>40)', 
                         aliases={'pidedx': pidedx})
        dat_tracks = ak.to_pandas(arrs)
        dat_tracks_groups = dat_tracks.groupby('entry').agg(uniques=('tz', 'count'), charge=('tcharge', 'sum'))
        idx = dat_tracks_groups.query('(uniques==4)&(charge==0)').index
        dat_tracks = dat_tracks.loc[idx]
        dat_tracks.index.rename(['entry', 'ksvind'], inplace=True)
        return dat_tracks
    def get_dat_kaons(self):
        dlt_mass = 'abs(ksminv-497.6)'
        cuts = f'(nt>=4)&(nks==2)&(ksalign>{self.cut_align})&(dlt_mass<200)'
        dat_kaons = ak.to_pandas(self.tree.arrays(['ksptot', 'ksminv', 'ksalign', 'dlt_mass', 'ksvind', 'ksdpsi', 'ksz0', 'kslen', 'ksth', 'ksphi'], 
                           cuts, aliases={'dlt_mass': dlt_mass})).loc[:, :, :1]
        
        idx2kaons = dat_kaons.groupby('entry').agg(n=('ksvind', 'nunique')).query('n==4').index
        dat_kaons = dat_kaons.loc[idx2kaons]
        return dat_kaons.reset_index().set_index(['entry', 'subentry', 'ksvind']).drop(['subsubentry'], axis=1)
    def get_good_kaons(self, photons='one'):
        """
        """
        dat_tracks = self.get_dat_tracks()
        dat_kaons = self.get_dat_kaons()
        dat_glob = self.get_dat_glob()

        dat_goods = dat_tracks.join(dat_kaons, how='inner')
        
        #kick badruns
        dat_glob = dat_glob.query('badrun==False')
        dat_goods = dat_goods.join(dat_glob, how='inner')
        dat_goods['tcharge'] = np.where(dat_goods['tcharge']>0, 'p', 'n')
        
        #pivot
        dat1 = pd.pivot_table(
            dat_goods, values=['tz', 'trho', 'tdedx', 'tth', 'tphi'],
            index=['entry', 'subentry'],
            columns=['tcharge']
        )
        dat1.columns = ['_'.join(map(lambda x: str(x), col)) for col in dat1.columns]
        dat2 = dat_goods.reset_index().drop_duplicates(subset=['entry', 'subentry']).set_index(['entry', 'subentry'])[['ksptot',
       'ksminv', 'ksalign', 'dlt_mass', 'ksdpsi', 'ksz0', 'kslen', 'ksth',
       'ksphi', 'ebeam', 'emeas', 'lumoff', 'lumofferr', 'runnum',
       'finalstate_id', 'trigbits', 'badrun']]
        dat1 = dat1.join(dat2)
        return dat1
    def get_dat_glob(self):
        """
        Работа с глобальными переменными и поиск `badruns`
        """
        dat_glob = ak.to_pandas(self.tree.arrays(['ebeam', 'emeas', 'lumoff', 'lumofferr', 'runnum', 'finalstate_id', 'trigbits']))
        badruns = np.loadtxt('pylib/badruns.dat')
        dat_glob['badrun'] = dat_glob.runnum.isin(badruns)
        return dat_glob
    def collinear_cut(df, col_th=0.25, col_phi=0.15, plot=False, return_pivot=False):
        """
        Кат на коллинеарность каонов: 0.25 по тета, 0.15 по фи
        return_pivot - вернуть (pd.Series, pd.Series) с коллинеарностями (для собственной отрисовки)
        """
        dtemp_th = df.groupby('entry').agg(th1=('ksth', 'first'), th2=('ksth', 'last'))
        coll_th = dtemp_th.loc[np.abs(dtemp_th.th1 + dtemp_th.th2 - np.pi) < col_th].index

        dtemp_ph = df.groupby('entry').agg(ph1=('ksphi', 'first'), ph2=('ksphi', 'last'))
        coll_ph = dtemp_ph.loc[np.abs( np.abs(dtemp_ph.ph2 - dtemp_ph.ph1) - np.pi) < col_phi].index
        
        if return_pivot:
            return (np.abs(dtemp_th.th1 + dtemp_th.th2 - np.pi), np.abs(np.abs(dtemp_ph.ph2 - dtemp_ph.ph1) - np.pi))

        if plot:
            fig, ax = plt.subplots(1, 2)
            ylabel = 'num of events per bin'
            ax[0].hist(np.abs(dtemp_th.th1 + dtemp_th.th2 - np.pi), 
                       bins=3*int(np.sqrt(len(dtemp_th))))
            ax[0].axvline(x=col_th, ymin=0, ymax=1, color='green')
            ax[0].set(xlim=(0, None), title='Collinearity $\\theta$',
                     xlabel='$\\Delta\\theta$', ylabel=ylabel)
            ax[1].hist(np.abs(np.abs(dtemp_ph.ph2 - dtemp_ph.ph1) - np.pi), 
                       bins=3*int(np.sqrt(len(dtemp_ph))))
            ax[1].axvline(x=col_phi, ymin=0, ymax=1, color='green')
            ax[1].set(xlim=(0, None), title='Collinearity $\\phi$',
                     xlabel='$\\Delta\\phi$', ylabel=ylabel)
            plt.tight_layout()

        return df.loc[coll_th.intersection(coll_ph)]
    def sum_energy_cut(df, cut_en=100, plot=False, return_pivot=False):
        """
        Кат на разницу энергии пары каонов и пучков 100 МэВ (default)
        return_pivot - вернуть pd.Series с полными энергиями (для собственной отрисовки)
        """
        dk = pd.pivot_table(
            df.reset_index(),
            index=['entry'],
            values=['ksminv', 'ksptot', 'ksth', 'ksphi', 'kslen'],
            columns=['subentry'],
        )
        dk.columns = ['_'.join(map(lambda x: str(x), col)) for col in dk.columns]

        total_en = np.sqrt( dk.ksptot_0**2 + dk.ksminv_1**2 ) + np.sqrt( dk.ksptot_1**2 + dk.ksminv_1**2 )
        
        if return_pivot:
            return total_en
        
        cal_en = df.emeas.mean()*2
        idx = dk.loc[ np.abs(total_en - cal_en)<cut_en ].index
        
        if plot:
            fig, ax = plt.subplots(1, 1)
            ylabel = 'num of events per bin'
            ax.hist(total_en, 
                       bins=3*int(np.sqrt(len(total_en))))
            ax.axvline(x=cal_en + cut_en, ymin=0, ymax=1, color='green')
            ax.axvline(x=cal_en - cut_en, ymin=0, ymax=1, color='green')
            ax.set(title='Total energy of the particles',
                     xlabel='Total energy, MeV', ylabel=ylabel)
            plt.tight_layout()
        
        return df.loc[idx]
    def kaon_mom_cut(df, cut_mom=60, plot=False):
        """
        Кат на импульс каона 60 МэВ
        """
        cal_mom = np.sqrt(df.emeas.mean()**2 - 497.6**2)
        fls = df.loc[ np.abs(df.ksptot - cal_mom) < cut_mom ]
        idx = fls.reset_index().groupby('entry').agg({'subentry' : 'count'}).query('subentry==2').index

        if plot:
            fig, ax = plt.subplots(1, 1)
            ylabel = 'num of events per bin'
            ax.hist(df.ksptot, 
                       bins=3*int(np.sqrt(len(df.ksptot))))
            ax.axvline(x=cal_mom + cut_mom, ymin=0, ymax=1, color='green')
            ax.axvline(x=cal_mom - cut_mom, ymin=0, ymax=1, color='green')
            ax.set(title='Momentum of the KS',
                     xlabel='Momentum, MeV', ylabel=ylabel)
            plt.tight_layout()
        
        return df.loc[idx]
    def flight_cut(df, cut_flight=0.1, plot=False):
        """
        Кат на отлёт 0.1 см
        """
        idx = df.loc[df.kslen > cut_flight].reset_index().groupby('entry').agg({'subentry': 'count'}).query('subentry==2').index
        
        if plot:
            fig, ax = plt.subplots(1, 1)
            ylabel = 'num of events per bin'
            ax.hist(df.kslen, 
                       bins=3*int(np.sqrt(len(df.kslen))))
            ax.axvline(x=cut_flight, ymin=0, ymax=1, color='green')
            ax.set(title='KS flight length, cm',
                     xlabel='Momentum, MeV', ylabel=ylabel)
            plt.tight_layout()
            
        
        return df.loc[idx]
    def ksminv_cut(df, cut_mass=25):
        """
        Кат на инв. массу 25 МэВ
        """
        idx = df.loc[(df.ksminv - 497.6) < cut_mass ].reset_index().groupby('entry').agg({'subentry': 'count'}).query('subentry==2').index
        return df.loc[idx]
        