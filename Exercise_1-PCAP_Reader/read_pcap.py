# freq - pkt.ChannelFrequency
# rssi - pkt.dBm_AntSignal
# noise strength - pkt.dBm_AntNoise
# data rate - pkt.Rate
# bssid - pkt[Dot11FCS].addr3
# band - pkt.ChannelFlags

import sys 
from scapy.all import *
import pandas as pd
import csv

def extract_info(pkt):
    if pkt.haslayer(Dot11Elt) and pkt[Dot11Elt].info:

        ssid = pkt[Dot11Elt].info.decode() #
        channel = pkt[Dot11].channel # 
        bssid = pkt[Dot11FCS].addr3 #
        rssi = pkt.dBm_AntSignal #
        noise = pkt.dBm_AntNoise #
        freq = pkt.ChannelFrequency
        channel_flags = str(pkt.ChannelFlags)

        if channel_flags.__contains__('2GHz'):
            band = '2.5GHz'
        elif channel_flags.__contains__('5GHz'): 
            band = '5GHz'    

        info = [ssid, bssid, channel, band, freq, rssi, noise]
    else:
        info = None

    return info

def process_pcap(file_path):
    pkt_lst = rdpcap(file_path)

    ssid_lst = []
    bssid_lst = []
    channel_lst = []
    band_lst = []
    freq_lst = []
    rssi_lst = []
    noise_lst = []

    for pkt in pkt_lst:
        info = extract_info(pkt)    

        if info is not None:
            ssid_lst.append(info[0])
            bssid_lst.append(info[1])
            channel_lst.append(info[2])
            band_lst.append(info[3])
            freq_lst.append(info[4])
            rssi_lst.append(info[5])
            noise_lst.append(info[6])            
            

    info_lst = [ssid_lst, bssid_lst, channel_lst, band_lst, freq_lst, rssi_lst, noise_lst]
                    
    return info_lst

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <pcap_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    pcap_data = process_pcap(file_path)
    

    #
    # for pcap_data
    # in order - ssid, bssid, channel, band, freq, rssi, noise
    # index vals - 0     1      2       3      4     5     6
    #

    #
    # for unique_info_lst
    # in order - count, ssid, bssid, channel, band, freq, rssi, noise, snr
    # index vals - 0     1      2       3       4     5     6     7     8
    #
    unique_info_lst = [[], [], [], [], [], [], [], [], []]

    for i in range(0, len(pcap_data[0])):

        if(pcap_data[0][i] not in unique_info_lst[1]):
            unique_info_lst[0].append(1)
            unique_info_lst[1].append(pcap_data[0][i])
            unique_info_lst[2].append(pcap_data[1][i])
            unique_info_lst[3].append(pcap_data[2][i])
            unique_info_lst[4].append(pcap_data[3][i])
            unique_info_lst[5].append(pcap_data[4][i])
            unique_info_lst[6].append(pcap_data[5][i])
            unique_info_lst[7].append(pcap_data[6][i])
            unique_info_lst[8].append(pcap_data[5][i] - pcap_data[6][i])
           

        else:
            element_idx = unique_info_lst[1].index(pcap_data[0][i])
            unique_info_lst[0][element_idx] = unique_info_lst[0][element_idx] + 1
            count = unique_info_lst[0][element_idx]
            prev_rssi =  unique_info_lst[6][element_idx]
            new_rssi = (prev_rssi*(count-1)+pcap_data[5][i])/count
            unique_info_lst[6][element_idx] = new_rssi

            prev_noise =  unique_info_lst[7][element_idx]
            new_noise = (prev_noise*(count-1)+pcap_data[6][i])/count
            unique_info_lst[7][element_idx] = new_noise

            unique_info_lst[8][element_idx] = new_rssi - new_noise

    unique_info_lst = list(zip(*unique_info_lst[1:]))
    
    print(pd.DataFrame(unique_info_lst).to_string())
    
    with open('scan.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(unique_info_lst)
    