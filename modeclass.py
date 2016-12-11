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
# Import standard Python modiles if it is available
#
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
# modeclass() Class definition
#
#
class modeclass:

# Instantiated Object stores data as self.vmstat_data.
#
#
    
    #
    # init method (just initialize the list)
    #
    def __init__(self):
        self.vmstat_data = [];
    # end if
    
    
    #
    # This function appenda data to self.vmstat_data
    #
    def store(self, data):
        self.vmstat_data.append(data);
    # end if
    
    
    #
    # Output (HTML and Plots) on self.vmstat_data data
    #
    def output(self, f_html, dirname, iplot, time_flag, inact_flag):
        # HTML header:
        if (inact_flag == 1):
            output_str = " Vmstat was run in VM mode with the active/inactive memory ";
            if (time_flag == 1):
                output_str = output_str + "flag set (-a) and time stamps enabled (-t). \n";
            else:
                output_str = output_str + "flag set (-a). \n";
            # end if
        else:
            if (time_flag == 1):
                output_str = " Vmstat was run in VM mode with time stamps enable (-t). \n";
            else:
                output_str = " Vmstat was run in VM mode. \n";
            # end if
        # end if
        
        output_str = output_str + " This script takes the vmstat output and creates a series  \n";
        output_str = output_str + "of plots and a html report for you. Below are hyperlinks \n";
        output_str = output_str + "to various plots within the report \n";
        output_str = output_str + "<BR><BR> \n";
        f_html.write(output_str);
        
        output_str = "<OL> \n";
        junk1 = "procs";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Processes waiting on run time and in uniterruptible sleep</a> \n";
        if (inact_flag == 1):
            junk1 = "memory_inact";
            output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Memory usage with the active/inactive flag</a> \n";
        else:
            junk1 = "memory";
            output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Memory usage with the buffer/cache</a> \n";
        # end if
        junk1 = "swap";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">Memory Swap per second</a> \n";
        junk1 = "io";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">IO blocks per second</a> \n";
        junk1 = "system";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">System metrics</a> \n";
        junk1 = "CPU";
        output_str = output_str + "   <LI><a href=\"#" + junk1 + "\">CPU metrics</a> \n";
        output_str = output_str + "</OL> \n";
        output_str = output_str + "</P> \n";
        output_str = output_str + " \n";
        f_html.write(output_str);
        
        # Constants for the plots:
        ilongest = 26;
        fsize = 8;
        flegsize = 6;
        # Compute box_expansion factor:
        junk1 = -0.0082702674*ilongest + 1.0538027948;   # Curve fit of # chars vs. expansion box
        expansion_box = round(junk1,2);
        
        # ---------
        # Figure 1:
        # ---------
        iplot = iplot + 1;
        junk2 = "procs";
        ydata1 = [int(item[0]) for item in self.vmstat_data];
        ydata2 = [int(item[1]) for item in self.vmstat_data];
        ydata = [ydata1, ydata2];
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            xdata = [junk1, junk1];
            xlabel = "Time (secs)";
        # end if
        ylabel = "Number of Process";
        d1 = "r = number of processes \n" + "waiting for run time \n";
        d2 = "b = number of processes \n" + "in uninterruptible sleep \n";
        dlabels = [d1, d2];
        filename = dirname + "/procs";
        
        # Call function to make plot
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, flegsize, filename, expansion_box);
        
        # HTML for plot
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">Processes waiting on run time and in uniterruptible sleep</a>";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the number of processes waiting for run time \n";
        output_str = output_str + "and the number of processes in uninterruptible sleep.  \n";
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Processes waiting on run time and in uniterruptible sleep</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        # -----------------------------------------
        # Figure 2: swp, free, buff, cache vs time
        # -----------------------------------------
        iplot = iplot + 1;
        if (inact_flag == 1):
            junk2 = "memory_inact";
        else:
            junk2 = "memory";
        # end if
        swp = [(int(item[2])/1024.) for item in self.vmstat_data];
        free = [(int(item[3])/1024.) for item in self.vmstat_data];
        if (inact_flag == 1):
            inact = [(int(item[4])/1024.) for item in self.vmstat_data];
            active = [(int(item[5])/1024.) for item in self.vmstat_data];
            ydata = [swp, free, inact, active];
            
            d1 = "swpd = Amount of virtual \n memory used \n";
            d2 = "free = Amount of idle \n memory \n";
            d3 = "inact = Amount of inactive \n memory \n";
            d4 = "active = Amount of active \n memory \n";
            dlabels = [d1, d2, d3, d4];
            filename = dirname + "/memory_inact";
        else:
            buff = [(int(item[4])/1024.) for item in self.vmstat_data];
            cache = [(int(item[5])/1024.) for item in self.vmstat_data];
            ydata = [swp, free, buff, cache];
            
            d1 = "swpd = Amount of virtual \n memory used \n";
            d2 = "free = Amount of idle \n memory \n";
            d3 = "buff = Amount of memory \n used as buffers \n";
            d4 = "cache = Amount of memory \n used as cache \n";
            dlabels = [d1, d2, d3, d4];
            filename = dirname + "/memory";
        # end if
        ylabel = "Amount of memory (MB)";
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1, xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            xdata = [junk1, junk1, junk1, junk1];
            xlabel = "Time (secs)";
        # end if
        
        # Call function to make plot:
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, 
                  flegsize, filename, expansion_box);
        
        # HTML output
        output_str = "<H3> \n"
        if (inact_flag == 1):
            output_str = output_str + "<a id=\"" + junk2 + "\">Memory usage with the active/inactive flag</a> \n";
        else:
            output_str = output_str + "<a id=\"" + junk2 + "\">Memory usage with the buffer/cache</a> \n";
        # end if
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the memory usage. It plots the \n";
        output_str = output_str + "the amount of virtual memory (in MB) and the amount of \n";
        output_str = output_str + "idle or free memory (in MB). \n";
        if (inact_flag == 1):
            output_str = output_str + "It also plots the active and inactive amount of  \n";
            output_str = output_str + "memory in MB. \n";
        else:
            output_str = output_str + "It also plots the amount of memory used for buffers  \n";
            output_str = output_str + "(in MB) and the amount of memory used as cache (in MB). \n";
        # end if
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        
        # HTML Output:
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 +".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Processes waiting on run time and in uniterruptible sleep</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        # ----------------------------
        # Figure 3: si, so versus time
        # ----------------------------
        iplot = iplot + 1;
        junk2 = "swap";
        ydata1 = [(int(item[6])/1024) for item in self.vmstat_data];
        ydata2 = [(int(item[7])/1024) for item in self.vmstat_data];
        ydata = [ydata1, ydata2];
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            xdata = [junk1, junk1];
            xlabel = "Time (secs)";
        # end if
        ylabel = "Rate of Memory swap (MB/s)";
        d1 = "si = rate of memory \n swapped in from disk \n (MB/s) \n";
        d2 = "so = rate of memroy \n swapped out from disk \n (MB/s) \n";
        dlabels = [d1, d2];
        filename = dirname + "/swap";
        
        # Call function to make the plot
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, 
                  flegsize, filename, expansion_box);
        
        # HTML Output
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">Rate of memory swapped in/out from disk (MB/s)</a>";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the rate of memory swap in MB/s both into and \n";
        output_str = output_str + "from disk.  \n";
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Rate of memory swap both in and out from disk (MB/s)</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        # ----------------------------
        # Figure 4: bi, bo versus time
        # ----------------------------
        iplot = iplot + 1;
        junk2 = "io";
        ydata1 = [int(item[8]) for item in self.vmstat_data];
        ydata2 = [int(item[9]) for item in self.vmstat_data];
        ydata = [ydata1, ydata2];
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            xdata = [junk1, junk1];
            xlabel = "Time (secs)";
        # end if
        
        ylabel = "Rate of blocks moved (Blocks/s)";
        d1 = "bi = rate of blocks received \n from a block device\n (blocks/s) \n";
        d2 = "bo = rate of blocks received \n from a block device\n (blocks/s) \n";
        dlabels = [d1, d2];
        filename = dirname + "/io";
        
        # Call a function to make the plot:
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, 
                  flegsize, filename, expansion_box);
        
        # HTML output
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">Rate of blocks received/sent to block device</a>";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the rate of blocks received and sent to a block \n";
        output_str = output_str + "device (blocks/s).  \n";
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Rate of blocks received/sent to block devices</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        # ----------------------------
        # Figure 5: in, cs versus time
        # ----------------------------
        iplot = iplot + 1;
        junk2 = "system";
        ydata1 = [int(item[10]) for item in self.vmstat_data];
        ydata2 = [int(item[11]) for item in self.vmstat_data];
        ydata = [ydata1, ydata2];
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            xdata = [junk1, junk1];
            xlabel = "Time (secs)";
        # end if
        ylabel = "System metrics per second";
        d1 = "in = Number of interrupts \n per second, including the \n clock \n ";
        d2 = "cs = Number of context \n switches per second) \n";
        dlabels = [d1, d2];
        filename = dirname + "/system";
        
        # Call a function to make the plot: 
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, 
                  flegsize, filename, expansion_box);
        
        # HTML output:
        output_str = "<H3> \n"
        output_str = output_str + " <a id=\"" + junk2 + "\">System metrics per second</a>";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the system metrics of interrupts and\n";
        output_str = output_str + "and context switches per second.  \n";
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - System metrics</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);


        # ----------------------------------------
        # Figure 6: us, sy, id, wa, st versus time
        # ----------------------------------------
        iplot = iplot + 1;
        junk2 = "CPU";
        vmstat_us = [int(item[12]) for item in self.vmstat_data];
        vmstat_sy = [int(item[13]) for item in self.vmstat_data];
        vmstat_id = [int(item[14]) for item in self.vmstat_data];
        vmstat_wa = [int(item[15]) for item in self.vmstat_data];
        vmstat_st = [int(item[16]) for item in self.vmstat_data];
        ydata = [vmstat_us, vmstat_sy, vmstat_id, vmstat_wa, vmstat_st];
        d1 = "us = Percent CPU time \n spent running non-kernel \n code (user+nice time) \n";
        d2 = "sy = Percent CPU time \n spent running kernel \n code (system time) \n";
        d3 = "id = Percent CPU time \n spent in idle \n";
        d4 = "wa = Percent CPU time \n wiating for IO \n";
        d5 = "st = No report \n";
        dlabels = [d1, d2, d3, d4, d5];
        filename = dirname + "/CPU";
        ylabel = ["Percent CPU Time", "Percent CPU Time", "Percent CPU Time", "Percent CPU Time", "Percent CPU Time"];
        if (time_flag == 0):
            xd1 = range(1,(len(ydata1)+1));
            xdata = [xd1, xd1, xd1, xd1, xd1];
            xlabel = " ";
        else:
            pattern = '%Y-%m-%d %H:%M:%S'                  # '2014-09-12', '13:03:39', 'EDT'
            year1 = [item[17] for item in self.vmstat_data];
            time1 = [item[18] for item in self.vmstat_data];
            iloop = -1;
            epoch_time = [];
            for item in year1:
                iloop = iloop + 1;
                junk = item + " " + time1[iloop];
                epoch = int(time.mktime(time.strptime(junk, pattern)))
                epoch_time.append(epoch);
            # end for
            base_epoch = epoch_time[0];
            junk1 = [(item-base_epoch) for item in epoch_time];
            data = dict()
            while junk1:
               data[junk1.pop(0)] = (vmstat_us.pop(0), vmstat_sy.pop(0), vmstat_id.pop(0), vmstat_wa.pop(0), vmstat_st.pop(0))
            #print data
            vmstat_us = []
            vmstat_sy = []            
            vmstat_id = []            
            vmstat_wa = []           
            vmstat_st = []        
            junk1 = []
            #print "Time (sec),User+Nice,System,Wait,Idle"
            for i in range(0, 1200):
                junk1.append(i)
                if i in data:
                    vmstat_us.append(data[i][0])
                    vmstat_sy.append(data[i][1])
                    vmstat_id.append(data[i][2])
                    vmstat_wa.append(data[i][3])
                    vmstat_st.append(data[i][4])
                else:
                    vmstat_us.append(0)
                    vmstat_sy.append(0)
                    vmstat_id.append(0)
                    vmstat_wa.append(0)
                    vmstat_st.append(100)
                #print "%d,%d,%d,%d,%d" % (i, vmstat_us[i], vmstat_sy[i],vmstat_wa[i],vmstat_id[i])
            xdata = [junk1, junk1, junk1, junk1];
            ydata = [vmstat_us, vmstat_sy, vmstat_wa, vmstat_id];
            xlabel = "Time (secs)";
        # end if
        
        # Call function to make plot:
        One_Chart(xdata, ydata, xlabel, ylabel, dlabels, fsize, 
                  flegsize, filename, expansion_box);
        
        # HTML output
        output_str = "<H3> \n"
        output_str = output_str + "<a id=\"" + junk2 + "\">CPU metrics (percent time)</a> \n";
        output_str = output_str + "</H3> \n";
        output_str = output_str + " \n";
        output_str = output_str + "<P>This figure plots the CPU metrics as percent CPU time. \n";
        output_str = output_str + "It plots percent CPU time running non-kernel code (user + nide), \n";
        output_str = output_str + "the percent CPU time running kernel time, the percent CPU time \n";
        output_str = output_str + "spent waiting for IO, and the percent CPU time stolen from a \n";
        output_str = output_str + "virtual machine. \n";
        if (time_flag == 1):
            output_str = output_str + "For this case the data is plotted versus time. \n";
        # end if
        f_html.write(output_str);
        output_str = "<center> \n";
        output_str = output_str + "<img src=\"" + junk2 + ".png" + "\"> \n";
        output_str = output_str + "<BR><BR><strong>Figure " + str(iplot) + " - Percent CPU Time for CPU metrics</strong></center><BR><BR> \n";
        output_str = output_str + "<BR><BR> \n";
        output_str = output_str + "</P> \n \n";
        f_html.write(output_str);
        
        return iplot;
    # end def

# end class


