c(C) :- course(C,_,_,_,_,_). t(T) :- course(_,T,_,_,_,_).
r(R) :- room(R,_,_). cu(Cu) :- curricula(Cu,_).
d(0..D-1) :- days(D). ppd(0..P-1) :- periods_per_day(P).
 
N { assigned(C,D,P) : d(D), ppd(P) } N :- course(C,_,N,_,_,_).
 
:- not { assigned(C,D,P) : course(C,T,_,_,_,_) } 1, t(T), d(D), ppd(P).
:- not { assigned(C,D,P) : curricula(Cu,C) } 1, cu(Cu), d(D), ppd(P).
 
{ assigned(C,R,D,P) : r(R) } 1 :- assigned(C,D,P).
:- not { assigned(C,R,D,P) : c(C) } 1, r(R), d(D), ppd(P).
 
:- assigned(C,D,P), unavailability_constraint(C,D,P).
:- not { assigned(C,D,P) : c(C) } N, d(D), ppd(P), rooms(N).
 
 
name("SoftDev"). courses(8). rooms(5). days(5).periods_per_day(6). curricula(2).
min_max_daily_lectures(2,5). unavailabilityconstraints(8). roomconstraints(0).
 
course("MachineLearning","jim",4,2,40,1). course("SecurityForSoft","eli",4,2,30,1). course("EmbeddedSysEng","nora",4,2,40,1). course("AppDevFramework","jimothy",4,3,30,1). 
course("ScaleMicroservi","Harry",4,2,30,1). course("EmbeddSysEng","cilian",4,2,30,1). course("SoftDefNetwork","aaron",4,3,35,1). course("EmbedSoftSecure","dylan",4,4,40,0). 
 
room("Ae",300). room("Ab",400). room("Be",251). room("Ba",351). room("Cb",402). 
 
curricula("SoftwareDev","MachineLearning"). curricula("SoftwareDev","SecurityForSoft"). curricula("SoftwareDev","EmbeddedSysEng"). curricula("SoftwareDev","AppDevFramework"). curricula("SoftwareDev",""). 
curricula("CompSys","EmbeddSysEng"). curricula("CompSys","ScaleMicroservi"). curricula("CompSys","SoftDefNetwork"). curricula("CompSys","EmbedSoftSecure"). curricula("CompSys",""). 
 
unavailability_constraint("MachineLearning",3,0). unavailability_constraint("MachineLearning",3,1). unavailability_constraint("ScaleMicroservi",1,1). unavailability_constraint("ScaleMicroservi",2,0). 
unavailability_constraint("AppDevFramework",1,0). unavailability_constraint("AppDevFramework",2,1). unavailability_constraint("SecurityForSoft",3,2). unavailability_constraint("EmbeddedSysEng",1,3). 
 
#show assigned/3.#defined addTab/2.