#!/bin/tcsh
set OKstatus="OK"
if (`caget -t FB_A:use_RF` != 'RF On') then
  caget FB_A:use_RF 
  echo "Should read RF On"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:isolate_en` != 'On') then
  caget FB_A:isolate_en
  echo "Should read On"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:disp_optics` != 'Standard') then
  caget FB_A:disp_optics
  echo "Should read Standard"
  OKstatus="Not OK"
endif
if (`caget -t FB_A:BPM:use:x_1` != 'used') then
  caget FB_A:BPM:use:x_1
  echo "Should read used"
  set OKstatus="Not OK"
endif
if (`caget -t FB_A:BPM:use:x_2` != 'unused') then
  caget FB_A:BPM:use:x_2
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_3` != 'unused') then
  caget FB_A:BPM:use:x_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_4` != 'unused') then
  caget FB_A:BPM:use:x_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_5` != 'unused') then
  caget FB_A:BPM:use:x_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_6` != 'used') then
  caget FB_A:BPM:use:x_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_7` != 'unused') then
  caget FB_A:BPM:use:x_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:x_8` != 'unused') then
  caget FB_A:BPM:use:x_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_1` != 'used') then
  caget FB_A:BPM:use:y_1
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_2` != 'unused') then
  caget FB_A:BPM:use:y_2
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_3` != 'unused') then
  caget FB_A:BPM:use:y_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_4` != 'unused') then
  caget FB_A:BPM:use:y_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_5` != 'unused') then
  caget FB_A:BPM:use:y_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_6` != 'used') then
  caget FB_A:BPM:use:y_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_7` != 'unused') then
  caget FB_A:BPM:use:y_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use:y_8` != 'unused') then
  caget FB_A:BPM:use:y_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_1` != 'used') then
  caget FB_A:BPM:use_energy:x_1
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_2` != 'unused') then
  caget FB_A:BPM:use_energy:x_2
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_3` != 'unused') then
  caget FB_A:BPM:use_energy:x_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_4` != 'used') then
  caget FB_A:BPM:use_energy:x_4
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_5` != 'unused') then
  caget FB_A:BPM:use_energy:x_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_6` != 'used') then
  caget FB_A:BPM:use_energy:x_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_7` != 'unused') then
  caget FB_A:BPM:use_energy:x_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:x_8` != 'unused') then
  caget FB_A:BPM:use_energy:x_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_1` != 'used') then
  caget FB_A:BPM:use_energy:y_1
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_2` != 'unused') then
  caget FB_A:BPM:use_energy:y_2
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_3` != 'unused') then
  caget FB_A:BPM:use_energy:y_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_4` != 'unused') then
  caget FB_A:BPM:use_energy:y_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_5` != 'unused') then
  caget FB_A:BPM:use_energy:y_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_6` != 'used') then
  caget FB_A:BPM:use_energy:y_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_7` != 'unused') then
  caget FB_A:BPM:use_energy:y_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_energy:y_8` != 'unused') then
  caget FB_A:BPM:use_energy:y_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif

if (`caget -t FB_A:use_RF` != 'RF On') then
  caget FB_A:use_RF
  echo "Should read RF On"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:disp_optics` != 'Standard') then
  caget FB_A:disp_optics
  echo "Should read Standard"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_1` != 'unused') then
  caget FB_A:BPM:use_disp:x_1
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_2` != 'used') then
  caget FB_A:BPM:use_disp:x_2
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_3` != 'unused') then
  caget FB_A:BPM:use_disp:x_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_4` != 'unused') then
  caget FB_A:BPM:use_disp:x_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_5` != 'unused') then
  caget FB_A:BPM:use_disp:x_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_6` != 'used') then
  caget FB_A:BPM:use_disp:x_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_7` != 'unused') then
  caget FB_A:BPM:use_disp:x_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:x_8` != 'unused') then
  caget FB_A:BPM:use_disp:x_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_1` != 'unused') then
  caget FB_A:BPM:use_disp:y_1
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_2` != 'used') then
  caget FB_A:BPM:use_disp:y_2
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_3` != 'unused') then
  caget FB_A:BPM:use_disp:y_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_4` != 'unused') then
  caget FB_A:BPM:use_disp:y_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_5` != 'unused') then
  caget FB_A:BPM:use_disp:y_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_6` != 'used') then
  caget FB_A:BPM:use_disp:y_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_7` != 'unused') then
  caget FB_A:BPM:use_disp:y_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_disp:y_8` != 'unused') then
  caget FB_A:BPM:use_disp:y_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_1` != 'unused') then
  caget FB_A:BPM:use_en_disp:x_1
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_2` != 'used') then
  caget FB_A:BPM:use_en_disp:x_2
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_3` != 'unused') then
  caget FB_A:BPM:use_en_disp:x_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_4` != 'used') then
  caget FB_A:BPM:use_en_disp:x_4
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_5` != 'unused') then
  caget FB_A:BPM:use_en_disp:x_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_6` != 'used') then
  caget FB_A:BPM:use_en_disp:x_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_7` != 'unused') then
  caget FB_A:BPM:use_en_disp:x_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:x_8` != 'unused') then
  caget FB_A:BPM:use_en_disp:x_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_1` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_1
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_2` != 'used') then
  caget FB_A:BPM:use_en_disp:y_2
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_3` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_3
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_4` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_4
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_5` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_5
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_6` != 'used') then
  caget FB_A:BPM:use_en_disp:y_6
  echo "Should read used"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_7` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_7
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`caget -t FB_A:BPM:use_en_disp:y_8` != 'unused') then
  caget FB_A:BPM:use_en_disp:y_8
  echo "Should read unused"
  OKstatus = "Not OK"
endif
if (`echo $OKstatus` != 'OK') then
  echo "Not OK"
else
  echo "OK"
endif
