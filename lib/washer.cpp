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
        if(jentry%10000 == 0)
            cout << "Progress: " << int(jentry*100/nentries) << " %\r" << std::flush;
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
        cout << "Found\n";
        passed_events.push_back({jentry, best_kaon});
    }
}

void Washer::Save(std::string file){
    TFile *f = TFile::Open(file.c_str(), "recreate");
    TTree *t = new TTree("t", "Cutted tree");
    float tthc[2], tzc[2], tptotc[2], trhoc[2], tdedxc[2], tchi2rc[2], tchi2zc[2];
    int tnhitc[2];
    t->Branch("ebeam", &ebeam, "ebeam/D");
    t->Branch("emeas", &emeas, "emeas/D");
    t->Branch("trigbits", &trigbits, "trigbits/I");
    t->Branch("tth", &tthc, "tthc[2]/F");
    t->Branch("tz", &tzc, "tzc[2]/F");
    t->Branch("tptot", &tptotc, "tptotc[2]/F");
    t->Branch("trho", &trhoc, "trhoc[2]/F");
    t->Branch("tdedx", &tdedxc, "tdedxc[2]/F");
    t->Branch("tchi2r", &tchi2rc, "tchi2rc[2]/F");
    t->Branch("tchi2z", &tchi2zc, "tchi2zc[2]/F");
    t->Branch("tnhit", &tnhitc, "tnhitc[2]/I");
    t->Branch("ksminv", &ksminv, "ksminv/F");
    t->Branch("ksalign", &ksalign, "ksalign/F");
    
    Long64_t nbytes = 0, nb = 0;
    for(const auto& event : passed_events){
        Long64_t jentry = event.first;
        size_t kaon = event.second;
        Long64_t ientry = LoadTree(jentry);
        if ((ientry < 0) || (kaon<0) || (kaon>=nks))
            continue;
        nb = fChain->GetEntry(jentry);
        nbytes += nb;

        int t1 = ksvind[kaon][0], t2 = ksvind[kaon][1];

        int track{-1};
        for(int i=0; i<2; i++){
            track = ksvind[kaon][i];
            tthc[i] = tth[track];
            tptotc[i] = tptot[track];
            trhoc[i] = trho[track];
            tdedxc[i] = tdedx[track];
            tchi2rc[i] = tchi2r[track];
            tchi2zc[i] = tchi2z[track];
            tnhitc[i] = tnhit[track];
            ksminv[i] = ksminv[track];
            ksalign[i] = ksalign[track];
        }
        t->Fill();
    }
    t->Write();
    return;
}

int Washer::StandardProcedure(){
    Loop({&Washer::FilterNTracks, &Washer::FilterNKaons, &Washer::FilterBadRun, 
          &Washer::FilterZ, &Washer::FilterChi2, &Washer::FilterMom,
          &Washer::FilterHits, &Washer::FilterRho, &Washer::FilterTheta,
          &Washer::FilterDeDx,
          &Washer::FilterBestMass});//, &Washer::FilterKaonTracks, &Washer::FilterKaonAngle});
    return 0;
}
