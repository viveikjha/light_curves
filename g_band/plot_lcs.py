from pylab import *
import glob,warnings,shutil
#from run_iccf import run_ccf
import matplotlib as mp
from astropy.stats import sigma_clip

mp.rcParams['font.family']='serif'
mp.rcParams['xtick.major.size']=10
mp.rcParams['xtick.major.width']=2
mp.rcParams['xtick.minor.size']=7
mp.rcParams['xtick.minor.width']=2
mp.rcParams['ytick.major.size']=10
mp.rcParams['ytick.major.width']=2
mp.rcParams['ytick.minor.size']=7
mp.rcParams['ytick.minor.width']=2
mp.rcParams['axes.linewidth']=2
mp.rcParams['xtick.labelsize']=3
mp.rcParams['ytick.labelsize']=3


warnings.filterwarnings("ignore")
gfiles=sorted(glob.glob('*split.csv'))
#rfiles=sorted(glob.glob('dr6/agn_mass_dr6/*r.txt'))
#ifiles=sorted(glob.glob('dr6/agn_mass_dr6/*i.txt'))
#names=np.genfromtxt('source_info_z_mbh.csv',usecols=0,delimiter=',',dtype=str)
#names=(sorted(names))
print(len(gfiles))

def variability_test(name):
    a=np.genfromtxt(name,delimiter=' ',unpack=True,usecols=1)
    #print(np.mean(a),np.std(a))
    k=[]
    n=len(a)
    for i in range(0,len(a)):
        k.append((a[i]-np.mean(a))**2)

    s=sum(k)/(n-1)
    t=std(a)/n
    f=np.sqrt((s-t)/np.mean(a)**2)*100
    print(name,f)
    #print(r"According to the F statistic, the variability  amplitude is %f. "%f)


def BinLightCurveFiveDayInterval(MJD,mag,magErr, dt):
    import numpy as np
    '''
    #MJD changes at midnight in Greenwich. We want to make sure that observations taken at the same night in
    Palomar are binned together (UT-8)! E.g. observations can be from 5-ish in the evening, which corresponds to 1+-1 in UT
    to the next morning, say 6-ish, which is in the afternoon in UT. So we need to bin observations with the same MJD
    same day observations
    #    print np.shape(MJD)
     obtained from https://github.com/noahkrever/pg1302/blob/c800f9ac491180013466b8e08ed300fdc94df700/functions/BinLightCurve.py
    -------------------------------------------------------
    '''


    MJD2=np.floor(MJD);
    # print np.max(MJD2)+5
    # print np.ceil((np.max(MJD2)+5-np.min(MJD2))/5)
    LinearGrid=np.arange(np.ceil((np.max(MJD2)+dt+1-np.min(MJD2))/dt))*dt+np.min(MJD2)
    
    # print LinearGrid
#    LinearGrid=np.linspace(np.min(MJD2),np.max(MJD2),np.ceil((np.max(MJD2)-np.min(MJD2))/5))

    MJD_Unique, MJD_UnIndices = np.unique(MJD2, return_inverse=True)
    
    #    print np.shape(MJD_Unique)
    MJD_temp=np.zeros(len(LinearGrid)-1)
    mag_temp=np.zeros(len(LinearGrid)-1)
    magErr_temp=np.zeros(len(LinearGrid)-1)
    #    print MJD2
    #    weighted average based on photometric error____MAKE SURE THIS IS CORRECT
    for i in np.arange(len(LinearGrid)-1):
        #        print i
        iii=np.where((MJD2>=LinearGrid[i])&(MJD2<LinearGrid[i+1]))
        #        print np.shape(iii)
        if np.shape(iii)[1]>=1:
            W=np.sum(1.0/magErr[iii]**2)
            wei=1.0/(W*magErr[iii]**2)



            MJD_temp[i]=np.average(MJD[iii], axis=None, weights=wei, returned=False)
            mag_temp[i]=np.average(mag[iii], axis=None, weights=wei, returned=False)
    #        magErr_temp[i]=np.average(magErr[iii], axis=None, weights=wei, returned=False)
            magErr_temp[i]=np.sqrt(np.sum(wei**2*magErr[iii]**2))
        else:
            MJD_temp[i]=-5
            mag_temp[i]=-5
            magErr_temp[i]=-5

#    print MJD_temp
#    print mag_temp
#    print magErr_temp
    kk=np.where(MJD_temp==-5)
    MJD=np.delete(MJD_temp,kk)
    kk=np.where(mag_temp==-5)
    mag=np.delete(mag_temp,kk)
    kk=np.where(magErr_temp==-5)
    magErr=np.delete(magErr_temp,kk)
    
    #    print MJD
    
    return MJD,mag,magErr


