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
