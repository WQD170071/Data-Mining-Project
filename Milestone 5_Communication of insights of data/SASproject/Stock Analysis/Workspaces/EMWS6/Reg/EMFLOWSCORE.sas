*************************************;
*** begin scoring code for regression;
*************************************;

length _WARN_ $4;
label _WARN_ = 'Warnings' ;

length I_target $ 4;
label I_target = 'Into: target' ;
*** Target Values;
array REGDRF [3] $4 _temporary_ ('SELL' 'HOLD' 'BUY' );
label U_target = 'Unnormalized Into: target' ;
format U_target $4.;
length U_target $ 4;
*** Unnormalized target values;
array REGDRU[3] $ 4 _temporary_ ('sell'  'hold'  'buy ' );

*** Generate dummy variables for target ;
drop _Y ;
label F_target = 'From: target' ;
length F_target $ 4;
F_target = put( target , $4. );
%DMNORMIP( F_target )
if missing( target ) then do;
   _Y = .;
end;
else do;
   if F_target = 'BUY'  then do;
      _Y = 2;
   end;
   else if F_target = 'SELL'  then do;
      _Y = 0;
   end;
   else if F_target = 'HOLD'  then do;
      _Y = 1;
   end;
   else do;
      _Y = .;
   end;
end;

drop _DM_BAD;
_DM_BAD=0;

