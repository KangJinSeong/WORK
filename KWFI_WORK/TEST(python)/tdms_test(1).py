'''
Date: 2021.10.18
Title: TDMS Data Write & Read
By: Kang Jin Seong
'''

from nptdms import TdmsWriter, ChannelObject, TdmsFile
import numpy

with TdmsWriter("path_to_file.tdms") as tdms_writer:
    data_array = numpy.linspace(0, 1, 10)
    channel = ChannelObject('group name', 'channel name', data_array)
    tdms_writer.write_segment([channel])
    

with TdmsFile.open("path_to_file.tdms") as tdms_file:
    group = tdms_file['group name']
    channel = group['channel name']
    channel_data = channel[:]   

print(channel_data)

