import numpy as np
from scipy.integrate import quad
from typing import Union, List

class MDVM():
    """
    Фитировать сечения с помощью МДВМ
    
    ...
    
    Attributes
    ----------
    ALPHA : float
        alpha constant
    C : float
        conversion constant
    mPhi : float
        phi meson mass, MeV
    mRho : float
        rho meson mass, MeV
    mOmg : float
        omega meson mass, MeV
    mK0 : float
        neutral kaon mass, MeV
    mP0 : float
        neutral pion mass, MeV
    mKC : float
        charged kaon mass, MeV
    mPC : float
        charged pion mass, MeV
    mKstar : float
        K* mass, MeV
    w0Phi : float
        width of the phi meson, MeV
    w0Rho : float
        width of the rho meson, MeV
    w0Omg : float
        width of the omega meson, MeV    
    """
    
    def __init__(self):
        self.ALPHA = 7.297352e-3
        self.C = 0.3893793656e12 #(MeV)^2 * nb

        self.mPhi = 1019.464
        self.mRho = 775.26
        self.mOmg = 782.65

        self.mK0 = 497.611
        self.mP0 = 135.
        self.mKC = 493.677
        self.mPC = 139.57
        self.mKstar = 891.76

        self.w0Phi = 4.247
        self.w0Rho = 149.1
        self.w0Omg = 8.49
    
    def BETA(self, s: np.array, M_K: float) -> np.array:
        """
        Вычислить бета-фактор для частицы с массой M_K
        
        Parameters
        ----------
        s : numpy.array
            s, Mev^2
        M_K : float
            particle mass, MeV
            
        Returns
        -------
        beta : float
            beta-factor
        """
        
        E = np.sqrt(s)/2.
        P = np.where( E<M_K, 0, np.sqrt( E**2 - M_K**2 ) )
        return P/E
    
    def q(self, M: float, m1: float, m2: float) -> float:
        """
        Parameters
        ----------
        M : float
            масса распавшейся частицы
        m1 : float
            масса первой распадной частицы
        m2 : float
            масса второй распадной частицы
        
        Returns
        -------
        q : float
            безразмерный параметр q
        """
        
        return math.sqrt( (M**2 - (m1 - m2)**2 )*( M**2 - (m1 + m2)**2 ) )/(2*M)
    
    def PV2_diff(self, s: np.array, M: float, mi: float, mj: float) -> np.array:
        """
        Фазовый объём распада на 2 разные частицы https://arxiv.org/pdf/hep-ph/9609216.pdf (2.6)
        
        Parameters
        ----------
        s : numpy.array
            s, MeV^2
        M : float
            масса распавшейся частицы, MeV
        mi : float
            масса первой распадной частицы, MeV
        mj : float
            масса второй распадной частицы, MeV
        
        Returns
        -------
        float
            относительный фазовый объём распада на 2 разные частицы
        """
        
        q0 = np.sqrt( (M**2 - (mi - mj)**2)*(M**2 - (mi + mj)**2) )/(2*M)
        E = np.sqrt(s)
        q_temp = np.where( E <= (mi + mj), 0, (E**2 - (mi - mj)**2)*(E**2 - (mi + mj)**2) )
        q1 = np.sqrt( q_temp )/(2*E)
        return (q1/q0)**3
    
    def PV2(self, s: np.array, M: float, Mn: float) -> np.array:
        """
        Фазовый объём распада на 2 одинаковые частицы
        
        Parameters
        ----------
        s : np.array
            s, MeV^2
        M : float
            масса распавшейся частицы, MeV
        Mn : flaot
            масса частицы из распада, MeV
        
        Returns
        -------
        w : float
            фазовый объём
        """
        
        w = np.where(s <= 4*Mn*Mn, 0, np.power( (s - 4*Mn**2)/(M**2 - 4*Mn**2), 3./2 )*(M**2)/s )
        return w
    
    def FAS3_RhoPiPi(self, s: np.array) -> np.array:
        """
        Фазовый объём распада ро в 2 пи
        
        Parameters
        ----------
        s : numpy.array
            s, MeV^2
        
        Returns
        -------
        numpy.array
            фазовый объём
        """
        
        e = np.sqrt(s)*1e-3
        f1 = 1.9e-3 + 2.68e-2*(e-1.2) + 2.446e-1 * (e-1.2)**2 + 3.1487 * (e-1.2)**3 + 23.3131 * (e-1.2)**4 + 59.7669 * (e-1.2)**5
        f2 = 1.9e-3 + 2.33e-2*(e-1.2) + 6.65e-2 * (e-1.2)**2 - 3.84e-2 * (e-1.2)**3 + 2.36e-2 * (e-1.2)**4 - 6.5e-3 * (e-1.2)**5
        return np.where(e<1.2, f1, f2)
    
    def FAS3_OmgPiPi(self, s):        
        e = np.sqrt(s)*1e-3
        f1 = 1.7e-3 + 2.61e-2*(e-1.2) + 2.67e-1 * (e-1.2)**2 + 3.61199 * (e-1.2)**3 + 27.6 * (e-1.2)**4 + 73.6433 * (e-1.2)**5
        f2 = 1.7e-3 + 2.18e-2*(e-1.2) + 6.89e-2 * (e-1.2)**2 - 4.52e-2 * (e-1.2)**3 + 3.25e-2 * (e-1.2)**4 - 1.09e-2 * (e-1.2)**5
        return np.where(e<1.2, f1, f2)
    
    def FAS3(self, s):
        e = np.sqrt(s)*1e-3
        f1 = 5.196 + 59.17*(e-1) + 227.7 * (e-1)**2 + 147 * (e-1)**3 - 998 * (e-1)**4 - 1712 * (e-1)**5
        f2 = 5.196 + 80*(e-1) + 200 * (e-1)**2 + 590 * (e-1)**3 - 510 * (e-1)**4 + 220 * (e-1)**5
        return np.where(e<1, f1, f2)
    def PV3(self, s, MX, m1, m2, m3): #фазовый объём (почти: он типа нормирован) распада на 3 частицы
        #WARNING. TRY TO FIND THE RIGHT VARIANT
        pv = self.FAS3(s)
        pv0 = self.FAS3(MX**2)
        return pv/pv0
    def PVG(self, s, MX, Mn): #распад частицы M на фотон и частицу Mn
        pv  = ((s - Mn**2)/(2*np.sqrt(s)))**3
        pv0 = ((MX**2 - Mn**2)/(2*MX))**3
        return np.where(pv>0, pv/pv0, 0)
    def P_RhoPiPi(self, s, MX):
        return np.where( np.sqrt(s)>self.mRho+2*self.mP0, self.FAS3_RhoPiPi(s)/self.FAS3_RhoPiPi(MX**2), 0 )
    def P_OmgPiPi(self, s, MX):
        return np.where( np.sqrt(s)>self.mOmg+2*self.mP0, self.FAS3_OmgPiPi(s)/self.FAS3_OmgPiPi(MX**2), 0 )
    
    def WRho(self, s, W0, MX):
        return W0 * self.PV2(s, MX, self.mPC)
    def WOmg(self, s, W0, MX):    
        Br_3Pi = 0.892    
        Br_Pi0G = 0.084
        Br_2Pi = 0.0153
        ost = 1 - Br_Pi0G - Br_2Pi - Br_3Pi;
        
        mPC = self.mPC
        mP0 = self.mP0

        W = W0 * ((Br_3Pi + ost) * self.PV3(s, MX, mPC, mPC, mP0) + \
                  Br_Pi0G * self.PVG(s, MX, mP0) + Br_2Pi * self.PV2(s, MX, mPC));
        return W
    def WPhi(self, s, W0, MX):
        Br_KC = 0.492
        Br_KN = 0.34
        Br_3Pi = 0.1524
        Br_EG = 0.01303
        ost = 1 - Br_KC - Br_KN - Br_3Pi - Br_EG

        mEta = 547.862
        mKC = self.mKC
        mK0 = self.mK0
        mPC = self.mPC
        mP0 = self.mP0

        W = W0*((Br_KC + ost)* self.PV2(s, MX, mKC) + Br_KN* self.PV2(s, MX, mK0) + \
                Br_3Pi * self.PV3(s, MX, mPC, mPC, mP0) + Br_EG * self.PVG(s, MX, mEta));
        return W
    def WPhi1680(self, s, W0, MX): #fully KK* decay
        W = W0*self.PV2_diff(s, MX, self.mKC, self.mKstar)
        return W
    def WRho1(self, s, W0, MX): #\omega \pi
        return W0 * self.PV2_diff(s, MX, self.mP0, self.mOmg)
    def WRhoN(self, s, W0, MX): #\rho \pi \pi
        return W0 * self.P_RhoPiPi(s, MX)
    def WOmg1(self, s, W0, MX): #\rho \pi
        return W0 * self.PV2_diff(s, MX, self.mP0, self.mRho)
    def WOmgN(self, s, W0, MX): #\omega \pi \pi
        return W0 * self.P_OmgPiPi(s, MX)
    
    def WRhoX(self, s, W0, MX):
        return W0 * self.PV2(s, MX, self.mPC)
    def WOmgX(self, s, W0, MX):
        return W0 * self.PV2_diff(s, MX, self.mRho, self.mP0) #self.PV3(s, MX, self.mPC, self.mPC, self.mP0)
    def WPhiX(self, s, W0, MX):
        return W0 * self.PV2(s, MX, self.mKC)
    
    def BW(self, s, MX, WX0, WX): #функция Брейта-Вигнера
        bw = (MX**2)/( MX**2 - s - 1j*MX*WX(s, WX0, MX) )#np.sqrt(s)
        return bw
    def BW_RhoX(self, s, mX, wX):
        return self.BW(s, mX, wX, self.WRhoX)
    def BW_OmgX(self, s, mX, wX):
        return self.BW(s, mX, wX, self.WOmgX)
    def BW_PhiX(self, s, mX, wX):
        return self.BW(s, mX, wX, self.WPhiX)
    
    def BW_Rho(self, s):
        return self.BW(s, self.mRho, self.w0Rho, self.WRho)
    def BW_Omg(self, s):
        return self.BW(s, self.mOmg, self.w0Omg, self.WOmg)
    def BW_Phi(self, s):
        return self.BW(s, self.mPhi, self.w0Phi, self.WPhi)
    def BW_Rho1(self, s, m=1465, g=400):
        return self.BW(s, m, g, self.WRho1)#self.BW_RhoX(s, m, g)
    def BW_Rho3(self, s, m=1720, g=250):
        return self.BW(s, m, g, self.WRhoN)#self.BW_RhoX(s, m, g)
    def BW_Omg1(self, s, m=1420, g=220):
        return self.BW(s, m, g, self.WOmg1)#self.BW_OmgX(s, m, g)
    def BW_Omg2(self, s, m=1670, g=315):
        return self.BW(s, m, g, self.WOmgN)#self.BW_OmgX(s, m, g)
    def BW_Phi1(self, s, m=1673, g=182):
        return self.BW(s, m, g, self.WPhi1680)
    def BW_Phi2(self, s, m=2198, g=71):
        return self.BW(s, m, g, self.WPhi1680)#self.BW_PhiX(s, mPhi2, gPhi2)#BESIII:2239.2, 139.8 #PDG: 2198, 71 
    
    #PUBLIC
    def F0(self, x, KR, KO, KP, n): #формфактор, нулевое приближение; mode: 0 - short/long; 1 - charged;
        s = (x*1e3)**2 
        F = KR * self.BW_Rho(s) + KO * self.BW_Omg(s) + n * KP * self.BW_Phi(s)
        return F
    def F1(self, x, par, charged=False): #формфактор с учётом omega(1400)
        n = 1 if charged else par[0] #1.027
        s = (x*1e3)**2
        CR = np.array([par[1], par[2], par[3], 0])
        CR[-1] = 1 - CR.sum()
        CO = np.array([par[20], par[21], par[22], par[23]])
        CP = np.array([par[4], par[5], 0])
        CP[-1] = 3/2. - CO.sum()/2 - CP.sum()
