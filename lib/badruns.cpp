//Время от времени обновлять по адресу: /storeA/ryzhenenkov/badrunfunction.C 
//Сейчас используется версия от 2 июля 2020.

bool badrun(int runnum)
{	
	//2011
	if (runnum == 9238 ) return 1; //ttt     Edc=18% 
	if (runnum == 9355 ) return 1; //ttt Edc=89%
	if (runnum == 9673 ) return 1; // Nee==0
	if (runnum == 10344 ) return 1;//ttt   Edc=75%
	if (runnum == 10272 ) return 1; //   Nee==3 e+ beam only
	if (runnum == 10273 ) return 1;//   Nee==3 e+ beam only
	if (runnum == 10325 ) return 1;//   Nee==0
	if (runnum == 10351 ) return 1;//  Nee==0 
	if (runnum == 10390 ) return 1;//  Nee==0 
	if (runnum == 10466 ) return 1;//  Nee==0 
	if (runnum == 10467 ) return 1;//tt//   Edc==58%
	if (runnum == 10470 ) return 1;//tt//   Edc==86%
	if (runnum == 10698 ) return 1;//tt//   Edc==78%
	if (runnum == 10835 ) return 1;//tt//   Nee==0
	if (runnum == 11136 ) return 1;//tt//   Edc==71%, no up-out crate
	if (runnum == 11205 ) return 1;//   
	if (runnum == 11252 ) return 1;//   Nee==0 
	if (runnum == 11353 ) return 1;//tt//   Edc==77%
	if (runnum == 11412 ) return 1;//   Nee==0
	if (runnum == 11739 ) return 1;//   Nee==0
	if (runnum == 11744 ) return 1;//   Nee==0
	if (runnum == 12287 ) return 1;//   Nee==0

	if (runnum == 12470 ) return 1;//t 687// Nee==0, Elxe=70%  
	if (runnum == 12477 ) return 1;//t 687//  Nee==0, Elxe=70% 
	if (runnum == 12478 ) return 1;//t 687//   Nee==0, Lxe - OFF
	if (runnum == 12479 ) return 1;//t 687//   Nee==0, Lxe - OFF
	if (runnum == 12480 ) return 1;//t 687//   Nee==0, Lxe - OFF
	if (runnum == 12481 ) return 1;//t 687//   Nee==0, Lxe - OFF
	if (runnum == 12482 ) return 1;//t 687//  Nee==0, Lxe - OFF 
//   
	if (runnum == 12698 ) return 1;//tt//   Nee==0 ??? Why?
	if (runnum == 12792 ) return 1;//tt//   Edc==71%
	if (runnum == 13124 ) return 1;//   Nee==0 ???
	//2012
	if (runnum == 26581 ) return 1;//   Edc=70%, dc-off after 130k
	if (runnum == 16368 ) return 1;//   Nee==0 e- beam only
	if (runnum == 16369 ) return 1;//   Nee==0 N==214k e- beam only
	if (runnum == 16370 ) return 1;//   Nee==0 N==211k e- beam only
	if (runnum == 16371 ) return 1;//   Nee==0 N==213k e- beam only
	if (runnum == 16372 ) return 1;//   Nee==0 N==128k e- beam only
	if (runnum == 16378 ) return 1;//   Edc=29%
	if (runnum == 16376 ) return 1;//   Very shady run
	if (runnum == 16279 ) return 1;//   Nee==0 N=348
	if (runnum == 15839 ) return 1;//   No tracks in down outer part, Edc=75%
	if (runnum == 15879 ) return 1;//   Very strange run, very strange comment, Edc=85%
	if (runnum == 15774 ) return 1;//   bad Edc=95%, in the end of run DC is off
	if (runnum == 15672 ) return 1;//   Nee==0 N==13
	if (runnum == 15135 ) return 1;//   bad Edc=84%, in the middle of run DC is off
	if (runnum >= 15825 && runnum<=15834  ) return 1;//  Nee==1,2, Only e- beam 
	//2013
	if (runnum == 17667 ) return 1;//508 omega//  Edc=50%, dc-off after 100k 
	if (runnum == 17813 ) return 1; // 512//   bad dc
//rho2013
	if (runnum == 19704  ) return 1;//   Edc=60%, dc-off after 75k 
	if (runnum == 19585  ) return 1;//   Edc=75%, dc-off after 140k
	if (runnum == 19587  ) return 1;//   Edc=75%, dc-off after 200k
	if (runnum == 20063  ) return 1;//   Edc=75%, dc-off after 200k
	if (runnum == 20064  ) return 1;//   Edc=75%, dc-off after 200k
	if (runnum == 20063  ) return 1;//   
	if (runnum == 23283  ) return 1;//   Edc=75%, dc-off after 200k 
	if (runnum == 23284  ) return 1;//   Edc=0%, all run bad
	if (runnum == 23463 ) return 1;// 17  upalo visokoe 200//   
	if (runnum == 22604  ) return 1;//   Edc=
	if (runnum == 22643  ) return 1;//   Edc=
	if (runnum == 22650  ) return 1;//   Edc=
	if (runnum == 22728  ) return 1;//   Edc=
	if (runnum == 22349  ) return 1;//   Edc=
	if (runnum == 22218  ) return 1;//   Edc=
	if (runnum == 22260  ) return 1;//   Edc=
	if (runnum == 22263  ) return 1;//   Edc=


if( runnum>=20071 && runnum <=20233) return 1;// E=391.5 MeV,  Problems with Energy in LXE
if( runnum>=20234 && runnum <=20241) return 1;// E=390.5 MeV,  Problems with Energy in LXE, same

if( runnum>=22453 && runnum <=22457) return 1;// E=290 MeV, larger tail on energy,  Problems with Energy 


//phi 2013
	if (runnum == 28517  ) return 1;//   Edc=80%, dc-off after 200k
	if (runnum == 28538  ) return 1;//   Edc=50%, dc-off after 100k
	if (runnum == 28619  ) return 1;//   Edc=50%, dc-off after 100k
	if (runnum == 28633  ) return 1;//   Edc=50%, dc-off after 100k
	if (runnum == 28634  ) return 1;//   Edc=50%, dc-off!
	if (runnum == 28661  ) return 1;//   Edc=50%, dc-off after 100k
	if (runnum == 28792  ) return 1;//   Edc=50%, dc-off after 80k
	if (runnum == 28054  ) return 1;//   Edc=80%, dc-off after 200k
	if (runnum == 28221  ) return 1;//   Edc=80%, bad dc
	if (runnum == 28225  ) return 1;//   bad dc
	if (runnum == 28434  ) return 1;//   Edc=0%, dc-off after 10k
	if (runnum == 27416  ) return 1;//   Edc=80%, dc-off after 200k
	if (runnum == 27421  ) return 1;//   bad dc-off
	if (runnum == 27423  ) return 1;//   Edc=0%, dc-off after 10k
	if (runnum == 27481  ) return 1;//   Edc=95%
	if (runnum == 27289  ) return 1;//   Edc=%, dc-off after 50k
	if (runnum == 27373  ) return 1;//   Edc=%, dc-off after 150k
	if (runnum == 27374  ) return 1;//   Edc=0%, dc-off

	if (runnum == 30975) return 1;//   Edc
	if (runnum == 30979) return 1;//   Edc
	if (runnum == 30984) return 1;//   Edc
	if (runnum == 31006) return 1;//   Edc
	if (runnum == 31017) return 1;//   Edc
	if (runnum == 31024) return 1;//   Edc
	if (runnum == 31036) return 1;//   Edc
	if (runnum == 31040) return 1;//   Edc
	if (runnum == 31042) return 1;//   Edc
	if (runnum == 31054) return 1;//   Edc
	if (runnum == 31055) return 1;//   Edc
	if (runnum == 31060) return 1;//   Edc
	if (runnum == 31063) return 1;//   Edc
	if (runnum == 31064) return 1;//   Edc

        // phi2013
	if (runnum == 26581 ) return 1; // 525 phi13//   

// -- HIGHI 2017 -----------------------------------------------------------------------------------------------------------
	if (runnum == 39951 || runnum == 39952 || runnum == 39953) return 1;
	
	if ( runnum >= 41420 && runnum <= 41700 )  return 1; //2017  936 kolbas // не было фазы все выходные

	if ( runnum==42476 || (runnum>=42480 && runnum <=42499) || runnum==42525)  return 1;  //2017  960 kolbas // bad events 50%
	if ( runnum >= 43691 && runnum <= 43743)  return 1; //2017  938.9 doubled banks 


	//skip runs with bad trigger and DC eficiency
	if(runnum==42476 || (runnum>=42480 && runnum <=42499) || runnum==42525) return 1;// E=960 MeV
	if(runnum==43080 || runnum==43081) return 1;// E=990 MeV
	if(runnum==40800 || runnum==40932 || runnum==40933 || runnum==40934 || runnum==40980 ||
		runnum==41378 || runnum==41379 || (runnum>41406 && runnum <41733)||
		runnum==41737 || runnum==41738 || runnum==41747 || runnum==41748 ||
		runnum==41752 || runnum==41753 || runnum==41754 || runnum==41755 || 
		runnum==41766  )  return 1;//E=936
	if(runnum==41812 || runnum==41813 || runnum==41814 ||
		(runnum>41822 && runnum <41842)||
		runnum==41865 || runnum==41869 || runnum==41870 ||
		runnum==41871 || runnum==41875 || runnum==41887 ||
		runnum==41937 || runnum==41942 || runnum==41948 ||
		runnum==41972 || runnum==41973 || runnum==41975  ) return 1;//E=942
	if(runnum==43753 || runnum==43754 || runnum==43755 ||
		runnum==43756 || runnum==43818 || runnum==43841 || runnum==43876 ||
		runnum==43891 || runnum==43892 || runnum==43913 ||
		runnum==43966 || runnum==43970  ) return 1;//E=938.9

	if(runnum==44052 || runnum==44053 || runnum==44209 ||
		runnum==44211 || runnum==44244 || runnum==44246 || 
		runnum==44247 || runnum==44248  ) return 1;//E=939.6

	if(runnum==44268 || runnum==44269 || runnum==44332 || runnum==44387  ) return 1;//E=940.2

	if(runnum==44476 || runnum==44554 || runnum==44555 || runnum==44623 || runnum==44624) return 1;//E=938.3

	if(runnum==44702 || runnum==44703 || runnum==44747 || (runnum>44809 && runnum <44828) ) return 1;//E=937.5

	if(runnum==45002 || runnum==45003 || runnum==45008 || (runnum>=45011 && runnum<=45018) ||
	   runnum==45021 || runnum==45027 || runnum==45047 || runnum==45048 || runnum==45064 ||  
		(runnum>45136 && runnum <45153) ) return 1;//E=940.8

	/*if(runnum==45011 || runnum==45027 || runnum==45047 || runnum==45048 || runnum==45064 ||
		(runnum>45136 && runnum <45153) ) return 1;//E=940.8*/

	if(runnum==45212  ) return 1;//E=937.5
//----------------------------------------------------------------------------------------------------------------
		if(runnum== 37087 || runnum==37159 || runnum==37160 || runnum==37161 ) return 1;//E=509.8
		if(runnum== 46515 || runnum==46516) return 1;//E=675
		if(runnum==46030 ) return 1;//E=725
		if(runnum==45498  || runnum==45497 || runnum==45499) return 1;//E=825

		if(runnum== 38128  || runnum==38157 || runnum==38275) return 1;//E=850

			if( runnum==39137  || runnum==39178 || runnum==39179 || runnum==39196  || runnum==39207
			 || runnum==39380  || runnum==39394 || runnum==39408 || runnum==39425 ) return 1;//E=880

		if(runnum==39642 || runnum==39654 || runnum==39655 || runnum==39656 || runnum== 39724 
		|| runnum==39716 || runnum==39717 || runnum==39718 || runnum==39729
		|| runnum==39765 || runnum==39766 || runnum==39773 || runnum==39779
		|| runnum==39839 || runnum==39873 ) return 1;	// 890


		if(runnum==41404  ) return 1;//E=936
		if(runnum==45022  ) return 1;//E=940.8
		if(runnum==43409 ) return 1;//E=1003.5
		//if(runnum==  ) return 1;//E=
		//if(runnum==  ) return 1;//E=
		//if(runnum==  ) return 1;//E=
	
	if(runnum==39877  ) return 1;//E=890  2017
	if(runnum==39693  ) return 1;//E=890  2017
	
	if(runnum>=45448 && runnum<=45487)  return 1;//E=840  (2017) плохая эфф ДК, вся ночная смена Kulidzhoglyan, Karpov


//---------Phi omega 2018  sid=8-----------------------------------------------------------------------
	if(runnum>=68423 && runnum<=68475) return 1;//E=340
	if(runnum==58225 ) return 1;//E=375   nh
	if(runnum==64749 ) return 1;//E=389   nh
	if(runnum==65299 || runnum==65300) return 1;//E=390.5   no tracks
	if(runnum==67490 || runnum==67491 || runnum==67629) return 1;//E=392.5 no tracks
	
	if(runnum==67860 ) return 1;//E=394	no tracks
	if(runnum==58466 ) return 1;//E=455	no tracks
	if(runnum==58772 ) return 1;//E=465	no tracks
	if(runnum==62227 ) return 1;//E=511 bad dc eff
	if(runnum==63171 ) return 1;//E=575 bad dc eff
	
	if(runnum==59872 || runnum==59873 || runnum==59875 
	|| runnum==59876 || runnum==59877|| runnum==59878 || runnum==59880 || runnum==59882
	 || runnum==59884 || runnum==59888 || runnum==59889 || runnum==59891 || runnum==59894
	  || runnum==59897 || runnum==59898 || runnum==59899 || runnum==59901 || runnum==59904
	   || runnum==59907 || runnum==59908 || runnum==59910 || runnum==59911 || runnum==59914
	    || runnum==59915 || runnum==59916 || runnum==59919 || runnum==59920 || runnum==59921 
	    || runnum==59923 || runnum==59926 || runnum==59927 || runnum==59928 || runnum==59929
	    || runnum==59930 || runnum==59933 || runnum==59935 || runnum==59936 || runnum==59937
	    || runnum==59938 || runnum==59941 || runnum==59942 || runnum==59944 || runnum==59945
	     || runnum==59950 || runnum==59953 || runnum==59954 || runnum==59955)  return 1;//E=505	problems with nhits

	if(runnum==59905 || runnum==59906 || runnum==59925 || runnum==59934)  return 1;//E=505	nt=0 and problems with nhits
	
	if( runnum>=64165 && runnum <=64297) return 1;// E=380 !! Problems with Energy in CSI
	if( runnum>=64298 && runnum <=64344) return 1;// E=387.5 !! Problems with Energy in CSI

	//510 L2014 r-61380-61858
	//510 L947  r-49070-49331
	
//---------RHO 2017-2018  sid=7-----------------------------------------------------------------------
	if(runnum==48954 ) return 1;//E=500	no tracks
	if(runnum==52946 ) return 1;//E=362	reason 3
	if(runnum==51159 ) return 1;//E=392	no tracks
	if(runnum==50083 ) return 1;//E=440 bad dc eff
	
	if(runnum==49173 ) return 1;//E=510 bad dc eff 
	if(runnum==49170 || runnum==49171) return 1;//E=510  problems with nh
	if(runnum==49173 || runnum==49174 || runnum==49175) return 1;//E=510	no tracks
	//if(runnum== 49175) return 1;//E=
//----------------------------------------------------------------------------------------------------

//----HIGHI 2019    sid=9-----------------------------------------------------------------------------
	if(runnum==70037 ) return 1;//550.1 	bad dc eff
	if(runnum==70049 ) return 1;//550.1 	bad dc eff
	if(runnum==82927 || runnum==82928|| runnum==82931 || runnum==82932 ||
	    runnum==82934 || runnum==82943|| runnum==82948|| runnum==82955) return 1;// 641	bad dc eff
	if(runnum==82940 || runnum==82958|| runnum==82959 || runnum==83144) return 1;// 641	very bad dc eff
	if(runnum==74232 ) return 1;// 687.5	bad dc eff
	if(runnum==78382 || runnum==78383) return 1;// 887.5  bad dc eff, 1 only track

	if(runnum==81775 || runnum==81777 || runnum==81778 || runnum==81781 ||
	   runnum==81782 || runnum==81783 || runnum==81784 || runnum==81785 ||
	   runnum==81786 || runnum==81787 || runnum==81788 || runnum==81789 ||
	   runnum==81790 || runnum==81792 || runnum==81793 || runnum==81794 ||
	   runnum==81795 || runnum==81796 || runnum==81797 ) return 1;// 955  ,dc eff, strange massive
	
	if(runnum>=81797 && runnum<=81869) return 1;  //E=955  dc eff, strange massive

	if(runnum==81776 || runnum==81779 || runnum==81780 || runnum==81791) return 1;//  955	 no tracks

	if(runnum==80402 ) return 1;// 962.5	bad dc eff
	if(runnum==81536 ) return 1;// 987.5	no tracks
	
//----LOW 2019    sid=10-----------------------------------------------------------------------------
	if(runnum>=87182 && runnum<=87185 ) return 1;// 240 no tracks, trb 3!!!
	
//----HIGH 2020   sid=11-----------------------------------------------------------------------------
	if(runnum==91236) return 1;// 935.0	no tracks trb 3!
	if(runnum==91238) return 1;// 935.0	no tracks
	
	if(runnum==91920) return 1;// 945.0	no tracks trb 2
	if(runnum==92012) return 1;// 945.0	no tracks trb 2
	if(runnum==92143) return 1;// 945.0	no tracks trb 2
	if(runnum==92215) return 1;// 945.0	no tracks trb 2
	if(runnum==92217) return 1;// 945.0	no tracks trb 2
	if(runnum==92272) return 1;// 945.0	no tracks trb 2
	if(runnum==92325) return 1;// 945.0	no trackstrb 2
	if(runnum==92391) return 1;// 945.0	no tracks trb 2
	if(runnum==92455) return 1;// 945.0	no trackstrb 2
	if(runnum==92499) return 1;// 945.0	no tracks trb 2
	if(runnum==92574) return 1;// 945.0	no tracks trb 2
	if(runnum==92625 || runnum==92626) return 1;// 945.0	no tracks trb 2
	if(runnum==92643) return 1;// 945.0	no tracks trb 2
	if(runnum==92649) return 1;// 945.0	no tracks trb 2
	if(runnum==92655) return 1;// 945.0	no tracks trb 2
	if(runnum==92673) return 1;// 945.0	no tracks trb 2
	if(runnum==92681) return 1;// 945.0	no tracks trb 2
	if(runnum==92740) return 1;// 945.0	no tracks trb 2
	if(runnum==92747) return 1;// 945.0	no tracks trb 2
	if(runnum==92791) return 1;// 945.0	no tracks trb 2
	if(runnum==92796) return 1;// 945.0	no tracks trb 2
	if(runnum==92814) return 1;// 945.0	no tracks trb 2
	if(runnum==92826) return 1;// 945.0	no tracks trb 2
	if(runnum==92840) return 1;// 945.0	no tracks trb 2
	if(runnum==92848) return 1;// 945.0	no tracks trb 2
	if(runnum==92861) return 1;// 945.0	no tracks trb 2
	if(runnum==92887) return 1;// 945.0	no tracks trb 2
	if(runnum==92915) return 1;// 945.0	no tracks trb 2
	if(runnum==92940) return 1;// 945.0	no tracks trb 2
	if(runnum==92964) return 1;// 945.0	no tracks trb 2
	if(runnum>=92982 && runnum<=92991) return 1;// 945.0 bad Nhit and dc eff, strange massive
	if(runnum==92997) return 1;// 945.0	no tracks trb 2
	if(runnum==93022) return 1;// 945.0	no tracks
	if(runnum==93041) return 1;// 945.0	no tracks
	if(runnum==93048) return 1;// 945.0	no tracks
	if(runnum==93056) return 1;// 945.0	no tracks
	if(runnum==93066) return 1;// 945.0	no tracks
	if(runnum==93078) return 1;// 945.0	no tracks
	if(runnum==93087) return 1;// 945.0	no tracks
	if(runnum==93094 || runnum==93095 ) return 1;// 945.0	no tracks
	if(runnum==93100 || runnum==93101) return 1;// 945.0	no tracks
	if(runnum==93116) return 1;// 945.0	no tracks
	if(runnum==93143) return 1;// 945.0	no tracks

	if( runnum==94717 || runnum==94739 || runnum==94740 || runnum==94743 || runnum==94770
	 || runnum==94777 || runnum==94778 || runnum==94804 || runnum==94818 || runnum==94823 
	 || runnum==94832 || runnum==94885 || runnum==94894 || runnum==94917 || runnum==94924 ) return 1;// 960 	no tracks
	if(runnum==94781 || runnum==94855) return 1;// 960 bad Nhit
		
//---------------------------------------------------------------------------------------------------

	return 0;
}
bool redrun(int runnum)
{
	if(runnum==43560 ) return 1;
	if(runnum==43561 ) return 1;
	if(runnum==43562 ) return 1;
	if(runnum==43563 ) return 1;
	if(runnum==43620 ) return 1;
	if(runnum==43621 ) return 1;
	if(runnum==43638 ) return 1;
	if(runnum==37005 ) return 1;
	if(runnum==37006 ) return 1;
	if(runnum==37007 ) return 1;
	if(runnum==37009 ) return 1;
	if(runnum==37010 ) return 1;
	if(runnum==37011 ) return 1;
	if(runnum==37012 ) return 1;
	if(runnum==37013 ) return 1;
	if(runnum==37014 ) return 1;
	if(runnum==37015 ) return 1;
	if(runnum==37016 ) return 1;
	if(runnum==37017 ) return 1;
	if(runnum==37018 ) return 1;
	if(runnum==37019 ) return 1;
	if(runnum==37020 ) return 1;
	if(runnum==37021 ) return 1;
	if(runnum==37022 ) return 1;
	if(runnum==37023 ) return 1;
	if(runnum==37024 ) return 1;
	if(runnum==37025 ) return 1;
	if(runnum==37026 ) return 1;
	if(runnum==37027 ) return 1;
	if(runnum==37028 ) return 1;
	if(runnum==37029 ) return 1;
	if(runnum==37030 ) return 1;
	if(runnum==37031 ) return 1;
	if(runnum==37032 ) return 1;
	if(runnum==37033 ) return 1;
	if(runnum==37034 ) return 1;
	if(runnum==37036 ) return 1;
	if(runnum==37037 ) return 1;
	if(runnum==37038 ) return 1;
	if(runnum==37039 ) return 1;
	if(runnum==37040 ) return 1;
	if(runnum==37041 ) return 1;
	if(runnum==37042 ) return 1;
	if(runnum==37043 ) return 1;
	if(runnum==37044 ) return 1;
	if(runnum==37045 ) return 1;
	if(runnum==37046 ) return 1;
	if(runnum==37047 ) return 1;
	if(runnum==37048 ) return 1;
	if(runnum==37051 ) return 1;
	if(runnum==37052 ) return 1;
	if(runnum==37053 ) return 1;
	if(runnum==37054 ) return 1;
	if(runnum==37055 ) return 1;
	if(runnum==37056 ) return 1;
	if(runnum==37057 ) return 1;
	if(runnum==37058 ) return 1;
	if(runnum==37059 ) return 1;
	if(runnum==37060 ) return 1;
	if(runnum==37061 ) return 1;
	if(runnum==37062 ) return 1;
	if(runnum==37063 ) return 1;
	if(runnum==37064 ) return 1;
	if(runnum==37065 ) return 1;
	if(runnum==37066 ) return 1;
	if(runnum==37067 ) return 1;
	if(runnum==37068 ) return 1;
	if(runnum==37069 ) return 1;
	if(runnum==37070 ) return 1;
	if(runnum==37071 ) return 1;
	if(runnum==37072 ) return 1;
	if(runnum==37073 ) return 1;
	if(runnum==37074 ) return 1;
	if(runnum==37075 ) return 1;
	if(runnum==37076 ) return 1;
	if(runnum==37077 ) return 1;
	if(runnum==37078 ) return 1;
	if(runnum==37079 ) return 1;
	if(runnum==37080 ) return 1;
	if(runnum==37081 ) return 1;
	if(runnum==37082 ) return 1;
	if(runnum==37083 ) return 1;
	if(runnum==37084 ) return 1;
	if(runnum==37085 ) return 1;
	if(runnum==37089 ) return 1;
	if(runnum==37090 ) return 1;
	if(runnum==37091 ) return 1;
	if(runnum==37092 ) return 1;
	if(runnum==37093 ) return 1;
	if(runnum==37094 ) return 1;
	if(runnum==37095 ) return 1;
	if(runnum==37096 ) return 1;
	if(runnum==37097 ) return 1;
	if(runnum==37098 ) return 1;
	if(runnum==37099 ) return 1;
	if(runnum==37100 ) return 1;
	if(runnum==37101 ) return 1;
	if(runnum==37102 ) return 1;
	if(runnum==37103 ) return 1;
	if(runnum==37104 ) return 1;
	if(runnum==37105 ) return 1;
	if(runnum==37106 ) return 1;
	if(runnum==37107 ) return 1;
	if(runnum==37108 ) return 1;
	if(runnum==37109 ) return 1;
	if(runnum==37110 ) return 1;
	if(runnum==37111 ) return 1;
	if(runnum==37112 ) return 1;
	if(runnum==37113 ) return 1;
	if(runnum==37114 ) return 1;
	if(runnum==37115 ) return 1;
	if(runnum==37116 ) return 1;
	if(runnum==37117 ) return 1;
	if(runnum==37126 ) return 1;
	if(runnum==37127 ) return 1;
	if(runnum==37128 ) return 1;
	if(runnum==37129 ) return 1;
	if(runnum==37130 ) return 1;
	if(runnum==37131 ) return 1;
	if(runnum==37135 ) return 1;
	if(runnum==37136 ) return 1;
	if(runnum==37137 ) return 1;
	if(runnum==37138 ) return 1;
	if(runnum==37139 ) return 1;
	if(runnum==37140 ) return 1;
	if(runnum==37141 ) return 1;
	if(runnum==37142 ) return 1;
	if(runnum==37143 ) return 1;
	if(runnum==37144 ) return 1;
	if(runnum==37145 ) return 1;
	if(runnum==37146 ) return 1;
	if(runnum==37147 ) return 1;
	if(runnum==37148 ) return 1;
	if(runnum==37149 ) return 1;
	if(runnum==37150 ) return 1;
	if(runnum==37151 ) return 1;
	if(runnum==37152 ) return 1;
	if(runnum==37153 ) return 1;
	if(runnum==37154 ) return 1;
	if(runnum==37156 ) return 1;
	if(runnum==37157 ) return 1;
	if(runnum==37163 ) return 1;
	if(runnum==37164 ) return 1;
	if(runnum==37165 ) return 1;
	if(runnum==37166 ) return 1;
	if(runnum==37167 ) return 1;
	if(runnum==37168 ) return 1;
	if(runnum==36959 ) return 1;
	if(runnum==36962 ) return 1;
	if(runnum==36931 ) return 1;
	if(runnum==47277 ) return 1;
	if(runnum==47282 ) return 1;
	if(runnum==47462 ) return 1;
	if(runnum==47538 ) return 1;
	if(runnum==47552 ) return 1;
	if(runnum==47595 ) return 1;
	if(runnum==46566 ) return 1;
	if(runnum==46652 ) return 1;
	if(runnum==46655 ) return 1;
	if(runnum==46656 ) return 1;
	if(runnum==46702 ) return 1;
	if(runnum==46703 ) return 1;
	if(runnum==46704 ) return 1;
	if(runnum==46705 ) return 1;
	if(runnum==46772 ) return 1;
	if(runnum==46778 ) return 1;
	if(runnum==46779 ) return 1;
	if(runnum==46782 ) return 1;
	if(runnum==46398 ) return 1;
	if(runnum==46452 ) return 1;
	if(runnum==46476 ) return 1;
	if(runnum==46477 ) return 1;
	if(runnum==46203 ) return 1;
	if(runnum==46254 ) return 1;
	if(runnum==46265 ) return 1;
	if(runnum==46304 ) return 1;
	if(runnum==46322 ) return 1;
	if(runnum==46029 ) return 1;
	if(runnum==46122 ) return 1;
	if(runnum==46128 ) return 1;
	if(runnum==46132 ) return 1;
	if(runnum==45813 ) return 1;
	if(runnum==45814 ) return 1;
	if(runnum==45815 ) return 1;
	if(runnum==45818 ) return 1;
	if(runnum==45747 ) return 1;
	if(runnum==37860 ) return 1;
	if(runnum==37861 ) return 1;
	if(runnum==37862 ) return 1;
	if(runnum==37863 ) return 1;
	if(runnum==37864 ) return 1;
	if(runnum==37865 ) return 1;
	if(runnum==37866 ) return 1;
	if(runnum==37867 ) return 1;
	if(runnum==37868 ) return 1;
	if(runnum==37869 ) return 1;
	if(runnum==37870 ) return 1;
	if(runnum==37871 ) return 1;
	if(runnum==37872 ) return 1;
	if(runnum==37873 ) return 1;
	if(runnum==37874 ) return 1;
	if(runnum==37881 ) return 1;
	if(runnum==37883 ) return 1;
	if(runnum==37884 ) return 1;
	if(runnum==37885 ) return 1;
	if(runnum==37886 ) return 1;
	if(runnum==37887 ) return 1;
	if(runnum==37888 ) return 1;
	if(runnum==37889 ) return 1;
	if(runnum==37890 ) return 1;
	if(runnum==37891 ) return 1;
	if(runnum==37893 ) return 1;
	if(runnum==37894 ) return 1;
	if(runnum==37895 ) return 1;
	if(runnum==37897 ) return 1;
	if(runnum==37898 ) return 1;
	if(runnum==37899 ) return 1;
	if(runnum==37901 ) return 1;
	if(runnum==37902 ) return 1;
	if(runnum==37903 ) return 1;
	if(runnum==37904 ) return 1;
	if(runnum==37905 ) return 1;
	if(runnum==37907 ) return 1;
	if(runnum==37909 ) return 1;
	if(runnum==37910 ) return 1;
	if(runnum==37911 ) return 1;
	if(runnum==37912 ) return 1;
	if(runnum==37913 ) return 1;
	if(runnum==37914 ) return 1;
	if(runnum==37915 ) return 1;
	if(runnum==37916 ) return 1;
	if(runnum==37917 ) return 1;
	if(runnum==37918 ) return 1;
	if(runnum==37919 ) return 1;
	if(runnum==37921 ) return 1;
	if(runnum==37922 ) return 1;
	if(runnum==37923 ) return 1;
	if(runnum==37924 ) return 1;
	if(runnum==37925 ) return 1;
	if(runnum==37926 ) return 1;
	if(runnum==37927 ) return 1;
	if(runnum==37928 ) return 1;
	if(runnum==37929 ) return 1;
	if(runnum==37930 ) return 1;
	if(runnum==37931 ) return 1;
	if(runnum==37932 ) return 1;
	if(runnum==37933 ) return 1;
	if(runnum==37934 ) return 1;
	if(runnum==37935 ) return 1;
	if(runnum==37936 ) return 1;
	if(runnum==37937 ) return 1;
	if(runnum==37938 ) return 1;
	if(runnum==37939 ) return 1;
	if(runnum==37940 ) return 1;
	if(runnum==37941 ) return 1;
	if(runnum==37942 ) return 1;
	if(runnum==37943 ) return 1;
	if(runnum==37944 ) return 1;
	if(runnum==37945 ) return 1;
	if(runnum==37946 ) return 1;
	if(runnum==37947 ) return 1;
	if(runnum==37948 ) return 1;
	if(runnum==37949 ) return 1;
	if(runnum==37950 ) return 1;
	if(runnum==37951 ) return 1;
	if(runnum==37952 ) return 1;
	if(runnum==37953 ) return 1;
	if(runnum==37954 ) return 1;
	if(runnum==37955 ) return 1;
	if(runnum==37956 ) return 1;
	if(runnum==37957 ) return 1;
	if(runnum==37958 ) return 1;
	if(runnum==37990 ) return 1;
	if(runnum==37991 ) return 1;
	if(runnum==37992 ) return 1;
	if(runnum==37993 ) return 1;
	if(runnum==37994 ) return 1;
	if(runnum==37995 ) return 1;
	if(runnum==37999 ) return 1;
	if(runnum==38000 ) return 1;
	if(runnum==38001 ) return 1;
	if(runnum==38003 ) return 1;
	if(runnum==38004 ) return 1;
	if(runnum==38005 ) return 1;
	if(runnum==38006 ) return 1;
	if(runnum==38007 ) return 1;
	if(runnum==38008 ) return 1;
	if(runnum==38009 ) return 1;
	if(runnum==38010 ) return 1;
	if(runnum==38011 ) return 1;
	if(runnum==38012 ) return 1;
	if(runnum==38013 ) return 1;
	if(runnum==38014 ) return 1;
	if(runnum==38015 ) return 1;
	if(runnum==38016 ) return 1;
	if(runnum==38017 ) return 1;
	if(runnum==38018 ) return 1;
	if(runnum==38019 ) return 1;
	if(runnum==38020 ) return 1;
	if(runnum==38021 ) return 1;
	if(runnum==38022 ) return 1;
	if(runnum==38023 ) return 1;
	if(runnum==38024 ) return 1;
	if(runnum==38025 ) return 1;
	if(runnum==38027 ) return 1;
	if(runnum==38028 ) return 1;
	if(runnum==38029 ) return 1;
	if(runnum==38030 ) return 1;
	if(runnum==38031 ) return 1;
	if(runnum==38032 ) return 1;
	if(runnum==38034 ) return 1;
	if(runnum==38035 ) return 1;
	if(runnum==38036 ) return 1;
	if(runnum==38037 ) return 1;
	if(runnum==38038 ) return 1;
	if(runnum==38039 ) return 1;
	if(runnum==38052 ) return 1;
	if(runnum==38053 ) return 1;
	if(runnum==38054 ) return 1;
	if(runnum==38055 ) return 1;
	if(runnum==38117 ) return 1;
	if(runnum==38118 ) return 1;
	if(runnum==38120 ) return 1;
	if(runnum==38121 ) return 1;
	if(runnum==38167 ) return 1;
	if(runnum==38182 ) return 1;
	if(runnum==38184 ) return 1;
	if(runnum==38228 ) return 1;
	if(runnum==38265 ) return 1;
	if(runnum==38266 ) return 1;
	if(runnum==38267 ) return 1;
	if(runnum==38269 ) return 1;
	if(runnum==38270 ) return 1;
	if(runnum==38276 ) return 1;
	if(runnum==38278 ) return 1;
	if(runnum==38306 ) return 1;
	if(runnum==38307 ) return 1;
	if(runnum==38309 ) return 1;
	if(runnum==38311 ) return 1;
	if(runnum==38312 ) return 1;
	if(runnum==38313 ) return 1;
	if(runnum==38321 ) return 1;
	if(runnum==38358 ) return 1;
	if(runnum==38361 ) return 1;
	if(runnum==38387 ) return 1;
	if(runnum==38416 ) return 1;
	if(runnum==38421 ) return 1;
	if(runnum==38425 ) return 1;
	if(runnum==38426 ) return 1;
	if(runnum==38431 ) return 1;
	if(runnum==38433 ) return 1;
	if(runnum==38464 ) return 1;
	if(runnum==38568 ) return 1;
	if(runnum==38569 ) return 1;
	if(runnum==38570 ) return 1;
	if(runnum==38571 ) return 1;
	if(runnum==38572 ) return 1;
	if(runnum==38574 ) return 1;
	if(runnum==38575 ) return 1;
	if(runnum==38576 ) return 1;
	if(runnum==38577 ) return 1;
	if(runnum==38578 ) return 1;
	if(runnum==38579 ) return 1;
	if(runnum==38580 ) return 1;
	if(runnum==38581 ) return 1;
	if(runnum==38582 ) return 1;
	if(runnum==38583 ) return 1;
	if(runnum==38584 ) return 1;
	if(runnum==38585 ) return 1;
	if(runnum==38587 ) return 1;
	if(runnum==38588 ) return 1;
	if(runnum==38589 ) return 1;
	if(runnum==38590 ) return 1;
	if(runnum==38591 ) return 1;
	if(runnum==38592 ) return 1;
	if(runnum==38593 ) return 1;
	if(runnum==38594 ) return 1;
	if(runnum==38595 ) return 1;
	if(runnum==38596 ) return 1;
	if(runnum==38597 ) return 1;
	if(runnum==38598 ) return 1;
	if(runnum==38601 ) return 1;
	if(runnum==38746 ) return 1;
	if(runnum==38794 ) return 1;
	if(runnum==38819 ) return 1;
	if(runnum==38831 ) return 1;
	if(runnum==38839 ) return 1;
	if(runnum==38843 ) return 1;
	if(runnum==38935 ) return 1;
	if(runnum==38963 ) return 1;
	if(runnum==38973 ) return 1;
	if(runnum==38976 ) return 1;
	if(runnum==38977 ) return 1;
	if(runnum==38978 ) return 1;
	if(runnum==38979 ) return 1;
	if(runnum==38981 ) return 1;
	if(runnum==38982 ) return 1;
	if(runnum==38983 ) return 1;
	if(runnum==38984 ) return 1;
	if(runnum==38985 ) return 1;
	if(runnum==38986 ) return 1;
	if(runnum==38987 ) return 1;
	if(runnum==38988 ) return 1;
	if(runnum==38989 ) return 1;
	if(runnum==38990 ) return 1;
	if(runnum==38991 ) return 1;
	if(runnum==38992 ) return 1;
	if(runnum==38993 ) return 1;
	if(runnum==38994 ) return 1;
	if(runnum==38995 ) return 1;
	if(runnum==38996 ) return 1;
	if(runnum==38998 ) return 1;
	if(runnum==38999 ) return 1;
	if(runnum==39000 ) return 1;
	if(runnum==39001 ) return 1;
	if(runnum==39002 ) return 1;
	if(runnum==39003 ) return 1;
	if(runnum==39004 ) return 1;
	if(runnum==39005 ) return 1;
	if(runnum==39006 ) return 1;
	if(runnum==39007 ) return 1;
	if(runnum==39009 ) return 1;
	if(runnum==39010 ) return 1;
	if(runnum==39011 ) return 1;
	if(runnum==39012 ) return 1;
	if(runnum==39013 ) return 1;
	if(runnum==39014 ) return 1;
	if(runnum==39015 ) return 1;
	if(runnum==39016 ) return 1;
	if(runnum==39017 ) return 1;
	if(runnum==39018 ) return 1;
	if(runnum==39019 ) return 1;
	if(runnum==39020 ) return 1;
	if(runnum==39021 ) return 1;
	if(runnum==39022 ) return 1;
	if(runnum==39154 ) return 1;
	if(runnum==39158 ) return 1;
	if(runnum==39159 ) return 1;
	if(runnum==39164 ) return 1;
	if(runnum==39166 ) return 1;
	if(runnum==39167 ) return 1;
	if(runnum==39168 ) return 1;
	if(runnum==39169 ) return 1;
	if(runnum==39170 ) return 1;
	if(runnum==39171 ) return 1;
	if(runnum==39172 ) return 1;
	if(runnum==39173 ) return 1;
	if(runnum==39174 ) return 1;
	if(runnum==39177 ) return 1;
	if(runnum==39180 ) return 1;
	if(runnum==39181 ) return 1;
	if(runnum==39183 ) return 1;
	if(runnum==39184 ) return 1;
	if(runnum==39185 ) return 1;
	if(runnum==39186 ) return 1;
	if(runnum==39189 ) return 1;
	if(runnum==39190 ) return 1;
	if(runnum==39191 ) return 1;
	if(runnum==39192 ) return 1;
	if(runnum==39193 ) return 1;
	if(runnum==39194 ) return 1;
	if(runnum==39195 ) return 1;
	if(runnum==39197 ) return 1;
	if(runnum==39198 ) return 1;
	if(runnum==39199 ) return 1;
	if(runnum==39200 ) return 1;
	if(runnum==39202 ) return 1;
	if(runnum==39206 ) return 1;
	if(runnum==39208 ) return 1;
	if(runnum==39213 ) return 1;
	if(runnum==39216 ) return 1;
	if(runnum==39236 ) return 1;
	if(runnum==39239 ) return 1;
	if(runnum==39240 ) return 1;
	if(runnum==39241 ) return 1;
	if(runnum==39242 ) return 1;
	if(runnum==39249 ) return 1;
	if(runnum==39258 ) return 1;
	if(runnum==39259 ) return 1;
	if(runnum==39260 ) return 1;
	if(runnum==39281 ) return 1;
	if(runnum==39355 ) return 1;
	if(runnum==39356 ) return 1;
	if(runnum==39357 ) return 1;
	if(runnum==39377 ) return 1;
	if(runnum==39385 ) return 1;
	if(runnum==39386 ) return 1;
	if(runnum==39387 ) return 1;
	if(runnum==39388 ) return 1;
	if(runnum==39390 ) return 1;
	if(runnum==39391 ) return 1;
	if(runnum==39392 ) return 1;
	if(runnum==39393 ) return 1;
	if(runnum==39395 ) return 1;
	if(runnum==39396 ) return 1;
	if(runnum==39397 ) return 1;
	if(runnum==39398 ) return 1;
	if(runnum==39400 ) return 1;
	if(runnum==39401 ) return 1;
	if(runnum==39406 ) return 1;
	if(runnum==39407 ) return 1;
	if(runnum==39409 ) return 1;
	if(runnum==39410 ) return 1;
	if(runnum==39412 ) return 1;
	if(runnum==39415 ) return 1;
	if(runnum==39416 ) return 1;
	if(runnum==39419 ) return 1;
	if(runnum==39420 ) return 1;
	if(runnum==39423 ) return 1;
	if(runnum==39424 ) return 1;
	if(runnum==39429 ) return 1;
	if(runnum==39430 ) return 1;
	if(runnum==39499 ) return 1;
	if(runnum==39500 ) return 1;
	if(runnum==39501 ) return 1;
	if(runnum==39561 ) return 1;
	if(runnum==39597 ) return 1;
	if(runnum==39621 ) return 1;
	if(runnum==39622 ) return 1;
	if(runnum==39627 ) return 1;
	if(runnum==39629 ) return 1;
	if(runnum==39630 ) return 1;
	if(runnum==39634 ) return 1;
	if(runnum==39635 ) return 1;
	if(runnum==39636 ) return 1;
	if(runnum==39640 ) return 1;
	if(runnum==39643 ) return 1;
	if(runnum==39653 ) return 1;
	if(runnum==39662 ) return 1;
	if(runnum==39674 ) return 1;
	if(runnum==39685 ) return 1;
	if(runnum==39692 ) return 1;
	if(runnum==39699 ) return 1;
	if(runnum==39704 ) return 1;
	if(runnum==39705 ) return 1;
	if(runnum==39706 ) return 1;
	if(runnum==39707 ) return 1;
	if(runnum==39708 ) return 1;
	if(runnum==39711 ) return 1;
	if(runnum==39712 ) return 1;
	if(runnum==39713 ) return 1;
	if(runnum==39714 ) return 1;
	if(runnum==39715 ) return 1;
	if(runnum==39722 ) return 1;
	if(runnum==39723 ) return 1;
	if(runnum==39725 ) return 1;
	if(runnum==39728 ) return 1;
	if(runnum==39730 ) return 1;
	if(runnum==39731 ) return 1;
	if(runnum==39736 ) return 1;
	if(runnum==39739 ) return 1;
	if(runnum==39742 ) return 1;
	if(runnum==39743 ) return 1;
	if(runnum==39746 ) return 1;
	if(runnum==39749 ) return 1;
	if(runnum==39754 ) return 1;
	if(runnum==39758 ) return 1;
	if(runnum==39759 ) return 1;
	if(runnum==39760 ) return 1;
	if(runnum==39764 ) return 1;
	if(runnum==39767 ) return 1;
	if(runnum==39771 ) return 1;
	if(runnum==39772 ) return 1;
	if(runnum==39778 ) return 1;
	if(runnum==39805 ) return 1;
	if(runnum==39807 ) return 1;
	if(runnum==39808 ) return 1;
	if(runnum==39809 ) return 1;
	if(runnum==39812 ) return 1;
	if(runnum==39814 ) return 1;
	if(runnum==39815 ) return 1;
	if(runnum==39831 ) return 1;
	if(runnum==39840 ) return 1;
	if(runnum==39857 ) return 1;
	if(runnum==39860 ) return 1;
	if(runnum==39872 ) return 1;
	if(runnum==39874 ) return 1;
	if(runnum==39875 ) return 1;
	if(runnum==39876 ) return 1;
	if(runnum==39896 ) return 1;
	if(runnum==39898 ) return 1;
	if(runnum==39923 ) return 1;
	if(runnum==39928 ) return 1;
	if(runnum==39929 ) return 1;
	if(runnum==39930 ) return 1;
	if(runnum==39932 ) return 1;
	if(runnum==39933 ) return 1;
	if(runnum==39934 ) return 1;
	if(runnum==39935 ) return 1;
	if(runnum==39936 ) return 1;
	if(runnum==39937 ) return 1;
	if(runnum==39938 ) return 1;
	if(runnum==39939 ) return 1;
	if(runnum==39940 ) return 1;
	if(runnum==39941 ) return 1;
	if(runnum==39943 ) return 1;
	if(runnum==39947 ) return 1;
	if(runnum==39948 ) return 1;
	if(runnum==39977 ) return 1;
	if(runnum==39980 ) return 1;
	if(runnum==40000 ) return 1;
	if(runnum==40092 ) return 1;
	if(runnum==40093 ) return 1;
	if(runnum==40094 ) return 1;
	if(runnum==40095 ) return 1;
	if(runnum==40097 ) return 1;
	if(runnum==40100 ) return 1;
	if(runnum==40140 ) return 1;
	if(runnum==40198 ) return 1;
	if(runnum==40199 ) return 1;
	if(runnum==40201 ) return 1;
	if(runnum==40271 ) return 1;
	if(runnum==40277 ) return 1;
	if(runnum==40280 ) return 1;
	if(runnum==40311 ) return 1;
	if(runnum==40312 ) return 1;
	if(runnum==40320 ) return 1;
	if(runnum==40321 ) return 1;
	if(runnum==40467 ) return 1;
	if(runnum==40516 ) return 1;
	if(runnum==40552 ) return 1;
	if(runnum==40553 ) return 1;
	if(runnum==40725 ) return 1;
	if(runnum==41367 ) return 1;
	if(runnum==41368 ) return 1;
	if(runnum==41369 ) return 1;
	if(runnum==41370 ) return 1;
	if(runnum==41371 ) return 1;
	if(runnum==41372 ) return 1;
	if(runnum==41733 ) return 1;
	if(runnum==42221 ) return 1;
	if(runnum==42222 ) return 1;
	if(runnum==42223 ) return 1;
	if(runnum==42931 ) return 1;
	if(runnum==42935 ) return 1;
	return 0;
}