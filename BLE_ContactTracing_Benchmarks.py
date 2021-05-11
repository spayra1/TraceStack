# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:00:12 2021

@author: spayr
"""

import time
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300

fortymins = 4*60*40
twentymins = 4*60*20
tenmins = 4*60*10

def stage1v1():
    # test 3 trials
    timing = []
    for trial in range(5):
        elapsed = []
    
        # test latency with different number of simultaneous contacts
        for people in range(20):
            
            # contact test set
            contacts = {signal:{person for person in range(people)} for signal in range(fortymins)}
            
            #stage 1
            flags = []
            
            starttime = time.perf_counter()
            for signal in range(twentymins,fortymins):
                for person in contacts[signal]:
                    if person in contacts[signal-twentymins]:
                        flags.append(person)
            elapsed.append((time.perf_counter() - starttime)*1000)
            print(f"stage 1, {people} people: {elapsed[-1]} milliseconds")
        
        timing.append(elapsed)
    timing = list(np.average(timing, axis=0))
            
    plt.figure()
    plt.suptitle("Stage 1 Latency vs. # of Continuous Contacts")
    plt.xlabel("Number of Individuals in Continuous Contact")
    plt.ylabel("Calculation Time (milliseconds)")
    plt.plot(range(20),timing,marker='+',mec='r',linestyle='solid',label='average of 5 trials')
    plt.legend()
    # plt.savefig("plots/binarycomparison-draft.jpg",dpi=00)

def stage1v2():
    # test 3 trials
    timing = []
    for trial in range(5):
        elapsed = []
    
        # test latency with different number of simultaneous contacts
        for people in range(20):
            
            # contact test set
            contacts = {signal:{person for person in range(people)} for signal in range(fortymins)}
            
            #stage 1
            flags = set()
            
            starttime = time.perf_counter()
            for signal in range(twentymins,fortymins):
                for person in contacts[signal]:
                    if person not in flags:
                        if person in contacts[signal-twentymins]:
                            flags.add(person)
            elapsed.append((time.perf_counter() - starttime)*1000)
            print(f"stage 1, {people} people: {elapsed[-1]} milliseconds")
        
        timing.append(elapsed)
    timing = list(np.average(timing, axis=0))
            
    plt.figure()
    plt.suptitle("Contact-Tracing Latency vs. # of Continuous Contacts")
    plt.xlabel("Number of Individuals in Continuous Contact")
    plt.ylabel("Calculation Time (milliseconds)")
    plt.plot(range(20),timing,marker='+',mec='r',linestyle='solid',label='average of 5 trials')
    plt.legend()
    # plt.savefig("plots/binarycomparison-draft.jpg",dpi=00)

def allstages():
    # test 3 trials
    timing = []
    for trial in range(5):
        elapsed = []
    
        # test latency with different number of simultaneous contacts
        for people in range(0,105,5):
            
            # initialize
            contacts = {timestamp:{person for person in range(people)} for timestamp in range(fortymins)}
            period = 1 # timestamp delta for BLE
            flags = dict() # contact:coverage
            starttime = time.perf_counter()
            threshold = 0.9
            
            #stage 1 - screen for contact 20 minutes apart
            for timestamp in range(twentymins,fortymins):
                for person in contacts[timestamp]:
                    if person not in flags:
                        if person in contacts[timestamp-twentymins]:
                            flags[person] = 0
            
            #stage 2 - discard contacts with gaps >10 minutes
            removals = []
            timestamps = {person:{"signals":[], "blanks":[]} for person in flags}
            for person in timestamps:
                timestamps[person]["signals"] = [timestamp for timestamp in contacts if person in contacts[timestamp]]
                
                for index in range(len(timestamps[person]["signals"])-1):
                    gap = timestamps[person]["signals"][index]-timestamps[person]["signals"][index-1]
                    
                    if gap>tenmins:
                        removals.append(person)
                        break;
                    elif gap>period:
                        timestamps[person]["blanks"].append(gap//period)
            
                if person in removals:
                    flags.remove(person)
                
            
            #stage 3 - evaluate signal coverage for each contact
            removals = []
            for person in flags:
                flags[person]=sum(timestamps[person]["blanks"])/len(timestamps[person]["signals"])
            
            
            #stage 4 - flag contacts with coverage>threshold
            flaggedcontacts = [person for person in flags if flags[person]>threshold]
        
            # done all stages, calculate time elapsed
            elapsed.append((time.perf_counter() - starttime)*1000)
            print(f"all stages, {people} people: {elapsed[-1]} milliseconds")
        timing.append(elapsed)
    timing = list(np.average(timing, axis=0))
    
    plt.figure()
    plt.suptitle("Contact-Tracing Latency vs. # of Continuous Contacts")
    plt.xlabel("Number of Individuals in Continuous Contact")
    plt.ylabel("Calculation Time (milliseconds)")
    plt.plot(range(0,105,5),timing,marker='+',mec='r',linestyle='solid',label='average of 5 trials')
    plt.legend()
    # plt.savefig("plots/binarycomparison-draft.jpg",dpi=00)