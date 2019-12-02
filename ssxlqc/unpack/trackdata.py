import statistics as stats

# a class to unpack and format Track data files
class TrackData(object):
    def __init__(self, filename):

        self.filename = filename

        # order: slow position error, slow velocity error, slow phase current
        # fast position order, fast velocity error, fast phase current
        self.data = [[], [], [], [], [], []]

        # indexes within data[] lists of the relevent data columns
        self.slow_pos_index = 0
        self.slow_vel_index = 1
        self.slow_current_index = 2
        self.fast_pos_index = 3
        self.fast_vel_index = 4
        self.fast_current_index = 5

        # column locations
        self.pos_error_col = 2
        self.vel_col = 3
        self.vel_com_col = 4
        self.current_col = 5

        self.SLOW_VELOCITY = 50000.3

        # convert data type names to index locations
        self.data_dict = {
            "slow_pos_err": 0,
            "slow_vel_err": 1,
            "slow_current": 2,
            "fast_pos_err": 3,
            "fast_vel_err": 4,
            "fast_current": 5,
        }

        # string  list for file output
        self.output_formatter = []

        self.count = 0

        self.unpacked = False

    def unpack(self):

        print("unpacking")
        try:
            with open(self.filename, "r") as in_put:

                # initialize output list
                s = ("Reading #,Slow Pos Err,Slow Vel Err,Slow Phase A,Fast Pos Err,"
                    "Fast Vel Err,Fast Phase A")
                self.output_formatter.append(s)

                # iterate through each line of the input
                for line in in_put:
                    line_list = line.split(",")

                    # don't read the first line of the file
                    if self.count > 0:

                        output = ""
                        output += str(self.count) + ","

                        # slow data
                        if abs(float(line_list[self.vel_com_col])) == self.SLOW_VELOCITY:
                            # slow following error
                            err = line_list[self.pos_error_col]
                            self.data[self.slow_pos_index].append(float(err))
                            output += err + ","

                            # slow velocity error
                            err = float(line_list[self.vel_col]) - float(line_list[self.vel_com_col])
                            self.data[self.slow_vel_index].append(float(err))
                            output += str(err) + ","

                            # slow phase current
                            amps = line_list[self.current_col]
                            self.data[self.slow_current_index].append(float(amps))
                            output += amps.strip() + ",-,-,-"

                        # fast data
                        else:
                            # fast following error
                            err = line_list[self.pos_error_col]
                            self.data[self.fast_pos_index].append(float(err))
                            output += "-,-,-," + err + ","

                            # fast velocity error
                            err = float(line_list[self.vel_col]) - float(line_list[self.vel_com_col])
                            self.data[self.fast_vel_index].append(float(err))
                            output += str(err) + ","

                            # fast phase current
                            amps = line_list[self.current_col]
                            self.data[self.fast_current_index].append(float(amps))
                            output += amps.strip()

                        self.output_formatter.append(output)
                    self.count += 1

            self.unpacked = True
            print("unpacked")

        except FileNotFoundError as e:
            print("unpack failed")
            print("log file: %s does not exist" % self.filename)
            print(e)

    # private helper method to enforce unpacking first
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
            print("formatted date written")
        except PermissionError as e:
            print("format file: %s in use, cannot write" % name)
            print(e)
 
    # return one of the relevent data lists. See __init__() for labels
    def get_data(self, type):
        self.__unpack_check()
        return self.data[self.data_dict.get(type)]

    # write a summary of the trial to a .csv file
    def write_trial_summary(self):
        self.__unpack_check()
        name = self.filename[:-4] + "_Summary.csv"

        print("writing trial summary to: " + name)
        try:
            with open(name, "w+") as out:

                s = ("Statistic,Slow Pos Err,Slow Vel Err,Slow Phase A,Fast Pos Err,"
                    "Fast Vel Err,Fast Phase A\n")
                out.write(s)

                # absolute max row
                out.write("Absolute Max,")
                for col in self.data:
                    out.write(self.__abs_max(col, "s"))
                out.write("\n")
            
                # absolute min row
                out.write("Absolute Min,")
                for col in self.data:
                    out.write(self.__abs_min(col, "s"))
                out.write("\n")

                # absolute range row
                out.write("Absolute Range,")
                for col in self.data:
                    out.write(self.__abs_range(col, "s"))
                out.write("\n")

                # average row
                out.write("Absolute Average,")
                for col in self.data:
                    out.write(self.__safe_avg([abs(x) for x in col], "s"))
                out.write("\n")

                # abs std row
                out.write("Absolute STD,")
                for col in self.data:
                    out.write(self.__safe_std([abs(x) for x in col], "s"))
                out.write("\n")

                # true max row
                out.write("True Max,")
                for col in self.data:
                    out.write(self.__true_max(col, "s"))
                out.write("\n")

                # true min row
                out.write("True Min,")
                for col in self.data:
                    out.write(self.__true_min(col, "s"))
                out.write("\n")

                # True range row
                out.write("True Range,")
                for col in self.data:
                    out.write(self.__true_range(col, "s"))
                out.write("\n")

                # true average row
                out.write("True Average,")
                for col in self.data:
                    out.write(self.__safe_avg(col, "s"))
                out.write("\n")

                # true std row
                out.write("True STD,")
                for col in self.data:
                    out.write(self.__safe_std(col, "s"))
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
    
    # avoid finding avg of empty list
    def __safe_avg(self, input_list, s):
        if len(input_list) > 0:
            avg = stats.mean(input_list)
            if s == "s":
                return str(avg) + ","
            return avg        
        if s == "s":
            return "-,"
        return 0


    # avoid finding std of empty list
    def __safe_std(self, input_list, s):
        if len(input_list) > 0:
            std = stats.stdev(input_list)
            if s == "s":
                return str(std) + ","
            return std        
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

    # get the line length of the file
    def get_file_length(self):
        self.__unpack_check()
        return self.count

    def get_trial_time(self):
        self.__unpack_check()
        return

    # return the high-level summary values
    # ORDER: count, slow position error (avg, std, avg+3*std), slow velocity error (avg, std, avg+3*std), 
    # slow phase current (avg, std, avg+3*std), fast position order (avg, std, avg+3*std), 
    # fast velocity error (avg, std, avg+3*std), fast phase current (avg, std, avg+3*std), 
    def get_summary(self):
        self.__unpack_check()
        output = []

        output.append(self.get_file_length())
        for col in self.data:
            absolute = [abs(x) for x in col]
            avg = self.__safe_avg(absolute, "n")
            std = self.__safe_std(absolute, "n")
            output.append(avg)
            output.append(std)
            output.append(avg + (3 * std))
        return output
