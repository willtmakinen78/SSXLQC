import sys
sys.path.append("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC")

import os
import re
import time
import shutil
import tkinter as tk
import multiprocessing
from configparser import ConfigParser
from ssxlqc.numtest import is_number
from ssxlqc.sum.rfsum import RFSummary
from ssxlqc.sum.tracksum import TrackSummary
from ssxlqc.sum.conveyersum import ConveyerSummary
import ssxlqc.autogui.rfauto as rfauto
import ssxlqc.autogui.serialauto as serialauto

##### MODIFY THESE TO POINT TO LOG FILE LOCATIONS #####
rf_loc = "C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\rf"
track_loc = "C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\track"
conveyer_loc = "C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\conveyer"

perfectpick_logs_loc = "C:\\OPEX\\PerfectPick\\Logs"
##### END MODIFICATIONS #####

# assign recording/analysis objects
rf_sum = RFSummary(rf_loc)
track_sum = TrackSummary(track_loc)
conveyer_sum = ConveyerSummary(conveyer_loc)

# references to multiprocessing objects
rf_recorder = None
track_recorder = None
conveyer_recorder = None

# folder-monitoring methods to be executed as separate processes
def run_rf():
    global rf_sum
    rf_sum.summarize()
def run_track():
    track_sum.summarize()
def run_conveyer():
    conveyer_sum.summarize()

# methods to trigger the autogui sequences, also to be run as separate processes
def record_rf(bot_num, recording_length, num_trials):
    print("recording rf")

    # ensure that the bot # string is a valid number, then convert
    num = __format_bot_num(bot_num)

    # verify the correctness of the run length
    sleep_time = 10
    if __verify_num_input(recording_length, "Run Time"):
        sleep_time = float(recording_length)

    # verify the correctness of the trial numbers
    times_to_run = 1
    if __verify_num_input(num_trials, "# Trials"):
        times_to_run = int(float(num_trials))

    print("recording for {} minutes {} times".format(sleep_time, times_to_run))

    # run the requested # of times
    for i in range(times_to_run):
        print("run {}/{}".format(i + 1, times_to_run))

        # start the test
        rfauto.collect(num, rf_loc)

        print("recording for {} minutes".format(sleep_time))

        # delay accordingly
        time.sleep(sleep_time * 60)

        # end the test
        print("ending rf recording")
        rfauto.stop()

        # copy the log file from the default save loc to the package's install loc
        # files_by_date = __all_files_under(perfectpick_logs_loc).sort(key=os.path.getmtime)
        files_by_date = sorted(__all_files_under(perfectpick_logs_loc), key=os.path.getmtime)

        # the most recent file is always a .log (not .csv) file, so get the 2nd-most recent
        latest_file = files_by_date[-2]
        # latest_file = max(__all_files_under(perfectpick_logs_loc), key=os.path.getmtime)

        # only copy the most recent file that matches the file format
        match = re.search(r'\d*_\d\d\d\d\d\d\d\d_\d\d\d\d\d\d\.csv', latest_file)
    
        # copy the log file and handle exceptions
        if match:
            try:
                # figure out which part of the path matches
                matching_text = match.group()
                match_length = len(matching_text)
                diff = abs(match_length - 26)
                
                # add the number of zero sneede to the bot number
                for i in range(diff): matching_text = "0" + matching_text

                target = rf_loc + "\\SSXL" + matching_text

                print("copying: " + latest_file + " from default location to: " + target)
                # actual copy command
                shutil.copyfile(latest_file, target)

            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
        else: print("most recently-created file: " + latest_file + " not of correct format")


def record_track(bot_num, num_trials):
    print("recording track")

    # ensure that the bot # string is a valid number, then convert
    num = __format_bot_num(bot_num)

    # verify the correctness of the trial numbers
    times_to_run = 1
    if __verify_num_input(num_trials, "# Trials"):
        times_to_run = int(float(num_trials))

    print("recording {} times".format(times_to_run))

    # run the requested # of times
    for i in range(times_to_run):
        print("run {}/{}".format(i + 1, times_to_run))

        # start the test
        serialauto.collect(num, "track", track_loc)

