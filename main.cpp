#include "lib/washer.h"
#include <iostream>

using namespace std;

int main(){
  Washer a(vector<string>{"root://sl10cmd//scan2019/scan2019_tr_ph_fc_e550_v7.root",
                          "root://sl10cmd//scan2019/scan2019_tr_ph_fc_e800_v7.root"});
//   Washer a("data/trees_mc2019.txt");
  a.Loop({&Washer::FilterNTracks, &Washer::FilterNKaons, &Washer::FilterBadRun, 
          &Washer::FilterDeDx, &Washer::FilterHits, &Washer::FilterRho,
          &Washer::FilterBestMass, &Washer::FilterKaonTracks, &Washer::FilterKaonAngle, 
          &Washer::FilterKaonMom});
  a.Save("/spoolA/petrov/refac20/trees/exp2019_550_800.root");
  return 0;
}