count=0
length=[]
with open('lc_stats2.csv','w') as f:

    for i in range(0,len(gfiles)):
        #variability_test(gfiles[i])
        #count+=1


        try:

                #run_ccf(gfiles[i],rfiles[i],0,1,2)
                #run_ccf(gfiles[i],ifiles[i],0,1,2)
                #running_javelin(gfiles[i],rfiles[i],ifiles[i])
                #print(gfiles[i],len(gfiles[i]))

                #print('No. {} done'.format(i+1))
                #print(i,gfiles[i])
                names=gfiles[i]
                #names=names[23:32]
                dg,magg,ger=np.genfromtxt(gfiles[i],delimiter=',',unpack=True,usecols=( 2,3,4))
                #dr,magr,rer=np.genfromtxt(rfiles[i],delimiter=',',unpack=True,usecols=( 3,4,5))
                #di,magi,ier=np.genfromtxt(ifiles[i],delimiter=',',unpack=True,usecols=( 3,4,5))
                #print(len(magi))#,len(magr),len(magi))
                #print(names,np.mean(magg),np.median(magg),np.mean(ger))#,np.mean(magi))
               

                ndate,nflux,nerr=BinLightCurveFiveDayInterval(dg,magg,ger,3)
                filtered_g = sigma_clip(nflux, sigma=3)
                print(ndate[len(filtered_g)-1])
                years=(ndate[len(filtered_g)-1]-ndate[0])/365
                print(years)
                length.append(years)
               
                '''
                if (len(magi) > 15):
                    count+=1
                    #print(count,len(magg),len(magr),len(magi))

                    folder='/home/vivek/workhub/ztf-project/good_lc/'
                    shutil.copy(gfiles[i],folder)
                    shutil.copy(rfiles[i],folder)
                    shutil.copy(ifiles[i],folder)

                glc=[]
                '''
                ### Comment here
                fig = plt.figure()
                #fig.subplots_adjust(hspace=0.5, wspace = 0.4)

                #Plot lightcurves

                ax1 = fig.add_subplot(1, 1, 1)

                ax1.plot(ndate,filtered_g,color='green',marker='o',lw=0,markersize=10,markeredgecolor='black',markeredgewidth=1,label='g-band')
                ax1.errorbar(ndate,filtered_g, yerr = nerr, fmt =' ', color = 'green',lw=1,capsize=0)
                #ax1.plot(dr,magr+1,color='blue',marker='|',lw=0,markersize=40,markeredgewidth=5,label='r-band')
                #ax1.errorbar(dr, magr+1, yerr = rer,fmt=' ', lw=1,color = 'purple',capsize=0)
                #ax1.plot(di,magi+2,color='teal',marker='|',lw=0,markersize=40,label='i-band')
                #ax1.errorbar(di, magi+2, yerr = ier,fmt=' ', lw=1,color = 'teal',capsize=0)


                #ax1.set_ylim(15.1,16.2)
                ax1.tick_params(axis="both",direction="in",labelsize=20)
                ax1.tick_params(axis="both",which='minor',direction="in",labelsize=20)
                ax1.yaxis.set_ticks_position('both')
                #ax1.get_xaxis().set_visible(False)
                #ax1.xaxis.set_ticks_position('both')
                ax1.minorticks_on()
                #ax1.vlines([58400,58800],14,21,colors='gray',lw=1)
                #x1.vlines([58200,58450],14,21,colors='gray',ls='--',lw=1)
                #ax1.fill_between(magg, 0,where = (dg > 58400) & (dg <= 58800),color = 'g',alpha=0.2)

                ax1.invert_yaxis()
                ax1.set_xlabel('JD - 2400000',fontsize=36)
                ax1.set_ylabel('  magnitude ',fontsize=36)
                plt.legend(fontsize=36)
                plt.subplots_adjust(hspace=.0)
                plt.grid()
                plt.title('{}, {} years'.format(names, round(years,2)),fontsize=24)

                plt.subplots_adjust(wspace=None, hspace=None)

                plt.legend(fontsize=36)
                fig.set_size_inches(11.69,8.27)
                #plt.savefig('{}_preview.png'.format(names)) 
                #print('File named {} and number {} saved'.format(names,i))
                #plt.close()
                plt.show()
            
        except ValueError:
            print('empty values!')
        except TypeError:
            print('empty file!!')

        pass

plt.hist(length)
plt.show()



    ### testing the varibility usinf F test.
