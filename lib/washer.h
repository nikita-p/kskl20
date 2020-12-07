#pragma once
#include <fstream>
#include <iostream>
#include <vector>
#include <list>
#include <unordered_set>

#include <TROOT.h>
#include <TTree.h>
#include <TChain.h>
#include <TFile.h>
#include <TMath.h>
#include <TMatrix.h>

#include <omp.h>

#define mKs 497.614
#define mPi 139.570
#define NT 15
#define NK 15
#define NSIM 15

using std::cout;
using std::endl;

bool badrun(int runnum);

class Washer{
    std::vector<std::string> trees;
    TChain* fChain;
    std::vector<bool> passed;
    std::list<std::pair<Long64_t, size_t>> passed_events;
    std::vector<short> good_kaons;

    Float_t ebeam;
    TBranch *b_ebeam;
    Float_t emeas;
    TBranch *b_emeas;
    Int_t nt;
    TBranch *b_nt;
    Int_t nks;
    TBranch *b_nks;
    Int_t runnum;
    TBranch *b_runnum;
    Int_t trigbits;
    TBranch *b_trigbits;
    Float_t tth[NT];
    TBranch *b_tth;
    Float_t tz[NT];
    TBranch *b_tz;
    Float_t tptot[NT];
    TBranch *b_tptot;
    Float_t trho[NT];
    TBranch *b_trho;
    Int_t tnhit[NT];
    TBranch *b_tnhit;
    Float_t tdedx[NT];
    TBranch *b_tdedx;
    Float_t tchi2r[NT];
    TBranch *b_tchi2r;
    Float_t tchi2z[NT];
    TBranch *b_tchi2z;
    Int_t tcharge[NT];
    TBranch *b_tcharge;
    Int_t kstype[NK];
    TBranch *b_kstype;
    Int_t ksvind[NK][2];
    TBranch *b_ksvind;
    Float_t ksminv[NK];
    TBranch *b_ksminv;
    Float_t ksptot[NK];
    TBranch *b_ksptot;
    Float_t ksalign[NK];
    TBranch *b_ksalign;
    Float_t kslen[NK];
    TBranch *b_kslen;
    Float_t ksth[NK];
    TBranch *b_ksth;
    Float_t ksdpsi[NK];
    TBranch *b_ksdpsi;
    Float_t kspipt[NK][2];
    TBranch *b_kspipt;
    Int_t nsim;
    TBranch *b_nsim;
    Int_t simtype[NSIM];
    TBranch *b_simtype;
    Int_t simorig[NSIM];
    TBranch *b_simorig;
    Float_t simmom[NSIM];
    TBranch *b_simmom;

    //Hide vars and methods
    std::unordered_set<int> tracks;
    size_t best_kaon;
    int fCurrent;
    Long64_t LoadTree(Long64_t entry);
    void InitBranches();

    double PiDeDx(int i);

  public:

    //Filter methods: one entry input -> true/false output
    bool FilterNTracks();
    bool FilterNKaons();
    bool FilterBadRun();
    bool FilterZ();
    bool FilterChi2();
    bool FilterMom();
    bool FilterHits();
    bool FilterRho();
    bool FilterTheta();
    bool FilterDeDx();
    bool FilterBestMass();
    bool FilterKaonTracks();
    bool FilterKaonAngle();
    bool FilterKaonMom();

    Washer();
    Washer(const std::string& path);
    Washer(const std::vector<std::string>& pathes);

    void GetPassedVector();
    void Loop(const std::vector<bool (Washer::*)()>& global_foos);
    int StandardProcedure();
    int Roll(); //compute full analysis
    void Save(std::string file);
    void Print();
};
