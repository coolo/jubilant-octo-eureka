#!/usr/bin/python
#
# Copyright 2014 Jeffrey B. Layton
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

#
# Import standard Python modules if it is available
#
import sys


try:
    import matplotlib.pyplot as plt;
except:
    print "Cannot find matplotlib - needed for producing plots.";
    print "Stopping.";
    sys.exit();
# end try


# Import plot modules:
try:
    from vmstat_charts import *
except:
    print "Cannot find vmstat_charts python file. This is needed for this application.";
    print "Stopping.";
    sys.exit();
# end try

#
#
# partitionclass() Class definition
#
#
class partitionclass:

# Instantiated Object stores data as self.vmstat_partition = [];
#
#

    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.vmstat_partition = [];
    # end if
    
    
    #
    # This function appenda data to self.vmstat_partition
    #
    def store_append(self, data):
        self.vmstat_partition.append(data);
    # end if
    
    
    #
    # Output (HTML and Plots) on self.vmstat_partition data
    #
    def output(self, f_html, dirname, iplot, partition):

        # HTML header
        output_str = "Vmstat was run in Partition mode. This script takes the vmstat \n";
        output_str = output_str + "output and creates and html report for you that has three \n";
        output_str = output_str + "plots. Below are hyperlinks to the plots.\n";
        output_str = "<OL> \n";
        junk1 = "reads_writes";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Number of reads and writes</a> \n";
        junk1 = "read_sectors";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Number of sectors read</a> \n";
        junk1 = "requested_writes";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Number of writes requested</a> \n";
        output_str = output_str + "</OL> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + "<BR> \n\n";
        f_html.write(output_str);
        
        # Constants used for plotting:
        fsize = 8;
        flegsize = 6;
        ilongest = 26;
        # Compute box_expansion factor:
        junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
        box_expansion = round(junk1,2);
        
        # =======
        # Plot 1: Number of reads and number of writes (twochart)
        # =======
        iplot = iplot + 1;
        junk2 = "reads_writes";
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\"> Number of Read and Writes </a> \n";
        output_str = output_str + "</H3> \n \n";
        f_html.write(output_str);
        
        yd1 = [int(item[0]) for item in self.vmstat_partition];
        yd2 = [int(item[2]) for item in self.vmstat_partition];
        xd = range(1,(len(yd1)+1));
        ydata1 = [yd1];
        ydata2 = [yd2];
        xdata1 = [xd];
        xdata2 = [xd];
        xlabel = " ";
        ylabel1 = "Number";
        ylabel2 = "Number";
        d1 = ["Number of reads \n"];
        d2 = ["Number of writes \n"];
        junk2 = "reads_writes";
        filename = dirname + "/" + junk2 + ".png";
        
        # Call function make plots:
        Two_Chart(xdata1, ydata1, xdata2, ydata2, xlabel, ylabel1, ylabel2, d1, d2,  
                  fsize, flegsize, filename, box_expansion);
        
        # HTML for figure title
        output_str = "<P> \n";
        output_str = output_str + "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Number of Reads and Writes</strong></center><BR><BR> \n";
        output_str = output_str + "</P> \n\n";
        f_html.write(output_str);
        
        # =======
        # Plot 2: Number of sectors read
        # =======
        iplot = iplot + 1;
        junk2 = "read_sectors";
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">Number of sectors read</a> \n";
        output_str = output_str + "</H3> \n";
        f_html.write(output_str);

        yd = [int(item[1]) for item in self.vmstat_partition];
        xdata = range(1,(len(yd)+1));
        ydata = [yd];
        xdata = [xd];
        xlabel = " ";
        ylabel = "Number of sectors";
        dlabels = ["Number of sectors \n read \n"];
        filename = dirname + "/" + junk2 + ".png";
        
        # Call function to make the plot:
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
        
        # HTML for figure title
        output_str = "<P> \n";
        output_str = output_str + "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><strong>Figure " + junk2 + " - Number of sectors read</strong></center><BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        # =======
        # Plot 3: Number of writes requested
        # =======
        iplot = iplot + 1;
        junk2 = "requested_writes";
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">Number of writes requested</a> \n";
        output_str = output_str + "</H3> \n";
        f_html.write(output_str);
        
        yd = [int(item[3]) for item in self.vmstat_partition];
        xdata = range(1,(len(yd)+1));
        ydata = [yd];
        xdata = [xd];
        xlabel = " ";
        
        ylabel = "Number of requests";
        dlabels = ["Number of writes \n requested \n"];
        junk2 = "requested_writes";
        filename = dirname + "/" + junk2 + ".png";
        
        # Call fucntion to make the plot:
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
        
        # HTML for figure title
        output_str = "<P> \n";
        output_str = output_str + "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><strong>Figure " + junk2 + " - Number of writes requested</strong></center><BR><BR> \n";
        output_str = output_str + "</P> \n\n";
        f_html.write(output_str);
        
    # end def

# end class



