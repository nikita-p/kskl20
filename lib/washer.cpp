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

void Washer::InitBranches(){
    fChain->SetBranchAddress("ebeam", &ebeam, &b_ebeam);
    fChain->SetBranchAddress("nt", &nt, &b_nt);
    fChain->SetBranchAddress("nks", &nks, &b_nks);
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

bool Washer::Loop(std::vector<bool (Washer::*)()> foos){
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
        for(auto& foo : foos){
            passed[jentry] = ( passed[jentry] && (this->*foo)() ) ? true : false;
            std::cout << passed[jentry] << ' ';
        }
    }

}
