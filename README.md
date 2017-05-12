# TaiHu
To enchance water index for slender river, border of open water and so on by logical approach.


# dependency package
GDAL
numpy
PyQt4


# main modual
pypt.py


# needed image
water index:
    * in this code,EWI(enchanced water index was used)
    * wich is performed following the equation: (TM_2-TM_4-TM_5)/(TM_2+TM_4+TM_5)
    * Each subscript refers to a corresponding band number of TM sensor.
directional convolutions:
    * the directional filter can be found in ENVI:
    * Filter -> Convolutions and Morphology Tool -> Directional
    * only two directions were used : 180 and 270
    
    