*** Check LOG_high for missing values ;
if missing( LOG_high ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check LOG_low for missing values ;
if missing( LOG_low ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check LOG_open for missing values ;
if missing( LOG_open ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check LOG_price for missing values ;
if missing( LOG_price ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check REP_volume for missing values ;
if missing( REP_volume ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Check change for missing values ;
if missing( change ) then do;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;

*** Generate dummy variables for code ;
drop _1_0 _1_1 _1_2 ;
if missing( code ) then do;
   _1_0 = .;
   _1_1 = .;
   _1_2 = .;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;
else do;
   length _dm12 $ 12; drop _dm12 ;
   _dm12 = put( code , BEST12. );
   %DMNORMIP( _dm12 )
   if _dm12 = '5099'  then do;
      _1_0 = 0;
      _1_1 = 0;
      _1_2 = 1;
   end;
   else if _dm12 = '4707'  then do;
      _1_0 = 0;
      _1_1 = 1;
      _1_2 = 0;
   end;
   else if _dm12 = '7668'  then do;
      _1_0 = -1;
      _1_1 = -1;
      _1_2 = -1;
   end;
   else if _dm12 = '3182'  then do;
      _1_0 = 1;
      _1_1 = 0;
      _1_2 = 0;
   end;
   else do;
      _1_0 = .;
      _1_1 = .;
      _1_2 = .;
      substr(_warn_,2,1) = 'U';
      _DM_BAD = 1;
   end;
end;

*** Generate dummy variables for sentiment ;
drop _3_0 _3_1 ;
if missing( sentiment ) then do;
   _3_0 = .;
   _3_1 = .;
   substr(_warn_,1,1) = 'M';
   _DM_BAD = 1;
end;
else do;
   length _dm12 $ 12; drop _dm12 ;
   _dm12 = put( sentiment , BEST12. );
   %DMNORMIP( _dm12 )
   if _dm12 = '0'  then do;
      _3_0 = 0;
      _3_1 = 1;
   end;
   else if _dm12 = '1'  then do;
      _3_0 = -1;
      _3_1 = -1;
   end;
   else if _dm12 = '-1'  then do;
      _3_0 = 1;
      _3_1 = 0;
   end;
   else do;
      _3_0 = .;
      _3_1 = .;
      substr(_warn_,2,1) = 'U';
      _DM_BAD = 1;
   end;
end;

*** If missing inputs, use averages;
if _DM_BAD > 0 then do;
   _P0 = 0.3186813187;
   _P1 = 0.2637362637;
   _P2 = 0.4175824176;
   goto REGDR1;
end;

*** Compute Linear Predictor;
drop _TEMP;
drop _LP0  _LP1;
_LP0 = 0;
_LP1 = 0;

***  Effect: LOG_high ;
_TEMP = LOG_high ;
_LP0 = _LP0 + (     415.51526928802 * _TEMP);
_LP1 = _LP1 + (    700.988946546999 * _TEMP);

***  Effect: LOG_low ;
_TEMP = LOG_low ;
_LP0 = _LP0 + (    2041.78522978202 * _TEMP);
_LP1 = _LP1 + (    2411.39210167317 * _TEMP);

***  Effect: LOG_open ;
_TEMP = LOG_open ;
_LP0 = _LP0 + (   -1063.97435489004 * _TEMP);
_LP1 = _LP1 + (   -1704.14105387919 * _TEMP);

***  Effect: LOG_price ;
_TEMP = LOG_price ;
_LP0 = _LP0 + (   -1135.23390825138 * _TEMP);
_LP1 = _LP1 + (   -1054.64914824374 * _TEMP);

***  Effect: REP_volume ;
_TEMP = REP_volume ;
_LP0 = _LP0 + (  1.3136668357037E-6 * _TEMP);
_LP1 = _LP1 + (  1.8096100908067E-6 * _TEMP);

***  Effect: change ;
_TEMP = change ;
_LP0 = _LP0 + (   -6429.00143405165 * _TEMP);
_LP1 = _LP1 + (   -4132.62548467252 * _TEMP);

***  Effect: code ;
_TEMP = 1;
_LP0 = _LP0 + (    73.0492578180579) * _TEMP * _1_0;
_LP1 = _LP1 + (    107.949096538111) * _TEMP * _1_0;
_LP0 = _LP0 + (   -671.377189166035) * _TEMP * _1_1;
_LP1 = _LP1 + (   -912.765622465845) * _TEMP * _1_1;
_LP0 = _LP0 + (    289.504343957857) * _TEMP * _1_2;
_LP1 = _LP1 + (    385.135244805684) * _TEMP * _1_2;

***  Effect: sentiment ;
_TEMP = 1;
_LP0 = _LP0 + (    117.496964457404) * _TEMP * _3_0;
_LP1 = _LP1 + (    66.3027791728311) * _TEMP * _3_0;
_LP0 = _LP0 + (    84.5339695125311) * _TEMP * _3_1;
_LP1 = _LP1 + (    61.9067428197361) * _TEMP * _3_1;

*** Naive Posterior Probabilities;
drop _MAXP _IY _P0 _P1 _P2;
drop _LPMAX;
_LPMAX= 0;
_LP0 =    -709.012859897812 + _LP0;
if _LPMAX < _LP0 then _LPMAX = _LP0;
_LP1 =    -901.865168304282 + _LP1;
if _LPMAX < _LP1 then _LPMAX = _LP1;
_LP0 = exp(_LP0 - _LPMAX);
_LP1 = exp(_LP1 - _LPMAX);
_LPMAX = exp(-_LPMAX);
_P2 = 1 / (_LPMAX + _LP0 + _LP1);
_P0 = _LP0 * _P2;
_P1 = _LP1 * _P2;
_P2 = _LPMAX * _P2;

REGDR1:

*** Residuals;
if (_Y = .) then do;
   R_targetsell = .;
   R_targethold = .;
   R_targetbuy = .;
end;
else do;
    label R_targetsell = 'Residual: target=sell' ;
    label R_targethold = 'Residual: target=hold' ;
    label R_targetbuy = 'Residual: target=buy' ;
   R_targetsell = - _P0;
   R_targethold = - _P1;
   R_targetbuy = - _P2;
   select( _Y );
      when (0)  R_targetsell = R_targetsell + 1;
      when (1)  R_targethold = R_targethold + 1;
      when (2)  R_targetbuy = R_targetbuy + 1;
   end;
end;

*** Posterior Probabilities and Predicted Level;
label P_targetsell = 'Predicted: target=sell' ;
label P_targethold = 'Predicted: target=hold' ;
label P_targetbuy = 'Predicted: target=buy' ;
P_targetsell = _P0;
_MAXP = _P0;
_IY = 1;
P_targethold = _P1;
if (_P1 >  _MAXP + 1E-8) then do;
   _MAXP = _P1;
   _IY = 2;
end;
P_targetbuy = _P2;
if (_P2 >  _MAXP + 1E-8) then do;
   _MAXP = _P2;
   _IY = 3;
end;
I_target = REGDRF[_IY];
U_target = REGDRU[_IY];

*************************************;
***** end scoring code for regression;
*************************************;
