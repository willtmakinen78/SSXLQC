import time
import re
import statistics as stats
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ssxlqc.numtest import is_number
from ssxlqc.unpack.rfdata import RFData
from ssxlqc.chart.chart import plot


# class to create instances of Watcher Handler that in turn update 
# the running summary
class RFSummary(object):
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


# calls upon the _RFHandler class, initiating directory observation
class Watcher:

    observer = None
    DIRECTORY_TO_WATCH = ""

    # pass thru the directory to monitor
    def __init__(self, from_location):
        self.observer = Observer()
        self.DIRECTORY_TO_WATCH = from_location

    # begin monitoring
    def run(self):
        event_handler = RFHandler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            print("rf folder monitor starting")
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("rf watcher exiting")

        self.observer.join()

# catches any files uploaded and initites analysis
class RFHandler(FileSystemEventHandler):
    
    def on_any_event(self, event):
        if event.is_directory:
            return None

        # called when a file is first created/moved to tge folder
        elif event.event_type == 'created':

            from_location = event.src_path

            # don't analyze summary or any other types of files
            match = re.search(r'(i(B|b)ot|SSXL|ssxl)\d\d\d\d\d\d_\d\d\d\d\d\d\d\d_\d\d\d\d\d\d\.csv',
                                from_location)
            if not match:
                print("%s is not of the specified file name format" % from_location)  
                return

            print("Log File: %s Copied. Uploading..." % event.src_path)

            # simple delay to allow for file to transfer fully. Detect when file is done uploading?
            time.sleep(3)
            print("Upload complete. Analyzing...")

            # open the newly-created file and begin analysis
            rf_data = RFData(from_location)

            file_info = RFSummary.parse_filename(RFSummary, from_location)
            info_length = len(file_info)
            rf_data.unpack()
            summary = rf_data.get_summary()
            rf_data.write_trial_summary()

            # generate the output filename/location
            for i in range(len(from_location) - 1, 0, -1):
                if from_location[i] == "\\":
                    to_location = from_location[:i] + "\\summary\\SSXL_RF_Summary.csv"
                    break
            print("updating rf summary at: " + to_location)

            # stats for each column
            # add any additional calculations here
            NUM_STATS = 4
            maxs = []
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
            for col in data[info_length:]:
                if len(col) > 0:
                    maxs.append(max(col))
                    avgs.append(stats.mean(col))
                else: 
                    maxs.append(0)
                    avgs.append(0)
                if len(col) > 1: stds.append(stats.stdev(col))
                else: stds.append(0)

                if stds[-1] != 0:
                    avgs_stds.append(avgs[-1] / stds[-1])
                else:
                    avgs_stds.append(0)

            # add row titles
            data[0].insert(0, "Max")
            data[0].insert(1, "AVG")
            data[0].insert(2, "STD")
            data[0].insert(3, "AVG/STD")

            # add stats to data
            for i in range(len(data) - info_length):
                col = data[i + info_length]
            
                col.insert(0, maxs[i])
                col.insert(1, avgs[i])
                col.insert(2, stds[i])
                col.insert(3, avgs_stds[i])

            # fill in time slots with empties
            for col in data[1:info_length]:
                for i in range(NUM_STATS):
                    col.insert(i, "-")

            # re-write data and summarize
            try:
                with open(to_location, "w+") as out:
                    for item in title_line[:-1]:
                        out.write(item.strip() + ",")

                    # no comma after last item in row
                    out.write(title_line[- 1].strip())
                    out.write("\n")

                    for j in range(len(data[0])):
                        for i in range(len(data) - 1):
                            out.write(str(data[i][j]) + ",")

                        # no comma after last item in row
                        out.write(str(data[-1][j]))
                        out.write("\n")
                print("done")
            except PermissionError as e:
                print("summary file: %s is currently open/under use. Close and re-upload log file" % to_location)
                print(e)

            # generate the control charts. Gary requested that the position-based following errors
            # not be displayed for readability, hence the data[:-16] and the 3x3 grid (was 5x5)
            plot(data[:-16], title_line, info_length + 2, 1, NUM_STATS, 
                    "save", to_location[:-28], sup_title="RF", grid_size=(3, 3))
