drop _temp_;
if (P_targetsell ge 0.89655172413793) then do;
_temp_ = dmran(1234);
b_target = floor(1 + 6*_temp_);
end;
else
if (P_targetsell ge 0.11111111111111) then do;
_temp_ = dmran(1234);
b_target = floor(7 + 6*_temp_);
end;
else
do;
_temp_ = dmran(1234);
b_target = floor(13 + 8*_temp_);
end;
