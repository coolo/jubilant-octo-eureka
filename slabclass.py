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
# slabclass() Class definition
#
#
class slabclass:

# Instantiated Object stores data as self.vmstat_slabs.
#
#

    #
    # init method (just initialize the dictionary)
    #
    def __init__(self):
        self.vmstat_slabs = {};
    # end if
    
    
    #
    # This function adds data to self.vmstat_slabs
    #
    def store_add(self, metric, data):
        self.vmstat_slabs[metric] = data;
    # end if
    
    
    #
    # This function appenda data to self.vmstat_slabs
    #
    def store_append(self, metric, data):
        if (metric in self.vmstat_slabs):
            self.vmstat_slabs[metric].append(data);
        else:
            self.vmstat_slabs[metric] = data;
        # end if
    # end if
    
    
    #
    # Output (HTML and Plots) on self.vmstat_slabs data
    #
    def output(self, f_html, dirname, iplot):
        # Gather metrics to be plotted:
        metrics = [item for item in self.vmstat_slabs];    # list of metrics
        
        # HTML header
        output_str = "Vmstat was run in Slab mode. This script takes the vmstat \n";
        output_str = output_str + "output and creates an html report for you that has three \n";
        output_str = output_str + "plots for every metric tracked. Below are hyperlinks to \n";
        output_str = output_str + "each metric so you can easily navigate to them to see all \n";
        output_str = output_str + "of the plots for each. \n";
        output_str = "<OL> \n";
        base = "slab_";
        for metric in metrics:
            output_str = output_str + "   <LI><a href=\"#" + (base+metric) + "\">" + metric + "</a> \n";
        # end for
        output_str = output_str + "</OL> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + " \n";
        f_html.write(output_str);
        
        # Constants for all plots:
        fsize = 8;
        flegsize = 6;
        ilongest = 26;
        # Compute box_expansion factor:
        junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
        box_expansion = round(junk1,2);
        
        # ----------------------------------
        # Make plots by looping over metrics
        # ----------------------------------
        for metric in self.vmstat_slabs:
            # Extract data for specific metric:
            data = self.vmstat_slabs[metric];
            
            # HTML header for metric
            output_str = "<H3> \n"
            output_str = output_str + " <a id=\"" + (base+metric) + "\">Metric: " + metric + "</a> \n";
            output_str = output_str + "</H3> \n";
            f_html.write(output_str);
            
            # =======
            # Plot 1:
            # =======
            iplot = iplot + 1;         
            num_objects = [];
            total_objects = [];
            for item in data:
                num_objects.append(int(data[0]));
                total_objects.append(int(data[1]));
            # end for
            ydata = [num_objects, total_objects];
            xd = range(1,(len(num_objects)+1));
            xdata = [xd, xd];
            xlabel = " ";
            ylabel = "Number of objects";
            junk1 = "Number of currently \n active objects \n";
            junk2 = "Total number of \n available objects \n";
            dlabels = [junk1, junk2];
            filename = dirname + "/" + base + metric + "_" + str(iplot) + ".png";
            
            # Call function to make plots:
            One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<P> \n";
            output_str = output_str + "<center> \n";
            output_str = output_str + "<img src=\"" + base + metric + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Currently available and total objects for metric " + metric + "</strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            # =======
            # Plot 2: size
            # =======
            iplot = iplot + 1;
            size = [];
            for item in data:
                size.append(int(data[2]));
            # end for
            ydata = [size];
            xdata = [xd];
            xlabel = " ";
            ylabel = ["Size of object"];
            dlabels = ["Size of object"];
            filename = dirname + "/" + base + metric + "_" + str(iplot) + ".png";
            
            # Call function to make plots:
            One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"" + base + metric + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Size of each object for metric " + metric + " </strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            # =======
            # Plot 3: Pages
            # =======
            iplot = iplot + 1;
            number_pages = [];
            for item in data:
                number_pages.append(int(data[3]));
            # end for
            ydata = [number_pages];
            xdata = [xd];
            xlabel = " ";
            ylabel = "Number of pages)";
            dlabels = ["Number of pages with \n at least one active \n object"];
            filename = dirname + "/" + base + metric + "_" + str(iplot) + ".png";
            
            # Call function to make plots:
            One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, box_expansion);
            
            # HTML for figure title
            output_str = "<center> \n";
            output_str = output_str + "<img src=\"" + base + metric + "_" + str(iplot) + ".png" + "\"> \n";
            output_str = output_str + "<BR><strong>Figure " + str(iplot) + " - Number of pages with at least one active object for metric " + metric + " </strong></center><BR><BR> \n";
            f_html.write(output_str);
            
            output_str = output_str + "</P> \n \n";
        # end for
        
        return iplot
    # end def

# end class



