#coding:utf-8
'''
this file is used to calculate 
some point need to notice if one want use this code:
1.enhanced water index(EWI) is a water index. 
    for landsat 5: EWI = (TM2-TM4-TM5)/(TM2+TM4+TM5)
2.inputfile come from EWI with calculation of directional spatial opertor 
    it's better to gather both two direction:row and clomun.
    you are encouraged to change inputfile to your local dir. in your machine
3.we suppose all the calculation is carried out by row,
    so clomun direction should interchange its axes
4.firstly, we make a smoothness for result of opertor; 
    secondly, the selected zone of opertor's result should satisfied:
                    1.extreme max value should greater than 0
                    2.the selected zone range from exreme min to max
                    3.the change must be steep.
                        In other words,too gently transformation may not be water body
'''
from TH.Image import cRaster
import numpy as np
from TH.noise_rid import noiseRid

inputfile ='D:/360Downloads/test/beiJ_90_new.tif'   #one result of directional spatial opertor
ewi ='D:/360Downloads/test/beiJ_EWI.tif'            #EWI
outfile = 'D:/360Downloads/test/beiJ_90_out.tif' #outputfile


IMG = cRaster()
Numdata=IMG.Iread(inputfile)#return a tuple:im_data,im_geotrans,im_proj
data=Numdata[0]
if data.dtype==np.int16:
    data=data.astype(np.int32)

#interchange two axes. don't do this step if directional opertor is zero
#because following code is based on direction of zero.
#therefore, all the data preparing for calculation should follow similiar style
data=np.swapaxes(data,0,1)

ratioData=IMG.Iread(ewi)
ratioD=ratioData[0] #EWI
#so does  the varible "data"
ratioD=np.swapaxes(ratioD,0,1)#

#we will select some zone from "inputfile" row by row
new_data=data#for saving result of selected zone row by row
#这个存储的是符合3要求的纹理区域
#there are three demands for selected zone,"slop_data"
slop_data=data*0
corrected_data=ratioD#需要做调整的ewi;this is used to save corrected EWI
per_data=data*0.0#用来存储水体占比;percent of water body in a section
#用来存储水体占比总超过一定数值的地方
#when percent in local section greater than certain number, 
#this local zone will be saved in "extract_data"
extract_data = data.astype(np.int)*0


#print data.dtype,'\n',data.shape

line,col=data.shape
#print line,'col=',col
# we will smoothness by Ksize*Ksize
Ksize=5#kernel size used to smoothness
k=(Ksize-1)/2 #avoid border of image

'''
the following 3 varible is used to smoothness
we want adopt a dynamic threshold for smoothness
1.we employed stddev of EWI
2.for local zone, we want adopt this selected threshold be changeable along feature of locla zone
3.text and t decide the size of local zone. max,min,mean are used to behalf of feature of zone
'''
text=3#determine the size of local zone , and then the varible "limit"
t=(text-1)/2
# limit=3000 this is used as threshold for slope;one of the demands should satisfied
limit=np.std(data)
EWIlimit=np.std(ratioD)
#print 'limit',limit

for l in range(line):
    for i in range(col):
        
        ##  1.out of place 
        if (i-k <= 0) or (i+k >= (col-1)):
            continue
        #均值; mean of kernel size
        zone=data[l][i-k:i+k+1]
        temp=np.sum(zone)/float(Ksize)
        #obtain the factor to adjust limit 
        if(l-t<0):
            limit_zone=data[0:text,i-k:i+k+1]
        elif(l+t+1>line):
            limit_zone=data[-text:,i-k:i+k+1]
        else:
            limit_zone=data[l-t:l+t+1,i-k:i+k+1]
        LMin=np.min(limit_zone)#feature of this zone
        LMax=np.max(limit_zone)
        LMean=np.mean(limit_zone)
        #1.6 is a expirical factor, all this determine the output factor "Ldiv"
        if(LMean-LMin>1.6*limit or LMax-LMean>1.6*limit):
            Ldiv=0.1
        else:
            Ldiv=1
        if abs(data[l][i]-temp)<(limit*Ldiv):
            new_data[l][i]=temp#data  smoothness
        else:
            new_data[l][i]=data[l][i]#data that keep original state
        
    if l%500 == 0:
        print l,
#for now ,all data in this column has been smoothed   

data=new_data#del original "data"
#特点：1.极小值小于0；2.区间是极小值到极大值；3.变化陡峭
#demands should satisfied:1.extreme min less than 0;2.range;3.steep 

#Numdata=IMG.Iread(inputfile)
Noise=noiseRid()

for l in range(line):
    end=0#the index in column 
    dataL=data[l]#carry out corrected method row by row
    
    for i in range(col-1):
        if i<=end:#pass these pixels has been calculated
            continue
        ##  2.find out slope/range of gradient in the first place
        temp=dataL[i+1] - dataL[i]      #gradient
        start=i#find out range of slope
        while(temp>0 and i<col-2):
            i=i+1
            temp=dataL[i+1] - dataL[i]
        end=i
        if(start!=end):
            zone=dataL[start:end+1]        #range meet demands 1&2
            if(zone[0]>0):#extreme min value, it should less than 0
                continue
            tempZone = np.hstack((zone[0],zone[:-1]))
            slop=zone-tempZone              #calculate the gradient,marked as slope
            if(np.max(slop)<limit):#a solution to valid the magnitude of steep
                continue
            slop_data[l,start:end+1]=zone#all demands meet, saved this range into "slop_data"
            
            reflect=list(ratioD[l,start:end+1]) #EWI
            
            #有部分数值，他们本身不具有梯度的特征，但是由于算子本身的特点，使得部分
            #值也呈现出梯度的样式。特别是有较长的渐变的特征。他们的总体规律是：
            #1、EWI指数方差不足0.1个总体方差。2.其值最大不超过常规EWI阈值。
            #这儿取0.1是因为关注的细小水体，其值是EWI统计值的0.1个精度上
#             if(np.std(reflect)<(0.1*EWIlimit) ):
#                 continue
            
            #用来检测由于相似邻域,只调整梯度
            
            #print reflect,list(zone)
            mnf = Noise.mnf(reflect, list(zone))
            #调整值落在【-1,1】之间。
            adjust = np.where(mnf < -1, -1, mnf)
            adjust = np.where(mnf > 1, 1, adjust)
            #计算百分比
            percent = Noise.percent(adjust)
                
            try:
                per_data[l,start:end+1] = percent
                if(np.sum(percent) > 0.8 and np.max(percent) > 0.5):
                    extract_data[l,start:end+1] = 1
            except Exception,e:
                print "ppp:",e
            try:
                corrected_data[l,start:end+1] = adjust
            except Exception,e:
                print "ooo:",e   
            #print 'ok',start,end
            
            
        
    if l%500 == 0:
        print l,'l'       
#     
#     
#     
#     
#     ,slop_data[np.newaxis,:]
out=np.concatenate([extract_data[np.newaxis,:],per_data[np.newaxis,:],corrected_data[np.newaxis,:]],axis=0)
out=np.swapaxes(out,1,2)#翻转123-3
corrected_data=np.swapaxes(corrected_data,0,1)
print 'now',np.min(data)
c=[out]+list(Numdata[1:])+[outfile]
IMG.Iwrite(*c)  













 
