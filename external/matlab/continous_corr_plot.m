fs = 192000;
recObj = audiorecorder(fs, 16, 1);

if fs == 44100
    % dit wordt niet meer gebruikt, waren opnames van enkele signalen bij
    % een tragere bemonsteringssnelheid
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig120.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig150.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig180.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));
    
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig220.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));
end

if fs == 192000
    % hier worden alle vooraf opgenomen geluiden 'opgeroepen' en in een
    % variabele gezet, dat standaardiseren is handig zoda de amplitudes op
    % basis van relatief volume en niet absoluut volume geplot worden
    % anders gaan sommige signalen meer correleren puur omdat ze net iets 
    % luider waren tijdens het opnemen
    % om da fatsoenlijk te doen moet ge ook de lengte mee in rekening nemen maar hier waren
    % ze allemaal al wel van gelijke lengte dus dan boeit da ni meer ma toch voor zekerheid gedaan
    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig120_2.dat';
    sig120 = csvread(f_name);
    sig120 = sig120/(std(sig120)*length(sig120));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig150_2.dat';
    sig150 = csvread(f_name);
    sig150 = sig150/(std(sig150)*length(sig150));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig180_2.dat';
    sig180 = csvread(f_name);
    sig180 = sig180/(std(sig180)*length(sig180));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/sig220_2.dat';
    sig220 = csvread(f_name);
    sig220 = sig220/(std(sig220)*length(sig220));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/2sig390_2.dat';
    sig390 = csvread(f_name);
    sig390 = sig390/(std(sig390)*length(sig390));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/or_sig220_2.dat';
    or_sig220 = csvread(f_name);
    or_sig220 = or_sig220/(std(or_sig220)*length(or_sig220));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/or_sig1200_2.dat';
    sig1200 = csvread(f_name);
    sig1200 = sig1200/(std(sig1200)*length(sig1200));

    f_name = '/Users/brent/Documenten/KU Leuven/academiejaar 2023-2024/semester 1/P&O3/sigs/or_sig560_2.dat';
    or_sig560 = csvread(f_name);
    or_sig560 = or_sig560/(std(or_sig560)*length(or_sig560));

end

% hoe vaak een bepaalde blok is omgevallen (elke kleur is een andere blok)
count_geel = 0;
count_blauw = 0;
count_rood = 0;
count_groen = 0;
% cycle_count houdt bij hoe vaak er doorheen de while loop gecycled is
% geweest want dat is nodig voor de gemiddelde correlatie waardes te kunnen
% berekenen verderop in het document;
cycle_count = 0;
% hoeveel samples er in de vorige opname zaten maar dat moet hier even op 1
% worden gezet
pastArray = 1;
% gemiddelde correlatie
average560 = 0;
average390 = 0;
omgevallen = 0;

