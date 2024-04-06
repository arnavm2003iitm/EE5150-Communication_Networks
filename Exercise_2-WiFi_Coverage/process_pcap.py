import sys 
from scapy.all import *
import pandas as pd
import csv
import os
import math

def extract_info(pkt):

    try:

        ssid = pkt[Dot11Elt].info.decode() 
        rssi = pkt.dBm_AntSignal 
        # channel = pkt[Dot11].channel 
        # channel_flags = str(pkt.ChannelFlags)

        # if channel_flags.__contains__('2GHz'):
        #     band = '2.5GHz'
        # elif channel_flags.__contains__('5GHz'): 
        #     band = '5GHz'    

        # info = [ssid, rssi, channel, band]
        info = [ssid, rssi]

    except:
        info = None


    return info

def parse_pcap(file_path, search_ssid):
    pkt_lst = rdpcap(file_path)

    ssid_lst = []
    rssi_lst = []
    # channel_lst = []
    # band_lst = []

    for pkt in pkt_lst:
        info = extract_info(pkt)    

        if info is not None:
            ssid_lst.append(info[0])
            rssi_lst.append(info[1]) 
            # channel_lst.append(info[2])
            # band_lst.append(info[3])        
            

    # pcap_data = [ssid_lst, rssi_lst, channel_lst, band_lst]
    pcap_data = [ssid_lst, rssi_lst]    

    #
    # for pcap_data
    # in order - ssid, rssi, channel, band
    # index vals - 0     1      2       3     
    #

    #
    # for unique_info_lst
    # in order - count, ssid, rssi, channel, band
    # index vals - 0     1      2       3       4  
    #

    # unique_info_lst = [[], [], [], [], [], []]
    unique_info_lst = [[], [], []]

    for i in range(0, len(pcap_data[0])):

        if(pcap_data[0][i] not in unique_info_lst[1]):
            unique_info_lst[0].append(1)
            unique_info_lst[1].append(pcap_data[0][i])
            unique_info_lst[2].append(pcap_data[1][i])
            # unique_info_lst[3].append(pcap_data[2][i])
            # unique_info_lst[4].append(pcap_data[3][i])
           

        else:
            element_idx = unique_info_lst[1].index(pcap_data[0][i])

            unique_info_lst[0][element_idx] = unique_info_lst[0][element_idx] + 1
            count = unique_info_lst[0][element_idx]

            prev_rssi =  unique_info_lst[2][element_idx]
            prev_rssi_w = 10**(prev_rssi/10)    

            new_rssi = pcap_data[1][i]
            new_rssi_w = 10**(new_rssi/10)

            updated_rssi_w = (new_rssi_w + prev_rssi_w*(count - 1))/count
            updated_rssi = 10*math.log(updated_rssi_w, 10)

            unique_info_lst[2][element_idx] = updated_rssi

    print(unique_info_lst)

    # search for the required ssid in the list and extract required parameters

    ssid_idx = unique_info_lst[1].index(search_ssid)
    search_count = unique_info_lst[0][ssid_idx]
    search_rssi = unique_info_lst[2][ssid_idx]

    return [search_count, search_rssi]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <pcap_file_directory> <search_ssid>")
        sys.exit(1)

    dir_path = sys.argv[1]
    search_ssid = sys.argv[2]

    count = []
    rssi = []
    dist = []
    num_walls = []

    for file in os.listdir(dir_path):

        file_count, file_rssi = parse_pcap(dir_path + '/' + file, search_ssid)

        file_dist = float(file[:file.index('m')])
        file_num_walls = int(file[file.index('_')+1: file.index('w')])

        count.append(file_count)
        rssi.append(file_rssi)
        dist.append(file_dist)
        num_walls.append(file_num_walls)

    # print(count)
    # print(rssi)
    # print(dist)
    # print(num_walls)
        
    if('2.4GHz' in dir_path):
        band = '2.4GHz'
    else:
        band = '5GHz'
    
    directory_data_lst = [count, rssi, dist, num_walls]
    directory_data = list(zip(*directory_data_lst))
    print(pd.DataFrame(directory_data).to_string())

    with open('scan_{}_{}.csv'.format(band, search_ssid), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(directory_data)
        