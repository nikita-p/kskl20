#include "lib/washer.h"
#include <iostream>

using namespace std;

int main(int argc, char *argv[]){
  Washer a(argv[1]);
  a.Loop({&Washer::FilterNTracks, &Washer::FilterNKaons, &Washer::FilterBadRun, 
          &Washer::FilterDeDx, &Washer::FilterHits, &Washer::FilterRho,
          &Washer::FilterBestMass, &Washer::FilterKaonTracks});
  a.Save(argv[2]);
  return 0;
}
