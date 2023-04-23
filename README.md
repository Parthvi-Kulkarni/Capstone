## How to Set Up
1. Install Python and establish a virtual environment complete with standard packagages (numpy,pandas,scipy) which are used in data processing 
2. Extract the folder containing this repository in the local directory of choice
3. For detailed processing, ensure that FORM's ML repo is also setup correctly 
## How to Use
This codebase performs post-processing on the IMU data (Accelerometer and Gyroscope), as well as barometer data to obtain kick-related biomechanics metrics. It is made to be used with data downloaded from `offload.html` and RT Meta Outputs from the FORM goggle's sns files. 
To use this code either navigate to the working directory via command window, or an IDE of choice. 
### **Using Main**
1. Run the swim file obtained from the goggles through the meta-analysis pipeline
2. Extract the RT Meta output file obtained from Step 1
2. Rename the data file obtained from the fins as well as the RT csv so that the first two terms i.e. date_swimmername_xx_.csv match in **both** files 
4. Input the csv from the fins under the __data/input/fins__ folder and input the RT csv under the __data/input/goggles__ folder   
5. Run `main.py` in your python virtual environment. This will export a filtered, and formatted copy of both input files under respective __data\intermediate__ folders as well as export a csv containing all of the data, and processed metrics under __data\output__  
#### **Outputs**
1. A filtered, and formatted copy of both input files under respective __data\intermediate__ folders. 
2. A csv containing all of the raw data, as well as depth, and kick count under __data\output__ 
### **Using Kick Amplitude**
1. Download the dataset you want to analyze and copy the path of its location  
2. Change the path name in line 17 of KickAmplitudeRevised.py to this path  
3. Press Run   
#### **Outputs and Plots**
Through a number of filtering and windowing steps, this code transforms raw accelerometer and gyroscope data into useful biomechanics metrics and plots. 
1. The first plot that will be shown is of the quaternion distance travelled for each period over time. 
2. The second plot is of that same distance with vertical lines which indicate the start and stop of a kick window. 
3. The third plot will show that same quaternion distance within the window defined by the two vertical lines.
4. The fourth plot shows the gyroscope in the z direction within this window, overlayed with points that define a “zero-cross”. These are indicated when to be when the foot is stationary, i.e. at the top or bottom of each kick.The code will then output the number of kicks as well as the time of each kick. 
5. The fifth plot will show the absolute acceleration over time within the kick window. 
6. The sixth plot will show the up down angular amplitude of each kick over time. 
7. The seventh plot will show the total average angular amplitude per kick over time. 
8. Finally, the code will display the average amplitude over the entire kick window. 

### Things to Improve
1. Integrate Kicking Amplitude and Absolute Depth into the post-processing workflow
2. Define a barometer based kick-depth algorithim
3. Implement a better kick interval finding method. There is an apporach that uses matched filtering attached in this repo, that can be explored further. If storage limitations on the device are fixed and sufficient data is collected, higher order features can be exracted for machine learning models. 
4. Complete Kick Per Stroke Metric algorithim


