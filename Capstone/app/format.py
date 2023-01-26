
from fileinput import filename
import csv
import os
import glob 
import sys 
import getopt 
import pandas as pd 
import math 

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
   
if __name__ == "__main__":
    path = main(sys.argv[1:]) 
    print(path)
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    for f in txt_files:
        parsedName = f.split("/")
        filename = parsedName[len(parsedName) - 1] #Filename is last term in parsed expression
    # read the csv file
        df = pd.DataFrame(pd.read_csv(f))
        df_edited = df
        df_edited.columns = ['raw_acc_x', 'raw_acc_y', 'raw_acc_z', 'raw_gyr_x', 'raw_gyr_y', 'raw_gyr_z','raw_pressure','time'];
        df_edited['time'] = df_edited['time'].apply(lambda x: x/math.pow(10, 6))
        f = f.replace(".txt",".csv")
        print(f)
        df_edited.to_csv(f, encoding='utf-8', index=False) # overwrites the input CSV with the edited version
        # print the location and filename
        print("Formatted data file created for" ,filename , "in", path)