disp("Begin speaking.")
record(recObj);
% die pauze is nodig omdat die anders zeurt dat de recorder leeg is
pause(2);
% count_geel < 5 is niet belangrijk, had evengoed true kunnen staan
while count_geel < 5
    cycle_count = cycle_count + 1;
    % het aantal pieken in de correlatie dat voor de respectievelijke
    % blokken gevonden is, daarmee wordt verderop bepaald of de blok al dan
    % niet omgevallen is
    maxis150 = 0;
    maxis390 = 0;
    maxis560 = 0;
    
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
    
    % de kruiscorrelaties worden hier uitgevoerd
    conv150 = xcorr(norm_data, sig150);
    %conv180 = xcorr(norm_data, sig180);
    %conv120 = xcorr(norm_data, sig120);
    conv390 = xcorr(norm_data, sig390);
    conv1200 = xcorr(norm_data, sig1200);
    conv560 = xcorr(norm_data, or_sig560);
    %conv220 = xcorr(norm_data, or_sig220);

    past_conv150 = xcorr(past_data, sig150);
    %past_conv180 = xcorr(past_data, sig180);
    %past_conv120 = xcorr(past_data, sig120);
    past_conv390 = xcorr(past_data, sig390);
    past_conv1200 = xcorr(past_data, sig1200);
    past_conv560 = xcorr(past_data, or_sig560);
    %past_conv220 = xcorr(past_data, or_sig220);

    % bij kruiscorrelaties worden u signalen twee keer zo lang dus da wordt
    % hier gefixt
    conv150 = conv150(round(length(conv150)/2):end);
    %conv180 = conv180(round(length(conv180)/2):end);
    %conv120 = conv120(round(length(conv120)/2):end);
    conv390 = conv390(round(length(conv390)/2):end);
    conv1200 = conv1200(round(length(conv1200)/2):end);
    conv560 = conv560(round(length(conv560)/2):end);
    
    % ik heb gemerkt dat in de correlatie zelf ook een patroon terug te
    % vinden is dus ik ben aan het testen of de correlatie nogmaals met
    % zichzelf correleren betere resultaten geeft ma dit is work in
    % progress en waarschijnlijk ni heel nuttig dus kan zijn da ik da
    % weghaal ma wie weet werkt het super goe
    convofconv390 = xcorr(conv390(length(conv390)-10000:end), conv390);
    convofconv390 = convofconv390(1:round(length(convofconv390)/2));

    if max(convofconv390) > 35
        omgevallen = omgevallen + 1
    end

    past_conv150 = past_conv150(round(length(past_conv150)/2):end);
    %past_conv180 = past_conv180(round(length(past_conv180)/2):end);
    %past_conv120 = past_conv120(round(length(past_conv120)/2):end);
    past_conv390 = past_conv390(round(length(past_conv390)/2):end);
    past_conv1200 = past_conv1200(round(length(past_conv1200)/2):end);
    past_conv560 = past_conv560(round(length(past_conv560)/2):end);
    
    % de gemiddelde correlatie wordt hier berekend, het nut hiervan is dat
    % als bijvoorbeeld een signaal een gemiddelde correlatie van 0.05 heeft
    % en plots is de correlatie gedurende een korte periode 3 of 10 keer zo hoog dan
    % weet je dat de blok in kwestie omgevallen is
    average560 = (average560*cycle_count*length(pastArray) + sum(abs(past_conv560))) / (cycle_count*length(pastArray)+length(pastArray));
    average390 = (average390*cycle_count*length(pastArray) + sum(abs(past_conv390))) / (cycle_count*length(pastArray)+length(pastArray));


    % dit stuk is grote chaos omdat ik meerdere manieren van detecteren aan
    % het uittesten ben en ze staan een beetje rommelig door elkaar maar
    % dat komt nog wel in orde
    % negeer dit hele gedeelte maar gewoon tijdelijk
    [maxi, indx] = max(abs(conv560));
    treshold = 30000;
    max_treshold = 0.2;
    big_spike_treshold = 0.7;
    max_division = 1.7;
    count_up = false;
    % -----------------------------------------------
    if maxi >= big_spike_treshold
        count_geel = count_geel + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv560) - treshold && maxi > max_treshold
        for i = 1:length(conv560)
            if abs(conv560(i)) >= max_treshold
                maxis560 = maxis560 + 1;
            end
        end
        if maxis560 >= treshold/5
            count_geel = count_geel + 1
            count_up = true;
        end
        if count_up == false && cycle_count > 20
            if sum(abs(conv560(indx:indx+treshold)))/treshold >= 5*average560 || sum(abs(conv560(indx-treshold:indx)))/treshold >= 5*average560
                count_geel = count_geel + 1
                count_up = true;
            end
        end
    end
    % -------------------------------------------------------------------------------
    [maxi, indx] = max(abs(conv1200));
    if maxi >= big_spike_treshold
    count_blauw = count_blauw + 1
    count_up = true;
    elseif indx > treshold && indx < length(conv1200) - treshold && maxi > max_treshold
        if sum(abs(conv1200(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv1200(indx-treshold:indx)))/treshold >= max_treshold/max_division
            count_blauw = count_blauw + 1
            count_up = true;
        end
    end
    % -------------------------------------------------------------------------------
    [maxi, indx] = max(abs(conv390));
    if maxi >= big_spike_treshold
        count_rood = count_rood + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv390) - treshold && maxi > max_treshold
        for i = 1:length(conv390)
            if abs(conv390(i)) >= max_treshold
                maxis390 = maxis390 + 1;
            end
        end
        if maxis390 >= treshold/5
            count_rood = count_rood + 2
            %count_up = true;

        end
        if count_up == false && cycle_count > 20
            if sum(abs(conv390(indx:indx+treshold)))/treshold >= 5*average390 || sum(abs(conv390(indx-treshold:indx)))/treshold >= 5*average390
                k = sum(abs(conv390(indx:indx+treshold)))/treshold
                count_rood = count_rood + 1
                %count_up = true;
            end
        end
    end
    % -------------------------------------------------------------------------------
    [maxi, indx] = max(abs(conv150));
    if maxi >= big_spike_treshold
        count_groen = count_groen + 1
        count_up = true;
    elseif indx > treshold && indx < length(conv150) - treshold && maxi > max_treshold
        for i = 1:length(conv150)
            if abs(conv150(i)) >= max_treshold
                maxis150 = maxis150 + 1;
            end
        end
        if maxis150 >= treshold/30
            count_groen = count_groen + 1
            count_up = true;
        end
        if count_up == false
            if sum(abs(conv150(indx:indx+treshold)))/treshold >= max_treshold/max_division || sum(abs(conv150(indx-treshold:indx)))/treshold >= max_treshold/max_division
                count_groen = count_groen + 1
                count_up = true;
            end
        end
    end
    
    % de correlaties worden hier geplot
    figure(1);clf;
    hold on;
    %plot(conv150, "-g");
    %plot(conv180, '-r');
    %plot(conv120, "-p");
    %plot(conv390, "-r");
    %plot(conv560, "-y");
    %plot(conv1200, "-b");
    plot(convofconv390);
    xlabel('Sample number');
    ylabel('Correlation (up to 1)')
    hold off
    % als er een blok is omgevallen dan moet de geluidsopname even stoppen
    % want vaak zal het geluidssignaal in de volgende cyclus doorheen deze
    % while loop nog altijd aanwezig zijn en dan zal matlab dus beginnen
    % zeggen dat die blok al 2 of 3 of zelfs meer keer is omgevallen
    if count_up
        stop(recObj);
        pause(2);
        record(recObj);
        pause(0.2);
    end
end
% gefeliciteerd je hebt het einde van het document gehaald
stop(recObj);
disp("End of recording.")



