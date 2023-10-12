from pylab import *
import glob,warnings,shutil
import matplotlib as mp
import csv
from collections import Counter
import os
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
gfiles=sorted(glob.glob('*_r.csv'))
print(len(gfiles))


def split_and_count_oid(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        # Create a CSV reader
        reader = csv.reader(csv_file)
        
        # Initialize an empty dictionary to hold file writers and counters for each unique first column value
        writers = {}
        counters = {}
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Get the first column value (OID)
            oid = row[0]
            
            # If we haven't seen this OID before, create a new CSV writer and a new Counter for it
            if oid not in writers:
                # Open a new CSV file for writing
                output_file = open(f'{oid}.csv', 'w', newline='')
                
                # Create a new CSV writer
                writer = csv.writer(output_file)
                
                # Store the writer and output file in our dictionary
                writers[oid] = (writer, output_file)
                
                # Create a new Counter and store it in our dictionary
                counters[oid] = Counter()
            
            # Write the row to the appropriate CSV file
            writers[oid][0].writerow(row)
            
            # Increment the count for this OID
            counters[oid][oid] += 1
        
        # Find the OID with the maximum count
        max_oid = max(counters.items(), key=lambda x: x[1][x[0]])[0]
        
        # Close all of the CSV files we opened except for the one with the maximum count
        for oid, (writer, output_file) in writers.items():
            if oid != max_oid:
                output_file.close()
                os.remove(f'{oid}.csv')
        
        # Rename the file with the maximum count
        os.rename(f'{max_oid}.csv', f'{os.path.splitext(file_path)[0]}_split.csv')
        
        #print(f'The file with the maximum count of OID ({max_oid}) has been saved as {os.path.splitext(file_path)[0]}_split.csv')


def variability_test(name):
    a=np.genfromtxt(name,delimiter=',',unpack=True,usecols=3)
    #print(np.mean(a),np.std(a))
    k=[]
    n=len(a)
    for i in range(0,len(a)):
        k.append((a[i]-np.mean(a))**2)

    s=sum(k)/(n-1)
    t=std(a)/n
    f=np.sqrt((s-t)/np.mean(a)**2)*100
    return f
    #print(r"According to the F statistic, the variability  amplitude is %f. "%f)




count=0
with open('lc_stats2.csv','w') as f:

    for i in range(0,len(gfiles)):
    
        try:

                names=gfiles[i]
                #names=names[23:32]
                oid,dg,magg,ger=np.genfromtxt(names,delimiter=',',unpack=True,usecols=(0, 2,3,4))
                #print(np.mean(magg),np.median(magg),np.mean(ger),variability_test(names))#,np.mean(magi))
                split_and_count_oid(names)
                print('{} file split succesfully'.format(i+1))
        
        except ValueError:
            print('empty values!')
        except TypeError:
            print('empty file!!')

        pass





    ### testing the varibility usinf F test.
