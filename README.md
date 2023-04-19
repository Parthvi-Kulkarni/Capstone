## How to Set Up
1. Install python here.
2. Install a python IDE such as PyCharm. 
3. Download the zip folder contained in this GitHub.
## How to Use
This codebase allows us to perform post-processing on the IMU data (Accelerometer and Gyroscope) to obtain biomechanics metrics. It is made to be used with data downloaded from the web app.
1. Download the dataset you want to analyze and copy the path of its location. 
2. Change the path name in line 17 of KickAmplitudeRevised.py to this path. 
3. Press Run. 
## Outputs and Plots
Through a number of filtering and windowing steps, this code transforms raw accelerometer and gyroscope data into useful biomechanics metrics and plots. 
1. The first plot that will be shown is of the quaternion distance travelled for each period over time. 
2. The second plot is of that same distance with vertical lines which indicate the start and stop of a kick window. 
3. The third plot will show that same quaternion distance within the window defined by the two vertical lines.
4. The fourth plot shows the gyroscope in the z direction within this window, overlayed with points that define a “zero-cross”. These are indicated when to be when the foot is stationary, i.e. at the top or bottom of each kick.The code will then output the number of kicks as well as the time of each kick. 
5. The fifth plot will show the absolute acceleration over time within the kick window. 
6. The sixth plot will show the up down angular amplitude of each kick over time. 
7. The seventh plot will show the total average angular amplitude per kick over time. 
8. Finally, the code will display the average amplitude over the entire kick window. 
