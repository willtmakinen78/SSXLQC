import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from configparser import ConfigParser
import numpy as np
import pandas as pd
import statistics as stats
import ssxlqc.chart.nelsonrules as nr

# the max number of most recent points to use in calculating the avg and std
# POINTS_TO_USE = 15

def plot(data, title_line, start_col, multiple, num_stats, 
            show_mode, location, sup_title=None, grid_size=(1, 1), 
            title_strip=None, rules=True):

    # the figure object from which the oo interface can be accessed
    fig = plt.figure()

    # go through once and calculate how many cols/plots need to be made
    fig_count = 0
    for i in range(len(data)):
        if (i - start_col) % multiple == 0 and i >= start_col: 
            fig_count += 1

    # determine the size of the plot grid
    rows = grid_size[0]
    cols = grid_size[1]
    if fig_count <= 0: raise Exception("no data columns found")

    # place one big title on top of everything
    if sup_title != None: fig.suptitle(sup_title, fontsize=25)

    # the start of the save location
    filename = location + "\\charts\\"
    if not os.path.exists(filename): os.makedirs(filename)

    # create parser object
    parser = ConfigParser()

    # get the path to the .ini file
    script_path = os.path.abspath(__file__) 
    path_list = script_path.split(os.sep)
    script_directory = path_list[0:len(path_list)-1]
    rel_path = "chartconfig.ini"
    path = "/".join(script_directory) + "/" + rel_path

    # get the number of points to calculate from/show from the conf file
    parser.read(path)
    points_to_calculate = int(parser['points_to_use']['calc'])
    points_to_show = int(parser['points_to_use']['show'])

    # the first column of data[][] holds the trial names
    names = data[0]
            
    # iterate through the full data set again to do the actual plotting
    print("generating control charts")
    for i in range(len(data)):
        if (i - start_col) % multiple == 0 and i >= start_col:

            col = data[i]
            col_length = len(col)

            # only use the last POINTS_TO_USE data points, unless there aren't
            # enough available
            start_index_show = col_length - points_to_show
            if start_index_show < num_stats:
                start_index_show = num_stats
            points_show = col[start_index_show:]

            # get the labels as a subset of the names[] list
            labels = names[start_index_show:]

            # only use the last points_to_calculate data points to determine avg and std,
            # unless there aren't enough available
            start_index_calc = col_length - points_to_calculate
            if start_index_calc < num_stats:
                start_index_calc = num_stats
            points_calc = col[start_index_calc:]

            # do stats only on the most recent data
            avg = 0
            std = 0
            if len(points_calc) >= 2:
                avg = stats.mean(points_calc)
                std = stats.stdev(points_calc)
            else: raise Exception("insufficient (<2) summary rows to perform analysis ")

            # calculate the current plot index
            index = int((i - start_col) / multiple + 1)

            # formatting
            ax = fig.add_subplot(rows, cols, index)
            fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.3, hspace=0.37)
            # plot annotation
            if title_strip == None: title = title_line[i].strip()
            else: title = title_line[i].strip()[:title_strip]
            
            # ax.set_title(title)
            x_label = "{}: last {} trials".format(title, col_length - start_index_show)
            ax.set_xlabel(x_label, fontsize='large')

            # draw the avg and std lines
            colors = ['c', 'y', 'r']
            for j in range(1, 4):
                label = str(j) + "s"
                ax.axhline(y=(avg + (std * j)), color=colors[j-1], linestyle='--', label=label)
                if (avg - (std * j)) >= 0:
                    ax.axhline(y=(avg - (std * j)), color=colors[j-1], linestyle='--')
                else: ax.axhline(y=0, color='#000000')
            # avg line
            ax.axhline(y=avg, color='#007000', label='avg')
            
            # if no nelson rules have been specified, just plot the points
            # generate x-values first
            x = []
            for i in range(len(points_show)):
                x.append(i)
            # then plot
            ax.plot(x, points_show, '-o', label='success')

            # add trial labels
            for i in range(len(labels)):
                ax.annotate(labels[i][4:], (i, points_show[i]), fontsize='x-small', rotation=80)

            # convert to pandas series to feed into nr module
            series = pd.Series(points_show)

            # otherwise label rule violations
            if rules == True:
                rules_bool = []
                rules_bool.append(nr.rule1(series, avg, std))
                rules_bool.append(nr.rule2(series, avg, std))
                rules_bool.append(nr.rule3(series, avg, std))
                rules_bool.append(nr.rule4(series, avg, std))
                rules_bool.append(nr.rule5(series, avg, std))
                rules_bool.append(nr.rule6(series, avg, std))
                rules_bool.append(nr.rule7(series, avg, std))
                rules_bool.append(nr.rule8(series, avg, std))

                # if a point violates a nelson rule save its value in a list
                # otherwise, save a None in its place
                rules_val = []
                for i in range(len(rules_bool)):
                    rules_val.append([])
                    for j in range(len(rules_bool[i])):
                        if rules_bool[i][j] == True:
                            rules_val[i].insert(j, points_show[j])
                        else: rules_val[i].insert(j, None)
                
                # plot the nelson rules on top of everything else already plotted
                markers = ['H', '+', '.', 'o', '*', '<', '>', '^']
                for i in range(len(rules_val)):
                    label = "rule " + str(i + 1)
                    marker_size = 40 - (4 * i)
                    ax.plot(rules_val[i], marker=markers[i],  label=label)

            # legend has to be added at the end
            ax.legend(loc='upper left', bbox_to_anchor=(1,1), fontsize='small')
    print("control charts generated")

    # save/show all at once at the end
    if show_mode == "save":
        print("saving full chart...")
        filename += "all_charts.png"
        fig.set_size_inches(24, 12)
        plt.savefig(filename, dpi=250, bbox_inches="tight")
        print("saved")
    else: 
        print("showing charts, close out before continuing")
        plt.show()
        print("chart exited")