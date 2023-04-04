file = '20230314-test2.csv';
Arduino = readtable(file);
Arduino = Arduino(690:3000,:); % length 1
%Arduino = Arduino(3401:end,:); %length 2
acc_z_raw = Arduino.Var3;
gyr_x_raw = Arduino.Var4;
gyr_y_raw = Arduino.Var5;
A_ax_raw = (Arduino.Var1);
A_ay_raw = (Arduino.Var2);
A_gz_raw = (Arduino.Var6);
A_gz_raw(end) = A_gz_raw(end-1);
A_ay_raw(end) = A_ay_raw(end-1);
%% testing
% x1 = normalize(A_ax_raw);
% y1 = normalize(A_ay_raw);
% z1 = normalize(acc_z_raw);
% x2 = normalize(gyr_x_raw);
% y2 = normalize(gyr_y_raw);
% z2 = normalize(A_gz_raw);
% abssq = sqrt(x1.^2+y1.^2+z1.^2+x2.^2+y2.^2+z2.^2);
% abssq1 = sqrt(z1.^2+x2.^2+y2.^2);
% plot(abs(acc_z_raw))
% hold on
% plot(abs(A_ay_raw))
% plot(abs(A_ax_raw))
% plot(sqrt(acc_z_raw.^2+A_ax_raw.^2+A_ay_raw.^2))
% hold off
% legend('z','y','x','tot')

%% IMUfilter
A_az = zeros(length(A_ax_raw),1);
A_gx = zeros(length(A_ax_raw),1);
A_gy = zeros(length(A_ax_raw),1);
A = [A_ax_raw, A_ay_raw, A_az];
G = [A_gx, A_gy, A_gz_raw]*pi/180;
vqf = VQF(1/88);
out = vqf.updateBatch(G, A);
pos = quaternion(out.quat6D);
quat = quaternion(pos);
distmat = zeros(length(pos),1);
for i = 2:length(pos)
    distmat(i) = rad2deg(dist(quat(i-1,:),quat(i,:)));
end

%% find interval 
plot((lowpass((distmat),0.1)))
moving_mean = movmean(lowpass((distmat),0.1),88);
greater = moving_mean>1;
first = find(greater,1,"first")-100;
%last = find(greater,1,"last")+100;
last = find(greater,1,"last");
figure
plot(distmat)
hold on
xline(first,LineWidth=2)
xline(last,LineWidth=2)
legend('Quaternion Data','Start','Stop')
title('Start and Stop Kick Detection')
hold off
%% IFFT
A_time = Arduino.Var8;
time = A_time/10^6;
time = time-time(1);
time(end) = time(end-1)+time(end-1)-time(end-2);
Arduino = Arduino(first:last,:); 
A_ax_raw = (Arduino.Var1);
A_ay_raw = (Arduino.Var2);
A_az_raw = (Arduino.Var3);
A_gx_raw = (Arduino.Var4);
A_gy_raw = (Arduino.Var5);
A_gz_raw = (Arduino.Var6);
A_gz_raw(end) = A_gz_raw(end-1);
time = time(first:last);
A_ax_fft = windowFilt(detrend(A_ax_raw),'A_ax','Acceleration [m/s^2]');
A_ay_fft = windowFilt(detrend(A_ay_raw),'A_ay','Acceleration [m/s^2]');
A_gz_fft = windowFilt(detrend(A_gz_raw),'A_gz','Angular Velocity [rad/s]');
[b,a] = butter(4,.1,'low');
figure
A_ax = A_ax_fft;
A_ay = A_ay_fft;
A_gz = A_gz_fft;
A_ax = filter(b,a,A_ax_fft);
A_ay = filter(b,a,A_ay_fft);
A_gz = filter(b,a,A_gz_fft);
subplot(3,1,1)
plot(A_ax,'color','red')
hold on
plot(A_ax_fft,'color','blue')
hold off
subplot(3,1,2)
plot(A_ay,'color','red')
hold on
plot(A_ay_fft,'color','blue')
hold off
subplot(3,1,3)
plot(A_gz,'color','red')
hold on
plot(A_gz_fft,'color','blue')
hold off
%% Zerocross
A_az = zeros(length(A_ax),1);
A_gx = zeros(length(A_ax),1);
A_gy = zeros(length(A_ax),1);
A = [A_ax, A_ay, A_az];
G = [A_gx, A_gy, A_gz]*pi/180;
vqf = VQF(1/88);
out = vqf.updateBatch(G, A);
pos = quaternion(out.quat6D);
quat = quaternion(pos);
compactq = compact(quat);
distmat = zeros(length(pos),1);
anglularDistance = [];
for i = 2:length(pos)
    distmat(i) = rad2deg(dist(quat(i-1,:),quat(i,:)));
