#include "lib/washer.h"
#include <iostream>

using namespace std;

int main(){
    Washer a(vector<string>{"root://cmd//scan2011/scan2011_tr_ph_fc_e525_v7.root", "root://cmd//scan2011/scan2011_tr_ph_fc_e550_v7.root"});
    a.Loop({&Washer::FilterNTracks, &Washer::FilterNKaons}, {&Washer::FilterZ});
    a.GetPassedVector();
    return 0;
}
