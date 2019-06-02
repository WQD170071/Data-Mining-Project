*------------------------------------------------------------*;
* Data Source Setup;
*------------------------------------------------------------*;
libname EMWS6 "G:\SASproject\Stock Analysis\Workspaces\EMWS6";
*------------------------------------------------------------*;
* Ids3: Creating DATA data;
*------------------------------------------------------------*;
data EMWS6.Ids3_DATA (label="")
/ view=EMWS6.Ids3_DATA
;
set AAEM141.CMODEL_TRAIN;
run;
