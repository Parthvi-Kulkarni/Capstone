from pickle import FALSE
import pandas as pd
import numpy as np
import sys 
import glob 
import getopt 
import os

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

# Read csv file from Meta Analysis Output
def _read_csv_(path,filename):
    path = path + "/" + filename
    df_RT = pd.read_csv(path, sep=",", header=None)
    return df_RT


# Create template of updated df
def _create_template_df_(df):
    df_output = pd.DataFrame(columns=["Swimmer Name", "Date", "Length Index", "Length Category",
                                      "Stroke Type", "Length Time", "Stroke Count", "Stroke Rate", "Responsiveness",
                                      "Max Push Off Velocity","Average Underwater Velocity", "Distance per Stroke"])
    index = 0
    for i in range(0, df.shape[0]):
        d = pd.DataFrame({
            "Name": "",
            "Date": "",
            "Length Index": df.iloc[i, 0],
            "Length Category": "empty",
            "Stroke Type": _change_stroke_type_(df.iloc[i, 1]),
            "Length Time": df.iloc[i, 6],
            "Stroke Count": df.iloc[i, 7],
            "Stroke Rate": df.iloc[i, 8],
            "Responsiveness": df.iloc[i, 9],
            "Max Push Off Velocity": df.iloc[i, 21],
            "Average Underwater Velocity": df.iloc[i, 23],
            "Distance per Stroke": df.iloc[i,25],
        }, index=[index])
        df_output = pd.concat([df_output, d], sort=False)
        index += 1
    return df_output

def _create_RT_template_df_(df):
    df_output = pd.DataFrame(columns=["Name", "Date", "Length Index", "Stroke Type", "Length Start Time", "Length End Time", "Stroke Rate", "Stroke Rate RT", "Stroke Rate RT timestamp", "Stroke Rate RT P Class", "CNN predictions", "Rest"])
    index = 0
    for i in range(0, df.shape[0]):
        d = pd.DataFrame({
            "Name": "",
            "Date": "",
            "Length Index": df.iloc[i, 0],
            "Stroke Type": _change_stroke_type_(df.iloc[i, 1]),
            "Length Start Time": df.iloc[i, 2],
            "Length End Time": df.iloc[i,3],
            "Stroke Rate": df.iloc[i, 4],
            "Stroke Rate RT": df.iloc[i, 5],
            "Stroke Rate RT timestamp": df.iloc[i, 6],
            "Stroke Rate RT P Class": df.iloc[i, 7],
            "CNN predictions": df.iloc[i, 8],
            "Rest": df.iloc[i, 9],
        }, index=[index])
        df_output = pd.concat([df_output, d], sort=False)
        index += 1
    return df_output



# Modify Name Column
def _modify_name_column_(df, name):
    for i in range(0, df.shape[0]):
        df.iloc[i, 0] = name
    return df


# Modify Date Column
def _modify_date_column_(df, date):
    for i in range(0, df.shape[0]):
        df.iloc[i, 1] = date
    return df


# Get Rest from Df
def _get_rest_(df):
    rest_df = pd.DataFrame(columns=["Rest Index", "Length Index Before", "Rest Time"])
    rest_index = 1
    for i in range(0, df.shape[0]-1):
        if df.iloc[i, 3] != df.iloc[i+1, 2]:
            d = pd.DataFrame({
                "Rest Index": rest_index,
                "Length Index Before": df.iloc[i, 0],
                "Rest Time": df.iloc[i+1, 2] - df.iloc[i, 3]
            }, index=[rest_index-1])
            rest_df = pd.concat([rest_df, d], sort=False)
            rest_index += 1
    return rest_df


# Add Rest to Modified DF based on rest DF
def _add_rest_(df, df_rest):
    for i in range(0, df_rest.shape[0]):
        d = pd.DataFrame({
            "Name": "",
            "Date": "",
            "Length Index": 0,
            "Length Category": "rest",
            "Stroke Type": "rest",
            "Length Time": df_rest.iloc[i, 2],
            "Stroke Count": 0,
            "Stroke Rate": 0,
            "Responsiveness": 0,
            "Max Push Off Velocity":0,
            "Average Underwater Velocity":0,
            "Distance per Stroke":0
        }, index=[df_rest.iloc[i, 1]-0.5])
        df = pd.concat([df,d], ignore_index=False, sort=False)
    df = df.sort_index().reset_index(drop=True)
    return df


# Assign Length Categories
def _assign_length_categories_(df):
    if df.iloc[0, 3] == "empty":
        df.iloc[0, 3] = "first"
    for i in range(1, df.shape[0]-1):
        if df.iloc[i, 3] == "empty" and i == 0:
            df.iloc[i, 3] = "first"
        elif df.iloc[i, 3] == "empty" and df.iloc[i-1, 3] == "rest":
            df.iloc[i, 3] = "first"
        elif df.iloc[i, 3] == "empty" and df.iloc[i+1, 3] == "rest" and df.iloc[i-1, 3] != "rest":
            df.iloc[i, 3] = "last"
        elif df.iloc[i, 3] == "empty" and df.iloc[i-1, 3] != "rest" and df.iloc[i+1, 3] != "rest":
            df.iloc[i, 3] = "middle"
    if df.iloc[df.shape[0]-1, 3] == "empty" and df.iloc[df.shape[0]-2, 3] != "rest":
        df.iloc[df.shape[0] - 1, 3] = "last"
    if df.iloc[df.shape[0]-1, 3] == "empty" and df.iloc[df.shape[0]-2, 3] == "rest":
        df.iloc[df.shape[0] - 1, 3] = "first"
    return df


# Change stroke type to correct label and return it
def _change_stroke_type_(num):
    if num == 1:
        st = "BF"
    elif num == 2:
        st = "BK"
    elif num == 3:
        st = "BR"
    elif num == 4:
        st = "FR"
    elif num == 5:
        st = "BF KICK"
    elif num == 6:
        st = "BK KICK"
    elif num == 7:
        st = "BR KICK"
    elif num == 9:
        st = "FR KICK"
    else:
        st = "Drill"
    return st

# Extract Name and Date
def _extract_name_date_(file_name):
    first_name = file_name.split('_')[0]
    #last_name = file_name.split('_')[1]
    date = file_name.split('_')[1]
    name = first_name #+ " " + last_name
    return name, date


# Full Meta Output Parser
def meta_parser(path,out_path, input_name):
    df_RT = _read_csv_(path, input_name)
    swimmer_name, swim_date = _extract_name_date_(input_name)
    df_RT = _create_RT_template_df_(df_RT)
    df_RT = _modify_name_column_(df_RT, swimmer_name)
    df_RT = _modify_date_column_(df_RT, swim_date)
    if os.path.exists(out_path) == False:
        os.makedirs(out_path)
    input_name = input_name.replace(".csv","_formatted.csv")
    df_RT.to_csv(out_path +
              input_name , index=False)


def parseRT(path,out_path):
    txt_files = glob.glob(os.path.join(path, "*.csv"))
    for f in txt_files:
        parsedName = os.path.splitext(f)[0]
        parsedName = f.split("/")
        filename = parsedName[len(parsedName) - 1] #Filename is last term in parsed expression
        print(filename)
        meta_parser(path,out_path,filename)
        
if __name__ == "__main__":
    path = main(sys.argv[1:]) 
    parseRT(path,path)
