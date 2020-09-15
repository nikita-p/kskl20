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

void Washer::Loop(const std::vector<bool (Washer::*)()>& global_foos){
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
        tracks.clear();
        for(int i = 0; i<nt; i++){
            tracks.insert(i);
        }
        for(auto& foo : global_foos){
            passed[jentry] = ( passed[jentry] && (this->*foo)() );
            if (!passed[jentry])
                break;
        }
        // std::cout << jentry << ' ' << nt << ' ' << tracks.size() << ' ' << passed[jentry] << '\n';
        if (!passed[jentry] || tracks.size()!=2 )
            continue;
    }
}

void Save(std::string file){
    TFile *f = TFile::Open(file.c_str(), "recreate");
    return;
}

int Washer::StandardProcedure(){
    Loop({&Washer::FilterNTracks, &Washer::FilterNKaons, &Washer::FilterBadRun, 
          &Washer::FilterZ, &Washer::FilterChi2, &Washer::FilterMom,
          &Washer::FilterHits, &Washer::FilterRho, &Washer::FilterTheta,
          &Washer::FilterDeDx, 
          &Washer::FilterBestMass, &Washer::FilterKaonTracks, &Washer::FilterKaonAngle});
    return 0;
}
