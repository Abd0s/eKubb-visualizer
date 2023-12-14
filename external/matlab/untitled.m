t = tcpclient('localhost', 51001);

begin_byte = 43
end_byte = 45

% Handshake request
write(t, uint8([begin_byte, 1, end_byte]))
% Handshake confirm response
acknowledge_message = read(t, 3)
if acknowledge_message == uint8([43, 2, 45])
   fprintf("Handshake completed")
else
   fprintf("Handshake failedL %d", acknowledge_message)
end

% Test log
write(t, uint8([begin_byte, 4, 2, end_byte]))

fs = 192000;
recObj = audiorecorder(fs, 16, 1);

if fs == 192000
    % hier worden alle vooraf opgenomen geluiden 'opgeroepen' en in een
    % variabele gezet, dat standaardiseren is handig zoda de amplitudes op
    % basis van relatief volume en niet absoluut volume geplot worden
    % anders gaan sommige signalen meer correleren puur omdat ze net iets 
    % luider waren tijdens het opnemen
    % om da fatsoenlijk te doen moet ge ook de lengte mee in rekening nemen maar hier waren
    % ze allemaal al wel van gelijke lengte dus dan boeit da ni meer ma toch voor zekerheid gedaan

    f_name = 'sigs/or_sig470_2.dat';
    sig470 = csvread(f_name);
    sig470 = sig470/(std(sig470)*length(sig470));
    sig470 = xcorr(sig470(1:5000), sig470(5001:10000), 'normalized');
    sig470 = sig470(end-round(length(sig470)/2):end);
    sig470 = sig470/(std(sig470)*length(sig470));

    f_name = 'sigs/or_sig330_2.dat';
    sig330 = csvread(f_name);
    sig330 = sig330/(std(sig330)*length(sig330));
    sig330 = xcorr(sig330(1:5000), sig330(5001:10000), 'normalized');
    sig330 = sig330(end-round(length(sig330)/2):end);
    sig330 = sig330/(std(sig330)*length(sig330));    

    f_name = 'sigs/or_sig560_2.dat';
    sig560 = csvread(f_name);
    sig560 = sig560/(std(sig560)*length(sig560));
    sig560 = xcorr(sig560(1:5000), sig560(5001:10000), 'normalized');
    sig560 = sig560(end-round(length(sig560)/2):end);
    sig560 = sig560/(std(sig560)*length(sig560));

    f_name = 'sigs/sig390_2.dat';
    sig390 = csvread(f_name);
    sig390 = sig390/(std(sig390)*length(sig390));
    sig390 = xcorr(sig390(1:5000), sig390(5001:10000), 'normalized');
    sig390 = sig390(end-round(length(sig390)/2):end);
    sig390 = sig390/(std(sig390)*length(sig390));

end

omgevallen330 = 0;
omgevallen560 = 0;
omgevallen390 = 0;
omgevallen470 = 0;

