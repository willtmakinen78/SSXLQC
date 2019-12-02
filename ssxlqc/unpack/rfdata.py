import statistics as stats
from ssxlqc.numtest import is_number

# a class to unpack and format RF data files
class RFData(object):

    def __init__(self, filename):

        print("initializing")

        self.filename = filename

        # list for regularly-updating values: (list, column location)
        # order: amb_temp, track_motor_temp, track_drive_temp, track_current, track_rpm, 
        # all_error, conveyer_drive_temp, conveyer_current, conveyer_rpm
        self.regular_list = [
            ([], 25), ([], 26), ([], 32), ([], 70), ([], 72), 
            ([], 71), ([], 33), ([], 94), ([], 96)
        ]
        # indexes of the above list that correspond to temperature data
        # these datasets must be divided by 10
        self.temp_indexes = [0, 1, 2, 5]

        # lists for following errors
        # order: Asc, Dsc, HT, HB, TCU, TCD, BCU, BCD
        self.loaded_error_list = [[], [], [], [], [], [], [], []]
        self.unloaded_error_list = [[], [], [], [], [], [], [], []]

        # convert column names to index locations
        self.regular_index_dict = {
            "amb_temp": 0,

            "track_motor_temp": 1,
            "track_drive_temp": 2,
            "track_current": 3,
            "track_rpm": 4,

            "all_error": 5,

            "conveyer_drive_temp": 6,
            "conveyer_current": 7,
            "conveyer_rpm": 8
        }
        self.unloaded_error_dict = {
            "u_asc": 0,
            "u_dsc": 1,
            "u_ht": 2,
            "u_hb": 3,
            "u_tcu": 4,
            "u_tcd": 5,
            "u_bcu": 6,
            "u_bcd": 7,
        }
        self.loaded_error_dict = {
            "l_asc": 0,
            "l_dsc": 1,
            "l_ht": 2,
            "l_hb": 3,
            "l_tcu": 4,
            "l_tcd": 5,
            "l_bcu": 6,
            "l_bcd": 7,
        }

        # following error columns
        self.profile_col = 47
        self.load_col = 1
        self.following_error_col = 71

        # used to get the length of the trial
        self.clock_col = 0
        self.clock_list = []

        # string  list for file output
        self.output_formatter = []

        self.PARAMETER_COUNT = 28
        self.ERROR_COUNT = 16

        self.count = -1
        self.unpacked = False

        print("initialized")

    # fill out the lists
    def unpack(self):
        print("unpacking")

        try:
            with open(self.filename, "r") as data:
        
                # initialize output list
                s = ("reading count,amb temp,track motor temp,track drive temp,track current,"
                    "track rpm,all error,conveyer drive temp,conveyer current,conveyer rpm,Profile,Div,"
                    "u asc,u dsc,u ht,u hb,u tcu,u tcd,u bcu,u bcd,l asc,l dsc,l ht,l hb,"
                    "l tcu,l tcd,l bcu,l bcd")
                self.output_formatter.append(s)

                # iterate through each line of the input
                for line in data:
                    line_list = line.split(",")

                    # don't read the first or last line of the file
                    if len(line_list) > 1 and self.count > 0:

                        output_list = []
                        output_list.append(str(self.count))
                        output = ""
               
                        for tup in self.regular_list:
                            if is_number(line_list[tup[1]]):
                                val = int(line_list[tup[1]])
                                tup[0].append(val)
                                output_list.append(val)
                            else: output_list.append(0)
                
                        self.clock_list.append(line_list[self.clock_col])

                        # grab the following error depending on the stage of the loop
                        profile = int(line_list[self.profile_col])
                        load_state = int(line_list[self.load_col])
                        error = int(line_list[self.following_error_col])

                        output_list.append(profile)

                        if load_state % 2 == 0:
                            # even, unloaded
                            output_list.append("even")

                            for i in range(self.PARAMETER_COUNT - self.ERROR_COUNT):
                                output += str(output_list[i]) + ","
                            for i in range(self.ERROR_COUNT):
                                if i == profile: 
                                    if len(self.unloaded_error_list[profile]) > 0:
                                        if error != self.unloaded_error_list[profile][-1]:
                                            self.unloaded_error_list[profile].append(error)
                                            output += str(error) + ","
                                        else: output += "-,"
                                    else: 
                                        self.unloaded_error_list[profile].append(error)
                                        output += str(error) + ","
                                else: output += "-,"

                        else:
                            # odd, loaded
                            output_list.append("odd")

                            for i in range(self.PARAMETER_COUNT - self.ERROR_COUNT):
                                output += str(output_list[i]) + ","
                            for i in range(self.ERROR_COUNT):
                                if i - (self.ERROR_COUNT / 2) == profile: 
                                    if len(self.loaded_error_list[profile]) > 0:
                                        if error != self.loaded_error_list[profile][-1]:
                                            self.loaded_error_list[profile].append(error)
                                            output += str(error) + ","
                                        else: output += "-,"
                                    else: 
                                        self.loaded_error_list[profile].append(error)
                                        output += str(error) + ","
                                else: output += "-,"
                        
                    
                        self.output_formatter.append(output)
                    self.count += 1

            # final step: divide all temperature datesets by 10
            for i in range(len(self.regular_list)):
                if self.temp_indexes.count(i) > 0:
                    
                    col = self.regular_list[i][0]
                    col[:] = [x / 10.0 for x in col]

            self.unpacked = True
            print("unpacked")

        except FileNotFoundError as e:
            print("unpack failed")
            print("log file: %s does not exist" % self.filename)
            print(e)
        except Exception as e:
            print("unpack failed for unforseen reason: ")
            print(e)

    # private helper method to ensure data has been unpacked
    def __unpack_check(self):
        if self.unpacked == False:
            raise Exception("data has not been unpacked yet")

    # return a list of each formatted line as a string
    def get_formatted_data(self):
        self.__unpack_check()
        return self.output_formatter
    
    # write each of the formatted lines to a file
    def write_formatted_data(self):
        self.__unpack_check()
        name = self.filename[:-4] + "_Formatted.csv"

        print("formatting data to: " + name)
        try:
            with open(name, "w+") as out:
                for s in self.output_formatter:
                    out.write(s + "\n")
            print("formatted data written")
        except PermissionError as e:
            print("format file: %s in use, cannot write" % name)
            print(e)

    # return the requested regular data list. See __init__() for labels
    def get_regular_data(self, type):
        self.__unpack_check()
        return self.regular_list[self.regular_index_dict.get(type)]

    # return the requested unloaded data list. See __init__() for labels
    def get_unloaded_data(self, type):
        self.__unpack_check()
        return self.unloaded_error_list[self.unloaded_error_dict.get(type)]

    # return the requested loaded data list. See __init__() for labels
    def get_loaded_data(self, type):
        self.__unpack_check()
        return self.loaded_error_list[self.loaded_error_dict.get(type)]

    # write a summary of the trial to a .csv file
    def write_trial_summary(self):
        self.__unpack_check()
        name = self.filename[:-4] + "_Summary.csv"

        print("writing trial summary to: " + name)
        try:
            with open(name, "w+") as out:

                s = ("Statistic,amb temp,track motor temp,track drive temp,track current,"
                    "track rpm,all err,conveyer drive temp,conveyer current,conveyer rpm,u asc,"
                    "u dsc,u ht,u hb,u tcu,u tcd,u bcu,u bcd,l asc,l dsc,l ht,l hb,l tcu,"
                    "l tcd,l bcu,l bcd\n")
                out.write(s)

                # absolute max row
                out.write("Absolute Max,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__abs_max(col, "s"))
                # find max abs val for following errors
                for col in self.unloaded_error_list:
                    out.write(self.__abs_max(col, "s"))
                for col in self.loaded_error_list:
                    out.write(self.__abs_max(col, "s"))
                out.write("\n")
            
                # absolute min row
                out.write("Absolute Min,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__abs_min(col, "s"))
                # find min abs val for following errors
                for col in self.unloaded_error_list:
                    out.write(self.__abs_min(col, "s"))
                for col in self.loaded_error_list:
                    out.write(self.__abs_min(col, "s"))
                out.write("\n")

                # absolute range row
                out.write("Absolute Range,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__abs_range(col, "s"))
                # find abs range for following errors
                for col in self.unloaded_error_list:
                    out.write(self.__abs_range(col, "s"))
                for item in self.loaded_error_list:
                    out.write(self.__abs_range(col, "s"))
                out.write("\n")

                # abs average row
                out.write("Absolute Average,")
                for item in self.regular_list:
                    current_col = item[0]
                    if len(current_col) > 0:
                        avg = stats.mean([abs(x) for x in current_col])
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                # find avg of following errors
                for col in self.unloaded_error_list:
                    if len(col) > 0:
                        avg = stats.mean([abs(x) for x in col])
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                for col in self.loaded_error_list:
                    if len(col) > 0:
                        avg = stats.mean([abs(x) for x in col])
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                out.write("\n")

                # std row
                out.write("STD,")
                for item in self.regular_list:
                    current_col = item[0]
                    if len(current_col) > 1:
                        std = stats.stdev(current_col)
                        out.write(str(std) + ",")
                    else: out.write("-,")
                # find std for following errors
                for col in self.unloaded_error_list:
                    if len(col) > 1:
                        std = stats.stdev(col)
                        out.write(str(std) + ",")
                    else: out.write("-,")
                for col in self.loaded_error_list:
                    if len(col) > 1:
                        std = stats.stdev(col)
                        out.write(str(std) + ",")
                    else: out.write("-,")
                out.write("\n")

                # true max row
                out.write("True Max,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__true_max(col, "s"))
                # find true max for following errors
                for col in self.unloaded_error_list:
                    out.write(self.__true_max(col, "s"))
                for col in self.loaded_error_list:
                    out.write(self.__true_max(col, "s"))
                out.write("\n")

                # true min row
                out.write("True Min,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__true_min(col, "s"))
                # find true min for following errors
                for col in self.unloaded_error_list:
                    out.write(self.__true_min(col, "s"))
                for col in self.loaded_error_list:
                    out.write(self.__true_min(col, "s"))
                out.write("\n")

                # true range row
                out.write("True Range,")
                for item in self.regular_list:
                    col = item[0]
                    out.write(self.__true_range(col, "s"))
                # find true range for following errors
                for item in self.unloaded_error_list:
                    out.write(self.__true_range(col, "s"))
                for item in self.loaded_error_list:
                    out.write(self.__true_range(col, "s"))
                out.write("\n")

                # true average row
                out.write("True Average,")
                for item in self.regular_list:
                    current_col = item[0]  
                    if len(current_col) > 0:
                        avg = stats.mean(current_col)
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                # find true avg of following errors
                for col in self.unloaded_error_list:
                    if len(col) > 0:
                        avg = stats.mean(col)
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                for item in self.loaded_error_list:
                    if len(col) > 0:
                        avg = stats.mean(col)
                        out.write(str(avg) + ",")
                    else: out.write("-,")
                out.write("\n")

            print("trial summary written")
        except PermissionError as e:
                print("trual summary file: %s is currently open/under use" % name)
                print(e)
    
    # private helper method to calulate the largest absolute value of a list
    # use parameter "s" to return a string representation, or something else for numeric
    def __abs_max(self, input_list, s):
        absolute_list = []
        for i in range(len(input_list)):
            absolute_list.append(abs(float(input_list[i])))
        if len(absolute_list) > 0:
            if s == "s":
                return str(max(absolute_list)) + ","
            return max(absolute_list)
        if s == "s":
            return "-,"
        return 0

    # private helper method to calulate the smallest absolute value of a list
    # use parameter "s" to return a string representation, or something else for numeric
    def __abs_min(self, input_list, s):
        absolute_list = []
        for i in range(len(input_list)):
            absolute_list.append(abs(float(input_list[i])))
        if len(absolute_list) > 0:
            if s == "s":
                return str(min(absolute_list)) + ","
            return min(absolute_list)
        if s == "s":
            return "-,"
        return 0

    # private helper method to calculate range of absolute vals
    # use parameter "s" to return a string representation, or something else for numeric
    def __abs_range(self, input_list, s):
        if len(input_list) > 0:
            maximum = self.__abs_max(input_list, "n")
            minimum = self.__abs_min(input_list, "n")
            if s == "s":
                return str(maximum - minimum) + ","
            return float(maximum) - float(minimum)     
        if s == "s":
            return "-,"
        return 0
    
    # private helper method to avoid finding max of empty list
    def __true_max(self, input_list, s):
        if len(input_list) > 0:
                maximum = max(input_list)
                if s == "s":
                    return str(maximum) + ","
                return maximum        
        if s == "s":
            return "-,"
        return 0
    
    # private helper method to avoid finding min of empty list
    def __true_min(self, input_list, s):
        if len(input_list) > 0:
            minimum = min(input_list)
            if s == "s":
                return str(minimum) + ","
            return minimum        
        if s == "s":
            return "-,"
        return 0

     # private helper method to avoid finding range of empty list
    def __true_range(self, input_list, s):
        if len(input_list) > 0:
            maximum = self.__true_max(input_list, "n")
            minimum = self.__true_min(input_list, "n")
            if s == "s":
                return str(maximum - minimum) + ","
            return float(maximum) - float(minimum)        
        if s == "s":
            return "-,"
        return 0

    # return the line length of the file
    def get_file_length(self):
        return self.count
    
    # get the length of the trial
    def get_trial_time(self):
        return self.__true_range(self.clock_list, "n") / 60000

    # return the high-level summary values
    # order: reading_count, trial_length, amb_temp, track_motor_temp, track_drive_temp, 
    # track_current, track_rpm, all_error, conveyer_drive_temp,conveyer_current, conveyer_rpm, u_asc, 
    # u_dsc, u_ht, u_hb, u_tcu, u_tcd, u_bcu, u_bcd, l_asc, l_dsc, l_ht, l_hb, l_tcu, 
    # l_tcd, l_bcu, l_bcd
    def get_summary(self):
        self.__unpack_check()
        output = []

        output.append(self.get_file_length())
        output.append(self.get_trial_time())
        for item in self.regular_list:
            col = item[0]
            output.append(self.__abs_max(col, "n"))
        for col in self.unloaded_error_list:
            output.append(self.__abs_max(col, "n"))
        for col in self.loaded_error_list:
            output.append(self.__abs_max(col, "n"))
        return output






        






    
        




