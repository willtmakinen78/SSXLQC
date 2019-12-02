import time
import re
import statistics as stats
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ssxlqc.numtest import is_number
from ssxlqc.unpack.trackdata import TrackData
from ssxlqc.chart.chart import plot


# class to create instances of Watcher Handler that in turn update 
# the running summary
class TrackSummary(object):
    from_location = ""

    # initialize
    def __init__(self, from_location):
        self.from_location = from_location

    # analyzes the data, appends the summary file
    def summarize(self):
        w = Watcher(self.from_location)
        w.run()

    # get date, etc from the filename format: (iBot|SSXL)_yyyymmdd_hhmmss
    # order: full filename, bot number, year, month, day, hour, min, sec
    def parse_filename(self, filename):
        output = []

        # fulle filname
        output.append(filename[-30:-4])
        # bot number
        output.append(filename[-26:-20])
        # year
        output.append(filename[-19:-15])
        # month
        output.append(filename[-15:-13])
        # day
        output.append(filename[-13:-11])
        # hour
        output.append(filename[-10:-8])
        # minute
        output.append(filename[-8:-6])
        # second
        output.append(filename[-6:-4])

        return output


# calls upon the _TrackHandler class, initiating directory observation
class Watcher:

    observer = None
    DIRECTORY_TO_WATCH = ""

    # pass thru the directory to monitor
    def __init__(self, from_location):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = from_location

    # begin monitoring
    def run(self):
        event_handler = TrackHandler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            print("track folder monitor starting")
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("track watcher exiting")

        self.observer.join()

# catches any files uploaded and initites analysis
class TrackHandler(FileSystemEventHandler):
    
    def on_any_event(self, event):
        if event.is_directory:
            return None

        # called when a file is first created/moved to tge folder
        elif event.event_type == 'created':

            from_location = event.src_path

            # don't analyze summary or any other types of files
            match = re.search(r'.*(i(B|b)ot|SSXL|ssxl)\d\d\d\d\d\d_\d\d\d\d\d\d\d\d_\d\d\d\d\d\d\.txt', 
                                from_location)
            if not match:
                print("%s is not of the specified file name format" % from_location) 
                return

            print("Log File: %s Copied. Uploading..." % event.src_path)

            # simple delay to allow for file to transfer fully. Detect when file is done uploading?
            time.sleep(3)
            print("Upload complete. Analyzing...")

            # open the newly-created file and begin analysis
            track_data = TrackData(from_location)

            file_info = TrackSummary.parse_filename(TrackSummary, from_location)
            info_length = len(file_info)
            track_data.unpack()
            summary = track_data.get_summary()
            track_data.write_trial_summary()

            # generate the output filename/location
            for i in range(len(from_location) - 1, 0, -1):
                if from_location[i] == "\\":
                    to_location = from_location[:i] + "\\summary\\SSXL_Track_Summary.csv"
                    break
            print("updating track summary at: " + to_location)

            # stats for each column
            # add any additional calculations here
            NUM_STATS = 3
            avgs = []
            stds = []
            avgs_stds = []

            title_line = []
            data = []

            # read in all the existing data first
            try:
                with open(to_location, "r") as out:
                    count = 0
                    for line in out:
                        line_list = line.split(",")
                        if count == 0:
                            for item in line_list:
                                title_line.append(item)
                                data.append([])
                        elif count > NUM_STATS:
                            for i in range(len(line_list)):
                                if i == 0: data[i].append(line_list[i])
                                else: 
                                    if is_number(line_list[i]): data[i].append(float(line_list[i].strip()))
                        count += 1
            except FileNotFoundError as e:
                print("summary file: %s does not exist. Create and format properly before running" % to_location)
                print(e)

            # add the most recent trial's data
            for i in range(info_length):
                data[i].append(file_info[i])
            for i in range(len(summary)):
                data[i + len(file_info)].append(summary[i])

            # do the statistics
            for i in range(len(data) - info_length):
                col = data[i + info_length]
                if i % 3 == 0 and i > 1:
                    # an avg+3*std col, find avg and std of said column
                    if len(col) > 0: avgs.append(stats.mean(col))
                    else: avgs.append(0)
                    if len(col) > 1: stds.append(stats.stdev(col))
                    else: stds.append(0)

                    if stds[-1] != 0: avgs_stds.append(avgs[-1] + (3 * stds[-1]))
                    else: avgs_stds.append(0)
                else:
                    # otherwise it's an avg or std row, leave blank
                    avgs.append("-")
                    stds.append("-")
                    avgs_stds.append("-")
                    

            # add row titles
            data[0].insert(0, "AVG")
            data[0].insert(1, "STD")
            data[0].insert(2, "AVG + 3*STD")

            # add stats to data
            for i in range(len(data) - info_length):
                col = data[i + info_length]

                col.insert(0, avgs[i])
                col.insert(1, stds[i])
                col.insert(2, avgs_stds[i])

            # fill in time slots with empties
            for col in data[1:info_length]:
                for i in range(NUM_STATS):
                    col.insert(i, "-")

            # re-write data and summarize
            try:
                with open(to_location, "w+") as out:
                    for item in title_line[:-1]:
                        out.write(item.strip() + ",")

                    # no comma after last item in title row
                    out.write(title_line[- 1].strip())
                    out.write("\n")

                    for j in range(len(data[0])):
                        for i in range(len(data) - 1):
                            out.write(str(data[i][j]) + ",")

                        # no comma after last item in data rows
                        out.write(str(data[-1][j]))
                        out.write("\n")
                print("done")
            except PermissionError as e:
                print("summary file: %s is currently open/under use. Close and re-upload log file" % to_location)
                print(e)

            # bring down the global variables
            global num_calculate
            global num_show

            plot(data, title_line, info_length + 3, 3, NUM_STATS, 
                    "save", to_location[:-31], sup_title="Track",
                     grid_size=(2, 3), title_strip=-7)
