#!/usr/bin/python
#
# Enhanced data plotter for vmstat output. September 20, 2014
#
# Copyright Jeffrey B. Layton
#
# License: GNU GPL v2 (http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
# Version 2, June 1991
#
# Copyright (C) 1989, 1991 Free Software Foundation, Inc.  
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
import sys

try:
    import time;                       # Needed for time conversion function
    time_var = 1
except ImportError:
    time_var = 0;
    print "Cannot import time module - this is needed for this application.";
    print "Exiting..."
    sys.exit();
# end try


try:
    import matplotlib.pyplot as plt;   # Needed for plots
    matplotlib_var = 1
except ImportError:
    matplotlib_var = 0;
    print "Cannot import matplotlib module - this is needed for this application.";
    print "Exiting..."
    sys.exit();
# end try



# ------------------------------

def One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, expansion_box):
    
    #
    # Creates plot with data in xdata and ydata (lists of lists)
    #   Can have multitple lines in plot
    #
    # xdata = x-axis data for plots
    # ydata = y-axis data for plots
    # xlabel = x-axis label
    # ylabel = label for y-axis
    # dlabels = data labels (used in legend)
    # fsize = font size for tick labels
    # flegsize = font size for legend labels
    # filename = name of file for plot output
    # expansion_box = expansion factor on legend box
    #
    
    plt.figure(figsize=(24,10))
    # Create array of line colors/styles:
    # http://matplotlib.org/api/artist_api.html#matplotlib.lines.Line2D.lineStyles
    # line_style = ['-', '--', '-.'];
    # line_marker  = ['o', '^', 's', '*', '+', '<', '>', 'v'];
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k'];
    line_style = ['o-', '^--', 's-.', '*-', '<--', '>-.', 'v-', 'o--'];
    line_list = [];
    for line_type in line_style:
       for color in color_list:
          junk2 = color + line_type;
          line_list.append(junk2);
       # end for
    # end for
    
    # Plot:
    ax = plt.subplot(111);
    plt.ylim(0,100)
    plt.stackplot(xdata[0], ydata, labels=['User+Nice','System','Wait IO','Idle'], colors=['#C22326','#f37338','#fdb632','#027878'])
    # end for
    
    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * expansion_box, box.height])  
    leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                      borderpad=0.15, handletextpad=0.2);
    #frame1 = leg1.get_frame();
    #frame1.set_facecolor("0.80");           # Make legend box have a gray background
    #for t in leg1.get_texts():
    #    t.set_fontsize(flegsize);           # Change the font size of the legend text to flegsize
    # end for
    plt.grid();
    plt.ylabel(ylabel, fontsize=6);        # Use a 6 pt font for y-axis label
    plt.xlabel(xlabel, fontsize=fsize);
    plt.xticks(fontsize=fsize);
    plt.yticks(fontsize=fsize);
    
    # Either save the plot to a file or display it to the screen
    if (len(filename) == 0):
        plt.show();
    else:
        plt.savefig(filename);
        plt.close();
    # end if
   
# end def



def Two_Chart(xdata1, ydata1, xdata2, ydata2, xlabel, ylabel1, ylabel2, d1, d2,  
              fsize, flegsize, filename, box_expansion):
    #
    # Creates 2 horizontal supbplots, one above the other, with legends and
    #  one x-axis label at the the bottom. You can use multiple data sets
    #  for each of the two subplots.
    #
    # xdata1 = x-axis data for top plot
    # xdata2 = x-axis data for bottom plot
    # ydata1 = y-axis data for top plot
    # ydata2 = y-axis data for bottom plot
    # xlabel = x-axis label (only on bottom plot)
    # ylabel1 = label for top y-axis
    # ylabel2 = label for middle y-axis
    # d1 = data label for top plot
    # d2 = data label for middle plot
    # fsize = font size for tick labels
    # flegsize = font size for legend labels
    # filename = name of file for plot output
    # box_expansion = expansion factor on legend box
    #
    
    # Create array of line colors/styles:
    # http://matplotlib.org/api/artist_api.html#matplotlib.lines.Line2D.lineStyles
    # line_style = ['-', '--', '-.'];
    # line_marker  = ['o', '^', 's', '*', '+', '<', '>', 'v'];
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k'];
    line_style = ['o-', '^--', 's-.', '*-', '<--', '>-.', 'v-', 'o--'];
    line_list = [];
    for line_type in line_style:
       for color in color_list:
          junk2 = color + line_type;
          line_list.append(junk2);
       # end for
    # end for
    
    # Top plot
    ax1 = plt.subplot(211);                 # Define top plot using subplot function
    for i in range(0,len(xdata1)):
        plt.hist(xdata1[i], ydata1[i], line_list[i], label=d1[i], stacked=True, normed=True);
    # end for
    
    # Legend
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * box_expansion, box.height])  
    leg1 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                      borderpad=0.15, handletextpad=0.2);
    frame1 = leg1.get_frame();
    frame1.set_facecolor("0.80");           # Make legend box have a gray background
    for t in leg1.get_texts():
        t.set_fontsize(flegsize);           # Change the font size of the legend text to flegsize
    # end for

    plt.grid();
    plt.xlabel(" ");                        # Don't put an x-axis label since it's the top plot
    plt.ylabel(ylabel1, fontsize=6);        # Use a 6 pt font for y-axis label
    plt.xticks(fontsize=fsize);
    plt.yticks(fontsize=fsize);
    ax1.set_xticklabels([]);                # set x-axis tick label to blank (don't show them)

    
    
    # Bottom plot
    ax2 = plt.subplot(212);                 # Define bottom plot using subplot function
    for i in range(0,len(xdata2)):
        plt.hist(xdata2[i], ydata2[i], line_list[i], label=d2[i]);
    # end for

    # Legend
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * box_expansion, box.height])  
    leg2 = plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., labelspacing=0, 
                      borderpad=0.15, handletextpad=0.2);
    frame2 = leg2.get_frame();
    frame2.set_facecolor("0.80");           # Make legend box have a gray background
    for t in leg2.get_texts():
        t.set_fontsize(flegsize);           # Change the font size of the legend text to flegsize
    # end for
    plt.grid();
    plt.ylabel(ylabel2, fontsize=6);       # Use a 6 pt font for y-axis label
    plt.xlabel(xlabel);
    plt.xticks(fontsize=fsize);
    plt.yticks(fontsize=fsize);
    
    # Either save the plot to a file or display it to the screen
    if (len(filename) == 0):
        plt.show();
    else:
        plt.savefig(filename);
        plt.close();
    # end if
   
# end def


