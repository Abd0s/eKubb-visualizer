t = tcpclient('localhost', 51001);

begin_byte = 43;
end_byte = 45;

% Handshake request
write(t, uint8([begin_byte, 1, end_byte]))
% Handshake confirm response
acknowledge_message = read(t, 3);
if acknowledge_message == uint8([43, 2, 45])
   fprintf("Handshake completed\n")
else
   fprintf("Handshake failed\n")
   acknowledge_message
end

% Test log
write(t, uint8([begin_byte, 4, 2, end_byte]))

fs = 192000;
recObj = audiorecorder(fs, 16, 1);

if fs == 44100
    f_name = 'sigs/sig120.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));
    
    f_name = 'sigs/sig150.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));
    
    f_name = 'sigs/sig180.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));
    
    f_name = 'sigs/sig220.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));
end

if fs == 192000

    f_name = 'sigs/sig120_2.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));

    f_name = 'sigs/sig150_2.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));

    f_name = 'sigs/sig180_2.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));

    f_name = 'sigs/sig220_2.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));

    f_name = 'sigs/or_sig220_2.dat';
    or_sig220 = csvread(f_name);
    or_sig220 = or_sig220/(std(or_sig220)*length(or_sig220));

    f_name = 'sigs/or_sig1000_2.dat';
    or_sig1000 = csvread(f_name);
    or_sig1000 = or_sig1000/(std(or_sig1000)*length(or_sig1000));

end

count_geel = 0;
count_blauw = 0;
count_rood = 0;
count_groen = 0;

disp("Begin speaking.")
record(recObj);
pause(0.2);
while count_geel < 5
    
    doubleArray = cast(getaudiodata(recObj, 'int16'), "double");

    if length(doubleArray) > 200000
        doubleArray = doubleArray(end-200000:end);
    end

    k = conv(doubleArray.^2, ones(1000,1)/1000);
    amps = k(500:(end-500)).^0.5;
    norm_data = doubleArray./amps;
    
    conv150 = xcorr(norm_data, sig150);
    conv180 = xcorr(norm_data, sig180);
    conv120 = xcorr(norm_data, sig120);
    conv1000 = xcorr(norm_data, or_sig1000);
    %conv220 = xcorr(norm_data, or_sig220);

    conv150 = conv150(round(length(conv150)/2):end);
    conv180 = conv180(round(length(conv180)/2):end);
    conv120 = conv120(round(length(conv120)/2):end);
    conv1000 = conv1000(round(length(conv1000)/2):end);
    
    [maxi, indx] = max(abs(conv120));
    treshold = 25000;
    max_treshold = 0.18;
    big_spike_treshold = 0.6;
    max_division = 1.5;
    count_up = false;
    if maxi >= big_spike_treshold
        fprintf("Geel Omgevallen")
        write(t, uint8([begin_byte, 5, 0, end_byte]))
        %count_geel = count_geel + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv120) - treshold && maxi > max_treshold
        if sum(abs(conv120(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv120(indx-treshold:indx)))/treshold >= max_treshold/max_division
            fprintf("Geel Omgevallen")
            write(t, uint8([begin_byte, 5, 0, end_byte]))
            %count_geel = count_geel + 1
            count_up = true;
        end
    end
    [maxi, indx] = max(abs(conv150));
    if maxi >= big_spike_treshold
        fprintf("Blauw Omgevallen")
        write(t, uint8([begin_byte, 5, 1, end_byte]))
        %count_blauw = count_blauw + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv150) - treshold && maxi > max_treshold
        if sum(abs(conv150(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv150(indx-treshold:indx)))/treshold >= max_treshold/max_division
            fprintf("Blauw Omgevallen")
            write(t, uint8([begin_byte, 5, 1, end_byte]))
            %count_blauw = count_blauw + 1
            count_up = true;
        end
    end
    [maxi, indx] = max(abs(conv180));
    if maxi >= big_spike_treshold
        fprintf("Rood Omgevallen")
        write(t, uint8([begin_byte, 5, 2, end_byte]))
        %count_rood = count_rood + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv180) - treshold && maxi > max_treshold
        if sum(abs(conv180(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv180(indx-treshold:indx)))/treshold >= max_treshold/max_division
            fprintf("Rood Omgevallen")
            write(t, uint8([begin_byte, 5, 2, end_byte]))
            %count_rood = count_rood + 1
            count_up = true;
        end
    end
    [maxi, indx] = max(abs(conv1000));
    if maxi >= big_spike_treshold
        fprintf("Groen Omgevallen")
        %write(t, uint8([begin_byte, 5, 1, end_byte]))
        %count_groen = count_groen + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv1000) - treshold && maxi > max_treshold
        if sum(abs(conv1000(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv1000(indx-treshold:indx)))/treshold >= max_treshold/max_division
            fprintf("Groen Omgevallen")
            %count_groen = count_groen + 1
            count_up = true;
        end
    end

    figure(1);clf;
    hold on;
    plot(conv150, "-b");
    plot(conv180, '-r');
    plot(conv120, "-p");
    plot(conv1000, "-g");
    xlabel('sample number');
    ylabel('correlation (up to 1)')
    hold off
    if count_up
        stop(recObj);
        pause(2);
        record(recObj);
        pause(0.2);
    end
end

stop(recObj);
disp("End of recording.")