disp("Begin speaking.")
record(recObj);
% die pauze is nodig omdat die anders zeurt dat de recorder leeg is
pause(2);
count_up = false;
% count_geel < 5 is niet belangrijk, had evengoed true kunnen staan
while true

    % het inkomend audiosignaal op het moment zelf
    doubleArray = cast(getaudiodata(recObj, 'int16'), "double");
    
    % die doubleArray kan moeilijk oneindig lang worden dus enkel de meest
    % recente samples behouden
    if length(doubleArray) > 300000
        doubleArray = doubleArray(end-300000:end);
        % de samples die weggegooid worden houden we nog 1 cyclus doorheen
        % de while loop bij zodat we daarmee de gemiddelde correlatie
        % kunnen berekenen voor elke blok
        pastArray = doubleArray(1:length(doubleArray)-30000);
    end
    
    % normaliseren van de data, zorgt ervoor dat enorm luide geluiden
    % 'zachter' worden gemaakt zodat het volume van het signaal minder
    % effect heeft op de correlatie wat goed is want de speakers zijn niet
    % luid
    k = conv(doubleArray.^2, ones(1000,1)/1000);
    k2 = conv(pastArray.^2, ones(1000, 1)/1000);
    amps = k(500:(end-500)).^0.5;
    amps2 = k2(500:(end-500)).^0.5;
    norm_data = doubleArray./amps;
    past_data = pastArray./amps2;

    %-------------------------------------------------------------------------

    conv330_1 = xcorr(norm_data, sig330);
    conv330_1 = conv330_1(round(length(conv330_1)/2):end);

    conv330 = xcorr(conv330_1(1:end-10000), conv330_1(length(conv330_1)-10000:end));
    conv330 = conv330(round(length(conv330)/2):end);
    average_conv330 = sum(abs(conv330(1:100000)))/100000;
    if max(conv330(1:100000)) < 2.8*average_conv330
        average_conv330 = average_conv330 / 5;
    end
    last_average_conv330 = sum(abs(conv330(end-100000:end)))/100000;
    corr330 = last_average_conv330/average_conv330;

    %-------------------------------------------------------------------------

    conv560_1 = xcorr(norm_data, sig560);
    conv560_1 = conv560_1(round(length(conv560_1)/2):end);

    conv560 = xcorr(conv560_1(1:end-10000), conv560_1(length(conv560_1)-10000:end));
    conv560 = conv560(round(length(conv560)/2):end);
    average_conv560 = sum(abs(conv560(1:100000)))/100000;
    if max(conv560(1:100000)) < 2.8*average_conv560
        average_conv560 = average_conv560 / 5;
    end
    last_average_conv560 = sum(abs(conv560(end-100000:end)))/100000;
    corr560 = last_average_conv560/average_conv560;

    %-------------------------------------------------------------------------

    conv390_1 = xcorr(norm_data, sig390);
    conv390_1 = conv390_1(round(length(conv390_1)/2):end);

    conv390 = xcorr(conv390_1(1:end-10000), conv390_1(length(conv390_1)-10000:end));
    conv390 = conv390(round(length(conv390)/2):end);
    average_conv390 = sum(abs(conv390(1:100000)))/100000;
    if max(conv390(1:100000)) < 2.8*average_conv390
        average_conv390 = average_conv390 / 5;
    end
    last_average_conv390 = sum(abs(conv390(end-100000:end)))/100000;
    corr390 = last_average_conv390/average_conv390;

    %-------------------------------------------------------------------------

    conv470_1 = xcorr(norm_data, sig470);
    conv470_1 = conv470_1(round(length(conv470_1)/2):end);

    conv470 = xcorr(conv470_1(1:end-10000), conv470_1(length(conv470_1)-10000:end));
    conv470 = conv470(round(length(conv470)/2):end);
    average_conv470 = sum(abs(conv470(1:100000)))/100000;
    if max(conv470(1:100000)) < 2.8*average_conv470
        average_conv470 = average_conv470 / 5;
    end
    last_average_conv470 = sum(abs(conv470(end-100000:end)))/100000;
    corr470 = last_average_conv470/average_conv470;

    %-------------------------------------------------------------------------

    if corr330 > 20 || max(abs(round(conv330))) > 40
        if corr330 > corr560 || max(abs(round(conv330))) > max(abs(round(conv560)))
            if corr330 > corr390 || max(abs(round(conv330))) > max(abs(round(conv390)))
                if corr330 > corr470 || max(abs(round(conv330))) > max(abs(round(conv470)))
                    omgevallen330 = omgevallen330 + 1
                    count_up = true;
                end
            end
        end
    elseif corr560 > 20 || max(abs(round(conv560))) > 40
        if corr560 > corr390 || max(abs(round(conv560))) > max(abs(round(conv390)))
            if corr560 > corr470 || max(abs(round(conv560))) > max(abs(round(conv470)))
                omgevallen560 = omgevallen560 + 1
                count_up = true;
            end
        end
    elseif corr390 > 20 || max(abs(round(conv390))) > 40
        if corr390 > corr470 || max(abs(round(conv390))) > max(abs(round(conv470)))
            omgevallen390 = omgevallen390 + 1
            write(t, uint8([begin_byte, 5, 1, end_byte]))
            count_up = true;
        end
    elseif corr470 > 20 || max(abs(round(conv470))) > 40
        omgevallen470 = omgevallen470 + 1
        count_up = true;
    end
 

    % dit stuk is grote chaos omdat ik meerdere manieren van detecteren aan
    % het uittesten ben en ze staan een beetje rommelig door elkaar maar
    % dat komt nog wel in orde
    % negeer dit hele gedeelte maar gewoon tijdelijk

    % -----------------------------------------------
    %if maxi >= big_spike_treshold
    %    count_rood = count_rood + 1
        %count_up = true;
    %elseif indx > treshold && indx < length(conv150) - treshold && maxi > max_treshold
    %    for i = 1:length(conv150)
    %        if abs(conv150(i)) >= max_treshold
    %            maxis150 = maxis150 + 1;
    %        end
    %    end
    %    if maxis560 >= treshold/5
    %        count_rood = count_rood + 1
    %        %count_up = true;
    %    end
    %    if count_up == false && cycle_count > 20
    %        if sum(abs(conv150(indx:indx+treshold)))/treshold >= 5*average150 || sum(abs(conv560(indx-treshold:indx)))/treshold >= 5*average150
    %            count_rood = count_rood + 1
    %            %count_up = true;
    %        end
    %    end
    %end
    % -------------------------------------------------------------------------------
    
    % de correlaties worden hier geplot
    %figure(1);clf;plot(conv330);
    %figure(2);clf;plot(conv390);
    %figure(3);clf;plot(conv470);
    %figure(4);clf;plot(conv560);

    if count_up
        stop(recObj);
        pause(0.2);
        record(recObj);
        pause(2);
        count_up = false;
    end
end
% gefeliciteerd je hebt het einde van het document gehaald
stop(recObj);
disp("End of recording.")



