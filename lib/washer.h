#pragma once
#include <fstream>
#include <iostream>
#include <vector>
#include <functional>

#include <TROOT.h>
#include <TTree.h>
#include <TChain.h>
#include <TFile.h>
#include <TMath.h>
#include <TMatrix.h>
// #include "/storeA/ryzhenenkov/badrunfunction.C" //lums

#define mKs 497.614
#define mPi 139.570

class Washer{
    std::vector<std::string> trees;
    TChain* fChain;
    std::vector<bool> passed;

    Float_t ebeam;
    TBranch *b_ebeam;
    Int_t nt;
    TBranch *b_nt;
    Int_t nks;
    TBranch *b_nks;

    //Hide vars and methods
    int fCurrent;
    Long64_t LoadTree(Long64_t entry);
    void InitBranches();

    int StandardProcedure();

  public:

    //Filter methods: one entry input -> true/false output
    bool FilterNTracks();
    bool FilterNKaons();
    bool FilterZ(int i);
    bool FilterChi2(int i);
    bool FilterMom(int i);
    bool FilterHits(int i);
    bool FilterRho(int i);
    bool FilterTheta(int i);
    bool FilterPolarAngle();
    bool FilterDeDx();
    bool FilterBestMass();

    Washer();
    Washer(const std::string& path);
    Washer(const std::vector<std::string>& pathes);

    void GetPassedVector();
    bool Loop(std::vector<bool (Washer::*)()> foos);
    int Roll(); //compute full analysis
//     std::ostream& operator<<(std::ostream&, TTree&); //print the Tree in file (or terminal)
    void Save(std::string file, std::vector<std::string> fields);
    void Print();
};
