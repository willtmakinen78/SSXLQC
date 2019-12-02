import sys
sys.path.append("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC")

import time
import multiprocessing
from ssxlqc.sum.rfsum import RFSummary
from ssxlqc.sum.tracksum import TrackSummary
from ssxlqc.sum.conveyersum import ConveyerSummary

rf_sum = RFSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\rf")
track_sum = TrackSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\track")
conveyer_sum = ConveyerSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\conveyer")

def run_rf():
    rf_sum.summarize()
def run_track():
    track_sum.summarize()
def run_conveyer():
    conveyer_sum.summarize()

if __name__ == '__main__':
    try:
        rf = multiprocessing.Process(target=run_rf)
        rf.start()
        # rf.join()
    except Exception as e: 
        rf.terminate()
        rf.join()
        print("rf process exiting due to exception:")
        print(e)
    try: 
        track = multiprocessing.Process(target=run_track)
        track.start()
        # track.join()
    except Exception as e: 
        track.terminate()
        track.join()
        print("track process exiting due to exception")
        print(e)
    try:
        conveyer = multiprocessing.Process(target=run_conveyer)
        conveyer.start()
        # conveyer.join()
    except Exception as e: 
        conveyer.terminate()
        conveyer.join()
        print("conveyer process exiting due to exception")
        print(e)

    end_state = "" 
    while end_state != "q":
        end_state = input("press q at any point to quit\n")

    print("terminating all processes")
    rf.terminate()
    rf.join()
    track.terminate()
    track.join()
    conveyer.terminate()
    conveyer.join()
    print("processes terminated")
    