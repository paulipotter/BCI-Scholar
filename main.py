from __future__ import print_function
from Calf_Counter import *
from sqltest import *
import json

import pprint

while True:
    answer = raw_input("Use default values? (y/n): ")
    if answer == "y" or answer == "Y":
        window = 60*60
        break
    elif answer == "n" or answer == "N":
        window = raw_input("Input the number desired window (1 hr is recommended): ")#60*60 # window for grouping time default = 30 secs
        break
    else:
        print("Please only input 'y' or 'n'.")

total_study_days = 25

contacts = []
# big loop through all 2.5 ish seconds -- most likely a nested loop
# when seconds = 86400 -- day++
calf_list = create_dict(total_study_days)

#imports the csv file that contains shedding data
calf_list = health_status(calf_list)

frames = 86400/window #this gives total time frams in a day based on the window chosen

start = 1462363200 #  2016-05-04 07:00:00 1462363200
end = 1464335999 #  2016-05-27 02:59:59 AM 1464335999
index = start
day = 0

while day < total_study_days: #24:
    #day = (index - start) % 86400
    groupings = 0
    print("day: ",day)
    #loop through the frames
    while groupings < frames: 
        # returns a list of pairs of contacts
        contacts = pull_data(index)

        index += window
        #increment the appropriate counts
        add_counts(contacts, day)

        groupings +=1
        
    day +=1


export_data(total_study_days)
