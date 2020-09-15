#include "washer.h"

void Washer::InitBranches(){
    fChain->SetBranchAddress("ebeam", &ebeam, &b_ebeam);
    fChain->SetBranchAddress("emeas", &emeas, &b_emeas);
    fChain->SetBranchAddress("nt", &nt, &b_nt);
    fChain->SetBranchAddress("nks", &nks, &b_nks);
    fChain->SetBranchAddress("runnum", &runnum, &b_runnum);
    fChain->SetBranchAddress("tz", tz, &b_tz);
    fChain->SetBranchAddress("tchi2r", tchi2r, &b_tchi2r);
    fChain->SetBranchAddress("tchi2z", tchi2z, &b_tchi2z);
    fChain->SetBranchAddress("tcharge", tcharge, &b_tcharge);
    fChain->SetBranchAddress("tth", tth, &b_tth);
    fChain->SetBranchAddress("tptot", tptot, &b_tptot);
    fChain->SetBranchAddress("trho", trho, &b_trho);
    fChain->SetBranchAddress("tnhit", tnhit, &b_tnhit);
    fChain->SetBranchAddress("tdedx", tdedx, &b_tdedx);
    fChain->SetBranchAddress("kstype", kstype, &b_kstype);
    fChain->SetBranchAddress("ksvind", ksvind, &b_ksvind);
    fChain->SetBranchAddress("ksminv", ksminv, &b_ksminv);
    fChain->SetBranchAddress("ksalign", ksalign, &b_ksalign);
}

double Washer::PiDeDx(int i){
    double P = tptot[i], dEdX = tdedx[i];
    return 5.58030e+9 / pow(P + 40., 3) + 2.21228e+3 - 3.77103e-1 * P - dEdX;
}
