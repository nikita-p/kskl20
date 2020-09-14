#include "washer.h"

bool Washer::FilterNTracks(){
    return (nt>=2);
}

bool Washer::FilterNKaons(){
    return (nks>0);
}

bool Washer::FilterZ(int i){
    return fabs(tz[i]) < 10;
}

bool Washer::FilterChi2(int i){
    return (tchi2r[i] < 30) && (tchi2z[i] < 25);
}

bool Washer::FilterMom(int i){
    return (tptot[i] > 40.);
}

bool Washer::FilterHits(int i){
    return tnhit[i] > 6;
}

bool Washer::FilterRho(int i){
    return fabs(trho[i]) > 0.1;
}

bool Washer::FilterTheta(int i){
    return (tth[i] > 0.6) && (tth[i] < TMath::Pi() - 0.6);
}


std::vector<int> GoodTracks(){
    for( int i=0; i<nt; i++){
        if(fabs(tz[]))
    }
}
