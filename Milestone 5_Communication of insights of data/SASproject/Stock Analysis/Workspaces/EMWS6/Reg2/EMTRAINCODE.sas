*------------------------------------------------------------*;
* Reg2: Create decision matrix;
*------------------------------------------------------------*;
data WORK.target;
  length   target                           $  32
           COUNT                                8
           DATAPRIOR                            8
           TRAINPRIOR                           8
           DECPRIOR                             8
           DECISION1                            8
           DECISION2                            8
           DECISION3                            8
           ;

  label    COUNT="Level Counts"
           DATAPRIOR="Data Proportions"
           TRAINPRIOR="Training Proportions"
           DECPRIOR="Decision Priors"
           DECISION1="SELL"
           DECISION2="HOLD"
           DECISION3="BUY"
           ;
  format   COUNT 10.
           ;
target="SELL"; COUNT=59; DATAPRIOR=0.31891891891891; TRAINPRIOR=0.31891891891891; DECPRIOR=.; DECISION1=1; DECISION2=0; DECISION3=0;
output;
target="HOLD"; COUNT=50; DATAPRIOR=0.27027027027027; TRAINPRIOR=0.27027027027027; DECPRIOR=.; DECISION1=0; DECISION2=1; DECISION3=0;
output;
target="BUY"; COUNT=76; DATAPRIOR=0.41081081081081; TRAINPRIOR=0.41081081081081; DECPRIOR=.; DECISION1=0; DECISION2=0; DECISION3=1;
output;
;
run;
proc datasets lib=work nolist;
modify target(type=PROFIT label=target);
label DECISION1= 'SELL';
label DECISION2= 'HOLD';
label DECISION3= 'BUY';
run;
quit;
data EM_DMREG / view=EM_DMREG;
set EMWS6.Impt_TRAIN(keep=
LOG_high LOG_low LOG_open LOG_price REP_volume change code name sentiment
target );
run;
*------------------------------------------------------------* ;
* Reg2: DMDBClass Macro ;
*------------------------------------------------------------* ;
%macro DMDBClass;
    code(ASC) name(ASC) sentiment(ASC) target(DESC)
%mend DMDBClass;
*------------------------------------------------------------* ;
* Reg2: DMDBVar Macro ;
*------------------------------------------------------------* ;
%macro DMDBVar;
    LOG_high LOG_low LOG_open LOG_price REP_volume change
%mend DMDBVar;
*------------------------------------------------------------*;
* Reg2: Create DMDB;
*------------------------------------------------------------*;
proc dmdb batch data=WORK.EM_DMREG
dmdbcat=WORK.Reg2_DMDB
maxlevel = 513
;
class %DMDBClass;
var %DMDBVar;
target
target
;
run;
quit;
*------------------------------------------------------------*;
* Reg2: Run DMREG procedure;
*------------------------------------------------------------*;
proc dmreg data=EM_DMREG dmdbcat=WORK.Reg2_DMDB
validata = EMWS6.Impt_VALIDATE
outest = EMWS6.Reg2_EMESTIMATE
outterms = EMWS6.Reg2_OUTTERMS
outmap= EMWS6.Reg2_MAPDS namelen=200
;
class
target
code
name
sentiment
;
model target =
LOG_high
LOG_low
LOG_open
LOG_price
REP_volume
change
code
name
sentiment
/level=nominal
coding=DEVIATION
nodesignprint
selection=STEPWISE choose=VMISC
Hierarchy=CLASS
Rule=NONE
;
;
code file="G:\SASproject\Stock Analysis\Workspaces\EMWS6\Reg2\EMPUBLISHSCORE.sas"
group=Reg2
;
code file="G:\SASproject\Stock Analysis\Workspaces\EMWS6\Reg2\EMFLOWSCORE.sas"
group=Reg2
residual
;
run;
quit;
