fs = 192000;
recObj = audiorecorder(fs, 16, 1);

if fs == 44100
    display("hih")
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig120.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig150.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig180.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig220.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));
end

if fs == 192000

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig120_2.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig150_2.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig180_2.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sig220_2.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/or_sig1000_2.dat';
    or_sig1000 = csvread(f_name);
    or_sig1000 = or_sig1000/(std(or_sig1000)*length(or_sig1000));

end

recDuration = 5;
disp("Begin speaking.")
recordblocking(recObj,recDuration);
disp("End of recording.")

doubleArray = cast(getaudiodata(recObj, 'int16'), "double");
k = conv(doubleArray.^2, ones(1000,1)/1000);
amps = k(500:(end-500)).^0.5;
norm_data = doubleArray./amps;

sigs150 = sig150(1:3500);
sigs180 = sig180(1:3500);
sigs120 = sig120(1:3500);
sigs220 = sig220(1:3500);
sigs1000 = or_sig1000(1:3500);

conv150 = xcorr(norm_data, sig150);
conv180 = xcorr(norm_data, sig180);
conv120 = xcorr(norm_data, sig120);
conv220 = xcorr(norm_data, sig220);
conv1000 = xcorr(norm_data, sigs1000);

conv150 = conv150(round(length(conv150)/2):end);
conv180 = conv180(round(length(conv180)/2):end);
conv120 = conv120(round(length(conv120)/2):end);
conv220 = conv220(round(length(conv220)/2):end);
conv1000 = conv1000(round(length(conv1000)/2):end);


amp150 = conv(conv150.^2, ones(1000,1)/1000).^0.5;
amp180 = conv(conv180.^2, ones(1000,1)/1000).^0.5;
amp120 = conv(conv120.^2, ones(1000,1)/1000).^0.5;
amp220 = conv(conv220.^2, ones(1000,1)/1000).^0.5;




figure(1);clf;
hold on;
plot(conv150, "-b");
plot(conv180, '-r');
plot(conv120, "-p");
plot(conv220, "-g");
plot(conv1000, "-o");
hold off
%figure(2);clf;
%hold on;
%plot(conv150(200000:201000), '-b');
%plot(conv180(200000:201000), '-r');
%plot(conv120(200000:201000), '-p');
%plot(conv220(200000:201000), '-g');
%hold off;


