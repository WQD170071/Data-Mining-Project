*------------------------------------------------------------*;
* Data Source Setup;
*------------------------------------------------------------*;
libname EMWS6 "G:\SASproject\Stock Analysis\Workspaces\EMWS6";
*------------------------------------------------------------*;
* Ids2: Creating DATA data;
*------------------------------------------------------------*;
data EMWS6.Ids2_DATA (label="")
/ view=EMWS6.Ids2_DATA
;
set AAEM141.FMODEL_TRAIN;
run;
