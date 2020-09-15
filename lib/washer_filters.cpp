#include "washer.h"

bool Washer::FilterNTracks(){
    return (nt>=2);
}

bool Washer::FilterNKaons(){
    return (nks>0);
}

bool Washer::FilterZ(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (fabs(tz[*it]) < 10) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterChi2(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (tchi2r[*it] < 30) && (tchi2z[*it] < 25) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterMom(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (tptot[*it] > 40.) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterHits(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (tnhit[*it] > 6) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterRho(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (fabs(trho[*it]) > 0.1) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterTheta(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (tth[*it] > 0.6) && (tth[*it] < TMath::Pi() - 0.6) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterDeDx(){
    for(auto it = tracks.begin(); it!=tracks.end();){
        it = (fabs(this->PiDeDx(*it)) < 2000) ? ++it : tracks.erase(it);
    }
    return (tracks.size()>=2);
}

bool Washer::FilterBestMass(){
    double minDiv = TMath::Infinity();
    best_kaon = -1;
    for(int i = 0; i < nks; i++){
        if((TMath::Abs(ksminv[i] - mKs) < minDiv) && (kstype[i]==0)){
            best_kaon = i;
            minDiv = TMath::Abs(ksminv[i] - mKs);
        }
    }
    return (best_kaon>0);
}

bool Washer::FilterKaonTracks(){
    if(best_kaon<0 || best_kaon>=NK)
        return false;
    return (std::unordered_set<int>{ksvind[best_kaon][0], ksvind[best_kaon][1]} == tracks);
}

bool Washer::FilterKaonAngle(){
    return (ksalign[best_kaon]>0.8);
}