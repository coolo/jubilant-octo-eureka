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
# diskclass() Class definition
#
#
class diskclass:

# Instantiated Object stores data as self.vmstat_devices.
#
#

    #
    # init method (just initialize the dictionary)
    #
    def __init__(self):
        self.vmstat_device = {};
    # end if
    
    
    #
    # This function appenda data to self.vmstat_devices
    #
    def store_append(self, device, data):
        if (device in self.vmstat_device):
            self.vmstat_device[device].append(data);
        else:
            self.vmstat_device[device] = data;
        # end if
    # end if
    
    
    #
    # Output (HTML and Plots) on self.vmstat_devices data
    #
    def output(self, f_html, dirname, iplot):
        
        # Get list of devices
        devices = [item for item in self.vmstat_device];    # list of block devices
        
        # HTML header
        output_str = "Vmstat was run in Disk mode. This script takes the vmstat \n";
        output_str = output_str + "output and creates and html report for you that has three \n";
        output_str = output_str + "plots for every device tracked. Below are hyperlinks to \n";
        output_str = output_str + "each device so you can easily navigate to them to see all \n";
        output_str = output_str + "of the plots for each. \n";
        output_str = "<OL> \n";
        base = "disk_";
        for dev in devices:
            output_str = output_str + "   <LI><a href=\"#" + (base+dev) + "\">" + dev + "</a> \n";
        # end for
        output_str = output_str + "</OL> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + " \n";
        f_html.write(output_str);
        
        # Constants for all plots
        fsize = 8;
        flegsize = 6;
        ilongest = 26;
        # Compute box_expansion factor:
        junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
        box_expansion = round(junk1,2);
        
        # ----------------------------------
        # Make plots by looping over devices
        # ----------------------------------
        for dev in self.vmstat_device:
            # Data for device:
            data = self.vmstat_device[dev];
            
            output_str = "<H3> \n"
            output_str = output_str + " <a id=\"" + (base+dev) + "\">Device: " + dev + "</a> \n";
            output_str = output_str + "</H3> \n";
            f_html.write(output_str);
            
            # =======
            # Plot 1:
            # =======
            iplot = iplot + 1;
            read_total = [];
            read_merged = [];
            read_sectors = [];
            write_total = [];
            write_merged = [];
            write_sectors = [];
            for item in data:
                read_total.append(int(data[0]));
                read_merged.append(int(data[1]));
                read_sectors.append(int(data[2]));
                write_total.append(int(data[4]));
                write_merged.append(int(data[5]));
                write_sectors.append(int(data[6]));
            # end for
            ydata1 = [read_total, read_merged, read_sectors];
            ydata2 = [write_total, write_merged, write_sectors];
            xd = range(1,(len(read_total)+1));
            xdata1 = [xd, xd, xd];
            xdata2 = [xd, xd, xd];
            xlabel = " ";
            
            ylabel1 = "Numbers";
            ylabel2 = "Numbers";
            junk1 = "Total reads successfully \n completed \n";
            junk2 = "Number of grouped reads \n (resulting in one IO) \n";
            junk3 = "Sectors read successfully \n";
            d1 = [junk1, junk2, junk3];
            junk1 = "Total writes successfully \n completed \n";
            junk2 = "Number of grouped writes \n (resulting in one IO) \n";
            junk3 = "Sectors written successfully \n";
            d2 = [junk1, junk2, junk3];
            filename = dirname + "/" + base + dev + "_" + str(iplot) + ".png";
            
            # Call function to make the plot:
            Two_Chart(xdata1, ydata1, xdata2, ydata2, xlabel, ylabel1, ylabel2, d1, d2,  
                      fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<P> \n";
            output_str = output_str + "<center> \n";
            output_str = output_str + "<img src=\"" + base + dev + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " -Read and Write Totals for device " + dev + "</strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            
            # =======
            # Plot 2:
            # =======
            iplot = iplot + 1;
            read_ms = [];
            write_ms = [];
            for item in data:
                read_ms.append(int(data[3]));
                write_ms.append(int(data[7]));
            # end for
            ydata = [read_ms, write_ms];
            xdata = [xd, xd];
            xlabel = " ";
            ylabel = "Time (ms)";
            junk1 = "Total time reading \n (ms) \n";
            junk2 = "Total time writing \n (ms) \n";
            dlabels = [junk1, junk2];
            filename = dirname + "/" + base + dev + "_" + str(iplot) + ".png";
            
            # Call a function to make the plot
            One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"" + base + dev + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Time spent reading and writing (ms) for device " + dev + " </strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            # =======
            # Plot 3: cur, s
            # =======
            iplot = iplot + 1;
            cur = [];
            s = [];
            for item in data:
                cur.append(int(data[8]));
                s.append(int(data[9]));
            # end for
            ydata1 = [cur];
            ydata2 = [s];
            xdata1 = [xd];
            xdata2 = [xd];
            xlabel = " ";
            ylabel1 = ["IO in progress"];
            ylabel2 = ["Seconds spent doing IO"];
            junk1 = "IO in progress \n (GG) \n";
            d1 = [junk1];
            junk1 = "Seconds spent doing \n IO (s) \n";
            d2 = [junk1];
            filename = dirname + "/" + base + dev + "_" + str(iplot) + ".png";
            
            # Call function to make plots:
            Two_Chart(xdata1, ydata1, xdata2, ydata2, xlabel, ylabel1, ylabel2, d1,  
                      d2, fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"" + base + dev + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Current IO and Seconds spent doing IO for " + dev + " </strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            output_str = output_str + "</P> \n \n";
        # end for
        
        return iplot;
    # end def

# end class