def record_conveyer(bot_num, num_trials):
    print("recording conveyer")

    # ensure that the bot # string is a valid number, then convert
    num = __format_bot_num(bot_num)

    # verify the correctness of the trial numbers
    times_to_run = 1
    if __verify_num_input(num_trials, "# Trials"):
        times_to_run = int(float(num_trials))

    print("recording {} times".format(times_to_run))

    # run the requested # of times
    for i in range(times_to_run):
        print("run {}/{}".format(i + 1, times_to_run))

        # start the test
        serialauto.collect(num, "conveyer", conveyer_loc)
    
# the methods that trigger/call upon the processes that use the above autogui methods
# (NOT run in separate processes)
def process_rf(bot_num, recording_length, num_trials):
    try:
        global rf_recorder 
        rf_recorder = multiprocessing.Process(
            target=record_rf, args=(bot_num, recording_length, num_trials,))
        rf_recorder.start()
        rf_recorder = rf_recorder
    except Exception as e: 
        rf_recorder.terminate()
        rf_recorder.join()
        print("conveyer process exiting due to exception")
        print(e)

def process_track(bot_num, num_trials):
    try:
        global track_recorder 
        track_recorder = multiprocessing.Process(
            target=record_track, args=(bot_num, num_trials,))
        track_recorder.start()
    except Exception as e: 
        track_recorder.terminate()
        track_recorder.join()
        print("conveyer process exiting due to exception")
        print(e)

def process_conveyer(bot_num, num_trials):
    try:
        global conveyer_recorder
        conveyer_recorder = multiprocessing.Process(
            target=record_conveyer, args=(bot_num, num_trials,))
        conveyer_recorder.start()
    except Exception as e: 
        conveyer_recorder.terminate()
        conveyer_recorder.join()
        print("conveyer process exiting due to exception")
        print(e)

# calls upon the above three depending on the settings set
# when start button is pushed
def process_all(bot_num, recording_length, num_trials, test_type):
    if test_type == "rf":
        process_rf(bot_num, recording_length, num_trials)
    if test_type == "track":
        process_track(bot_num, num_trials)
    if test_type == "conveyer":
        process_conveyer(bot_num, num_trials)

# updates the points to use when the button is pressed
def update_num_points(points_to_calculate, points_to_show):
    # validate point counts
    calc_count = 50
    if __verify_num_input(points_to_calculate, "Calc Num"):
        calc_count = int(float(points_to_calculate))

    show_count = 15
    if __verify_num_input(points_to_show, "Show Num"):
        show_count = int(float(points_to_show))

    # make new config file
    writer = ConfigParser()
    writer['points_to_use'] = {'calc': str(calc_count),
                               'show': str(show_count)}

    # get the path of the config file
    script_path = os.path.abspath(__file__) 
    path_list = script_path.split(os.sep)
    script_directory = path_list[0:len(path_list)-1]
    rel_path = "chart/chartconfig.ini"
    path = "/".join(script_directory) + "/" + rel_path

    # write the new config contents to the file
    with open(path, 'w') as configfile:
        writer.write(configfile)

    print("points to use updated")


