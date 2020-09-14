#include "washer.h"

Washer::Washer(const std::string& path): trees({path}), fCurrent(-1){
    fChain = new TChain("tr_ph");
    fChain->Add(path.c_str());
    passed = std::vector<bool>(fChain->GetEntries(), true);
    InitBranches();
}

Washer::Washer(const std::vector<std::string>& pathes): trees(pathes), fCurrent(-1){
    fChain = new TChain("tr_ph");
    for(auto& str: pathes)
        fChain->Add(str.c_str());
    passed = std::vector<bool>(fChain->GetEntries(), true);
    InitBranches();
}

void Washer::Print(){
    fChain->Print();
    return;
}

void Washer::GetPassedVector(){
    for(auto b : passed){
        std::cout << b << ' ';
    }
    std::cout << std::endl;
    return;
}

Long64_t Washer::LoadTree(Long64_t entry){
    if (!fChain)
      return -5;
    Long64_t centry = fChain->LoadTree(entry);
    if (centry < 0)
        return centry;
    if (fChain->GetTreeNumber() != fCurrent){
        fCurrent = fChain->GetTreeNumber();
    }
    return centry;
}

void Washer::Loop(const std::vector<bool (Washer::*)()>& global_foos,
                  const std::vector<bool (Washer::*)(int)>& good_tracks_foos){
    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t nbytes = 0, nb = 0;

    for (Long64_t jentry = 0; jentry < nentries; jentry++){ //nentries
        Long64_t ientry = LoadTree(jentry);
        if (!passed[jentry])
            continue;
        if (ientry < 0)
            break;
        nb = fChain->GetEntry(jentry);
        nbytes += nb;
        for(auto& foo : global_foos){
            passed[jentry] = ( passed[jentry] && (this->*foo)() );
            // std::cout << passed[jentry] << ' ';
        }
        if (!passed[jentry])
            continue;
        int good_tracks = 0;
        bool accepted_track = true;
        for(int i=0; i<nt; i++){
            for(auto& foo : good_tracks_foos){
                accepted_track = ( accepted_track && (this->*foo)(i) );
                if(!accepted_track)
                    break;
            }
            good_tracks += accepted_track;
        }
        passed[jentry] = ( passed[jentry] && (good_tracks==2) );
        std::cout << passed[jentry] << ' ';
    }
}

int Washer::StandardProcedure(){
    Loop({&Washer::FilterNTracks, &Washer::FilterNKaons},
         {&Washer::FilterZ, &Washer::FilterChi2, &Washer::FilterMom,
          &Washer::FilterHits, &Washer::FilterRho, &Washer::FilterTheta,
          &Washer::FilterDeDx});
    return 0;
}