end
figure
plot(distmat)
hold on
zind = diff(A_gz>0);
zerocross=zeros(sum(zind~=0)+2,2);
zerocross(1,:) = [1,0]; 
count = 2;
for i = 1:length(zind)
    if zind(i)~=0
        zerocross(count,1) = i+1;
        zerocross(count,2) = 0;
        count = count+1;    
    end
end
zerocross(end,1) = length(distmat);
if rem(length(zerocross),2) == 0
    zerocross(end,:) = [];
end
plot(zerocross(:,1),zerocross(:,2),'*')
title('Quaternion Angular Distance with Zerocrossing')
hold off
%% total acceleration
A_total = sqrt(A_ax.^2+A_ay.^2);
plot(A_total)
hold on
plot(zerocross(:,1),zerocross(:,2),'*')
%% quaternion amplitude
amplitude_pos = [];
amplitude_neg = [];
count_pos = 1;
count_neg = 1;
for i = 1:length(zerocross)-1
    if A_gz(round((zerocross(i+1,1)+zerocross(i))/2))>0
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        amplitude_pos(count_pos) = sum(distmat(i1:i2));
        count_pos = count_pos+1;
    else
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        amplitude_neg(count_neg) = sum(distmat(i1:i2));
        count_neg = count_neg+1;
    end
end
amplitude = [-amplitude_neg',amplitude_pos'];
mean_amp = (amplitude_pos+amplitude_neg)/2;
figure
bar(amplitude)
ylabel('amplitude [deg]')
xlabel('kick')
title('Up and Down Kick Amplitude')
subtitle(file,'Interpreter','none')
figure
bar(mean_amp)
ylabel('Amplitude [deg]')
title('Amplitude per Kick')
subtitle(file,'Interpreter','none')
%% jerk amplitude
acc_pos = [];
acc_neg = [];
count_pos = 1;
count_neg = 1;
for i = 1:length(zerocross)-1
    if A_gz(round((zerocross(i+1,1)+zerocross(i))/2))>0
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        acc_pos(count_pos) = max(A_total(i1:i2))^2/(time(i2)-time(i1));
        count_pos = count_pos+1;
    else
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        acc_neg(count_neg) = max(A_total(i1:i2))^2/(time(i2)-time(i1));
        count_neg = count_neg+1;
    end
end
acc_amp = [-acc_neg',acc_pos'];
figure
bar(acc_amp)
ylabel('Jerk [m^2/s^5]')
xlabel('kick #')
title('Up and Down Kick Jerk Cost')
subtitle(file,'Interpreter','none')
%% Velocity amplitude
vel_pos = [];
vel_neg = [];
count_pos = 1;
count_neg = 1;
for i = 1:length(zerocross)-1
    if A_gz(round((zerocross(i+1,1)+zerocross(i))/2))>0
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        vel_pos(count_pos) = trapz(time(i1:i2),A_total(i1:i2));
        count_pos = count_pos+1;
    else
        i1 = zerocross(i,1);
        i2 = zerocross(i+1,1);
        vel_neg(count_neg) = trapz(time(i1:i2),A_total(i1:i2));
        count_neg = count_neg+1;
    end
end
vel_amp = [-vel_neg',vel_pos'];
figure
bar(vel_amp)
ylabel('velocity [m/s]')
xlabel('kick #')
title('Up and Down Kick Velocity')
subtitle(file,'Interpreter','none')

%% Window FFT
function var = windowFilt(raw,varnam,type)
    Fs = 88;
    L = length(raw);
    T = 1/Fs;
    t = (0:L-1)*T;
    var = [];
    Y = fft(raw);
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs*(0:(L/2))/L;
    PX = sort(P1);
    lim = PX(round(end-L/2*.05));
    Y(P2 < lim) = 0;
    P2 = abs(Y/L);  
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = Fs*(0:(L/2))/L;
    var = ifft(Y);
    figure
    subplot(1,2,1)
    plot(raw)
    hold on
    plot(var)
    title(varnam,'Interpreter','none')
    subtitle('filtered vs. unfiltered')
    ylabel(type,'Interpreter','none')
    legend('filtered','raw')
    subplot(1,2,2)
    plot(var)
    title(varnam,'Interpreter','none')
    subtitle('')
    ylabel(type,'Interpreter','none')
end