# the main method that does everything, called upon by __main__.py
def run():

    # start all three folder monitors
    try:
        rf = multiprocessing.Process(target=run_rf)
        rf.start()
    except Exception as e: 
        rf.terminate()
        rf.join()
        print("rf process exiting due to exception:")
        print(e)
    try: 
        track = multiprocessing.Process(target=run_track)
        track.start()
    except Exception as e: 
        track.terminate()
        track.join()
        print("track process exiting due to exception")
        print(e)
    try:
        conveyer = multiprocessing.Process(target=run_conveyer)
        conveyer.start()
    except Exception as e: 
        conveyer.terminate()
        conveyer.join()
        print("conveyer process exiting due to exception")
        print(e)

    # create the gui window to start tests. folder monitoring will still
    # be active regardless of what is done for files uploaded manually
    print("\nexit out of gui window to quit\n")

    m = tk.Tk()
    m.title("SSXLQC")

    # text entry boxes
    num_entry = tk.Entry(m, width=12)
    length_entry = tk.Entry(m, width=12)
    trial_entry = tk.Entry(m, width=12)
    calc_entry = tk.Entry(m, width=12)
    show_entry = tk.Entry(m, width=12)

    # type selector
    lb = tk.Listbox(width=12, height=3)
    lb.insert(1, 'rf')
    lb.insert(2, 'track')
    lb.insert(3, 'conveyer')


    # start button  
    start_button = tk.Button(m, text='Start', width=12, command=lambda:
                            process_all(num_entry.get(), length_entry.get(), 
                            trial_entry.get(), lb.get(lb.curselection())))
                                    
    # points to use update button
    num_points_updater = tk.Button(m, text='Update Point #s', width=12, 
                            command=lambda: update_num_points(calc_entry.get(), show_entry.get()))

    # scrub points button
    scrub_trial_button = tk.Button(m, text='Scrub Last Trial', width=12, 
                            command=lambda: scrub_last_trial(lb.get(lb.curselection())))

    # formatting
    tk.Label(m, text='iBot #: ').grid(row=0)
    tk.Label(m, text='Run Time: ').grid(row=1)
    tk.Label(m, text='# Trials: ').grid(row=2)
    tk.Label(m, text='Calc #: ').grid(row=3)
    tk.Label(m, text='Show #: ').grid(row=4)
    num_entry.grid(row=0, column=1)
    length_entry.grid(row=1, column=1)
    trial_entry.grid(row=2, column=1)
    calc_entry.grid(row=3, column=1)
    show_entry.grid(row=4, column=1)
    
    num_points_updater.grid(row=5, column=1)
    lb.grid(row=5)
    start_button.grid(row=6)
    scrub_trial_button.grid(row = 6, column=1)
    
    m.mainloop()

    # closing out of the window (exiting mainloop()) will terminate everything

    print("\nterminating all processes")
    rf.terminate()
    rf.join()
    track.terminate()
    track.join()
    conveyer.terminate()
    conveyer.join()

    # only terminate the recording processes if they've been assigned/started
    if rf_recorder != None:
        rf_recorder.terminate()
        rf_recorder.join()
    if track_recorder != None:
        track_recorder.terminate()
        track_recorder.join()
    if conveyer_recorder != None:
        conveyer_recorder.terminate()
        conveyer_recorder.join()
    print("processes terminated")

# scrub the last trial from a summary file
def scrub_last_trial(test_type):

    # get the right file location
    sumfile = ""
    if test_type == "rf":
        sumfile = rf_loc + "\\summary\\SSXL_RF_Summary.csv"
    elif test_type == "track":
        sumfile = track_loc + "\\summary\\SSXL_Track_Summary.csv"
    elif test_type == "conveyer":
        sumfile = track_loc + "\\summary\\SSXL_Conveyer_Summary.csv"

    print("scrubbing last line")
    # open the file and read data in
    lines = []
    try:
        with open(sumfile, "r") as out:

            # scrub the last line
            lines = out.readlines()
            lines = lines[:-1]

    except PermissionError as e:
        print("summary file: %s is currently open/under use. Close and re-upload log file" % sumfile)
        print(e)

    # re-write data and summarize
    try:
        with open(sumfile, "w+") as out:

            # write everything else back to the file
            for line in lines:
                out.write(line)
    except PermissionError as e:
        print("summary file: %s is currently open/under use. Close and re-upload log file" % sumfile)
        print(e)
    print("done")

# private helper method to get all the files in a directory
def __all_files_under(path):
    """Iterates through all files that are under the given path."""
    for cur_path, dirnames, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(cur_path, filename)

# private helper method to verify number inputs
def __verify_num_input(num, err_type):
    if is_number(num):
        if float(num) <= 0:
            print(err_type + " must be positive, using defaults")
            return False
        return True
    else:
        print(err_type + "  is invalid, using defaults")
        return False
    
# private helper mthod to format bot_num to have 6 digits
def __format_bot_num(bot_num):
    # ensure that the bot # string is a valid number, then convert
    if __verify_num_input(bot_num, "iBot #") == False: return

    length = len(bot_num)
    # everything good, bot_num is a 6-digit string
    if length == 6: return bot_num

    # bot_num is a number but has too many digits, use the 6
    # least significant digits
    elif length > 6: return bot_num[-6:]

    # bot_num is a number but has too few digits, use the add leading 0s
    else: 
        diff = 6 - length
        for i in range(diff): bot_num = "0" + bot_num
        return bot_num