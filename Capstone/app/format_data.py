
from fileinput import filename
import csv
import os
import glob 
import sys 
import getopt 
import pandas as pd 
import math 
import numpy as np

def main(argv):
    path = os.getcwd() #default path is working directory 
    try:
        opts, args = getopt.getopt(argv, "h:p:", 
                        ["path"])
    except:
        print("Usage: python3 format.py -p <PATH>")
        sys.exit(3)

    for opt, arg in opts:
        if opt == "-h":
            print("___.py -p <path>")
            sys.exit()
        if opt in ("-p", "--path"):
            path = arg
    return path


        
def format_data(path,out_path):
    txt_files = glob.glob(os.path.join(path, "*.csv"))
    for f in txt_files:
        parsedName = f.split("/")
        filename = parsedName[len(parsedName) - 1] #Filename is last term in parsed expression
    # read the csv file
        df = pd.DataFrame(pd.read_csv(f))
        df.columns = ['raw_acc_x', 'raw_acc_y', 'raw_acc_z', 'raw_gyr_x', 'raw_gyr_y', 'raw_gyr_z','raw_pressure','time'];
        ## Find Potential Data Logging Starts
        df['data_start'] = df.apply(lambda x: 0, axis=1)
        for i in range(0,len(df['time'])-1): 
            if df['time'].iloc[i+1]<df['time'].iloc[i]:
                df['data_start'].iloc[i+1] = 1
        s = df.index[df['data_start'] == 1].tolist()
        start = 0
        end = 0
        temp = 0
        interval = 0;
        #pick longest interval 
        for j in range(0, len(s)): 
                    interval = end - start
                    temp = s[j] 
                    if temp - end > interval:
                        start = end
                        end = temp
                        interval = end - start
        if(len(df)-end > interval):
            start = end
            end = len(df)             

        df_edited = df[start:end] #keep longest interval 
        
        df_edited.drop('data_start', axis=1,inplace=True)
        #Format Units 
        df_edited['time'] = df_edited['time'].apply(lambda x: x/math.pow(10, 6)) #us to s 
        df_edited['time'] = df_edited['time'].apply(lambda x: x - df_edited['time'].iloc[0])
        df_edited['raw_acc_x'] = df_edited['raw_acc_x'].apply(lambda x: x*9.80665)
        df_edited['raw_acc_y'] = df_edited['raw_acc_y'].apply(lambda x: x*9.80665)
        df_edited['raw_acc_z'] = df_edited['raw_acc_z'].apply(lambda x: x*9.80665) #convert to SI 
        df_edited['raw_pressure'] = df_edited['raw_pressure'].apply(lambda x: x*100) #HPa to Pa
        
        #Write Out Processed File 
        #f = f.replace(".csv","_formatted.csv") 
        df_edited.to_csv(out_path+filename, encoding='utf-8', index=False) #current behaviour is overwrite
        # print the location and filename
        print("Formatted data file created for" ,filename , "in", out_path)
   
if __name__ == "__main__":
    path = main(sys.argv[1:]) 
    print(path)
    format_data(path,path+'/'+'_formatted.csv')
    
    