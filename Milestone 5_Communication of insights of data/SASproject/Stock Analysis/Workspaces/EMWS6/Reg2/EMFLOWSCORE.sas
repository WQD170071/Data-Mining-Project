*************************************;
*** begin scoring code for regression;
*************************************;

length _WARN_ $4;
label _WARN_ = 'Warnings' ;

length I_target $ 4;
label I_target = 'Into: target' ;
*** Target Values;
array REG2DRF [3] $4 _temporary_ ('SELL' 'HOLD' 'BUY' );
label U_target = 'Unnormalized Into: target' ;
format U_target $4.;
length U_target $ 4;
*** Unnormalized target values;
array REG2DRU[3] $ 4 _temporary_ ('sell'  'hold'  'buy ' );

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

*** Compute Linear Predictor;
drop _TEMP;
drop _LP0  _LP1;
_LP0 = 0;
_LP1 = 0;

*** Naive Posterior Probabilities;
drop _MAXP _IY _P0 _P1 _P2;
drop _LPMAX;
_LPMAX= 0;
_LP0 =    -0.27029032973991 + _LP0;
if _LPMAX < _LP0 then _LPMAX = _LP0;
_LP1 =    -0.45953232937844 + _LP1;
if _LPMAX < _LP1 then _LPMAX = _LP1;
_LP0 = exp(_LP0 - _LPMAX);
_LP1 = exp(_LP1 - _LPMAX);
_LPMAX = exp(-_LPMAX);
_P2 = 1 / (_LPMAX + _LP0 + _LP1);
_P0 = _LP0 * _P2;
_P1 = _LP1 * _P2;
_P2 = _LPMAX * _P2;


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
I_target = REG2DRF[_IY];
U_target = REG2DRU[_IY];

*************************************;
***** end scoring code for regression;
*************************************;