#         print(CR, CO, CP)
        KR = CR/2. if charged else -CR/2.
        KO = CO/6.
        KP = CP/3.
        
        F1 = self.F0(x, KR[0], KO[0], KP[0], n)
        m3, w3 = par[6], par[7] #2150, 350
        m4, w4 = par[8], par[9]
        m5, w5 = par[10], par[11]
        m6, w6 = par[12], par[13]
        m1, w1 = par[14], par[15]
        m2, w2 = par[16], par[17]        
        m7, w7 = par[18], par[19]
        F1 += KR[1] * self.BW_Rho1(s, m1, w1) + KR[2] * self.BW_Rho3(s, m3, w3) + KR[3] * self.BW_Rho3(s, m6, w6)
        F1 += KO[1] * self.BW_Omg1(s, m2, w2) + KO[2] * self.BW_Omg2(s, m4, w4) + KO[3] * self.BW_Omg2(s, m6, w6) 
        F1 += KP[1] * self.BW_Phi1(s, m5, w5) + KP[2] * self.BW_Phi2(s, m7, w7)
        return F1
        
    def Cross_Section(self, x: np.array, par: List[float], charged: bool = False) -> np.array:
        """
        Получить сечение e+e- -> KSKL или e+e- -> K+K-, используя параметры
        
        Parameters
        ----------
        x : numpy.array
            набор s, в которых нужно вернуть сечение, GeV^2
        par : List[float]
            список параметров для вычисления формфактора
        charged : bool
            сечение в заряженные (True) или нейтральные (False) каоны нужно вернуть (default is False)
            
        Returns
        -------
        cs : numpy.array
            сечение в точках x
        """
        
        s = (x*1e3)**2
        fabs2 = np.abs( self.F1(x, par, charged) )**2
        M_K = self.mKC if charged else self.mK0
        constant = (np.pi/3.) * (self.ALPHA**2) * self.C
        cs = np.where( x<0.4976*2, 0, constant * (self.BETA(s, M_K)**3) * fabs2 / s  )
        return cs
    
    def Cross_Section_Neutral(self, x, par):
        """
        Получить сечение e+e- -> KSKL, используя параметры
        
        Parameters
        ----------
        x : numpy.array
            набор s, в которых нужно вернуть сечение, GeV^2
        par : List[float]
            список параметров для вычисления формфактора
            
        Returns
        -------
        cs : numpy.array
            сечение в точках x
        """
        
        return self.Cross_Section(x, par, False)
    
    def Cross_Section_Charged(self, x, par):
        """
        Получить сечение e+e- -> K+K-, используя параметры
        
        Parameters
        ----------
        x : numpy.array
            набор s, в которых нужно вернуть сечение, GeV^2
        par : List[float]
            список параметров для вычисления формфактора
            
        Returns
        -------
        cs : numpy.array
            сечение в точках x
        """
        
        return self.Cross_Section(x, par, True)    
    
    def Cross_Section2Formfacror(self, x, cs, mode=False):
        """
        Перевести сечение в формфактор
        
        Parameters
        ----------
        x : numpy.array
            набор s, в которых нужно вернуть формфактор, GeV^2
        cs : numpy.array
            список сечений в точках x, nb
        mode : bool
            использовать заряженный (True) или нейтральный каон (False) (default is False)
            
        Returns
        -------
        numpy.array
            формфактор
        """
        
        s = (x*1e3)**2
        M_K = self.mKC if mode else self.mK0
        constant = (np.pi/3.) * (self.ALPHA**2) * self.C
        return cs*s/(constant * ( self.BETA(s, M_K)**3 ) )