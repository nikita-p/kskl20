#include "lib/washer.h"
#include <iostream>

using namespace std;

int main(){
    // Washer a(vector<string>{"root://cmd//scan2011/scan2011_tr_ph_fc_e525_v7.root"});//, "root://cmd//scan2011/scan2011_tr_ph_fc_e550_v7.root"});
    // a.StandardProcedure();
    Washer a("data/trees_exp2011.txt");
    a.Loop({&Washer::FilterNTracks, &Washer::FilterNKaons, &Washer::FilterBadRun, 
          &Washer::FilterZ, &Washer::FilterChi2, &Washer::FilterMom,
          &Washer::FilterHits, &Washer::FilterRho,
          &Washer::FilterDeDx,
          &Washer::FilterBestMass, &Washer::FilterKaonTracks, &Washer::FilterKaonAngle});
    a.Save("/spoolA/petrov/refac20/trees/exp2011.root");
    return 0;
}
