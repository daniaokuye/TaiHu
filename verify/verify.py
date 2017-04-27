#coding:utf-8

from TH.Image import cRaster
import numpy as np

#myT='F:\\Landsat\\tai_hu\\direction\\verify\\myTool.tif'
ewi ='F:\\Landsat\\tai_hu\\direction\\EWI.tif'
output='F:\\Landsat\\tai_hu\\direction\\verify\\ewi_'
#inf='F:\\Data\\test\\nlzz_\\testField\\overlap_new.tif'
#outf='F:\\Data\\test\\nlzz_\\testField\\overlap_new2.tif'
IMG = cRaster()
Numdata=IMG.Iread(ewi)
data=Numdata[0]#
print 'ok'
thresH=-0.4
x=(0.2+0.5)/0.05
for i in range(int(x)+1):
    out=np.where(data>thresH,1,0)
    out=out.astype(np.uint8)
    thresH+=0.05
    Oput=output+repr(i)+'.tif'
    c=[out]+list(Numdata[1:])+[Oput]
    IMG.Iwrite(*c)




































