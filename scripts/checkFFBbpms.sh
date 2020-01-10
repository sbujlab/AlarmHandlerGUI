#!/bin/tcsh
set OKstatus="FFB:"
if (`caget -t FB_A:use_RF` != 'RF On') then
  set tmp=`caget FB_A:use_RF`
  set OKstatus="$OKstatus $tmp Not OK, Should read RF On\n"
endif
if (`caget -t FB_A:isolate_en` != 'On') then
  set tmp=`caget FB_A:isolate_en`
  set OKstatus="$OKstatus $tmp Not OK, Should read On\n"
endif
if (`caget -t FB_A:disp_optics` != 'Standard') then
  set tmp=`caget FB_A:disp_optics`
  set OKstatus="$OKstatus $tmp Not OK, Should read Standard\n"
endif
if (`caget -t FB_A:BPM:use:x_1` != 'used') then
  set tmp=`caget FB_A:BPM:use:x_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use:x_2` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:x_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:x_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:x_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:x_6` != 'used') then
  set tmp=`caget FB_A:BPM:use:x_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use:x_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:x_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use:x_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_1` != 'used') then
  set tmp=`caget FB_A:BPM:use:y_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use:y_2` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_6` != 'used') then
  set tmp=`caget FB_A:BPM:use:y_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use:y_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use:y_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use:y_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_1` != 'used') then
  set tmp=`caget FB_A:BPM:use_energy:x_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_2` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:x_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:x_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_4` != 'used') then
  set tmp=`caget FB_A:BPM:use_energy:x_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:x_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_energy:x_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:x_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:x_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:x_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_1` != 'used') then
  set tmp=`caget FB_A:BPM:use_energy:y_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_2` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_energy:y_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_energy:y_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_energy:y_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif

if (`caget -t FB_A:use_RF` != 'RF On') then
  set tmp=`caget FB_A:use_RF`
  set OKstatus="$OKstatus $tmp Not OK, Should read RF On\n"
endif
if (`caget -t FB_A:disp_optics` != 'Standard') then
  set tmp=`caget FB_A:disp_optics`
  set OKstatus="$OKstatus $tmp Not OK, Should read Standard\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_1` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_2` != 'used') then
  set tmp=`caget FB_A:BPM:use_disp:x_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_disp:x_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:x_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:x_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_1` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_2` != 'used') then
  set tmp=`caget FB_A:BPM:use_disp:y_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_disp:y_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_disp:y_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_disp:y_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_1` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_2` != 'used') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_4` != 'used') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:x_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_1` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_1`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_2` != 'used') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_2`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_3` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_3`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_4` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_4`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_5` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_5`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_6` != 'used') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_6`
  set OKstatus="$OKstatus $tmp Not OK, Should read used\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_7` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_7`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_8` != 'unused') then
  set tmp=`caget FB_A:BPM:use_en_disp:y_8`
  set OKstatus="$OKstatus $tmp Not OK, Should read unused\n"
endif
if (`echo $OKstatus` != 'FFB:') then
  set Foo=`caget -t IBC1H04CRCUR2`
  set Bar=`printf "%d" $Foo`
  if ($Bar > 50) then
    echo "$OKstatus Not OK"
  else
    echo "OK"
  endif
else
  echo "OK"
endif
