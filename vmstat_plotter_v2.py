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
#
#
# To run the application, first gather the vmstat information using:
#
# [laytonjb ~]$ vmstat -n -t 1 100 > vmstat.out
#
# "1 100" which tells vmstat to use "1" second intervals  and "100" 
# means to gather data for 100 internvals (or 100 sceonds in this case).
# You need to always use the "-n" option sicne that forces vmstat to
# print out the headers one time. The "-t" option also prints the
# time with the output.
#
# Note: You can run vmstat in VM mode (the default), disk mode ("-d"),
# slabinfo mode ("-m"), or partition mode ("-p") since those are the
# only modes that produce output as a function of time.
#
# Then to run vmstat_plotter, the command is,
#
# [laytonjb ~]$ ./vmstat_plotter_v2.py vmstat.out
#
# where "vmstat.out" is the output from vmstat. The code is written
# in Python (obviously) and uses the shlex, time, os, and matplotlib
# modules. vmstat_plotter is smart enough to recognize which mode and
# option was used but it has only been tested with CentOS 6.5.
#
# When vmstat_plotter is done it will create a subdirectory "HTML_REPORT"
# that contains the plots and an html file "report.html". Open that
# html file in a browser or word processor and you will see the plots
# and a small write-up about them. Feel free to modify the code but
# please send back changes.
#
#

import sys
try:
    import shlex                      # Needed for splitting input lines
except ImportError:
    print "Cannot import shlex module - this is needed for this application.";
    print "Exiting..."
    sys.exit();
# end try


try:
    import os                          # Needed for mkdir
except ImportError:
    print "Cannot import os module - this is needed for this application.";
    print "Exiting..."
    sys.exit();
# end try



# Import submodules
from vmstat_charts import *

# Import class definitions:
from modeclass import *
from diskclass import *
from slabclass import *
from partitionclass import *

def help_out():
    # prints out help information and stops
    print " ";
    print "This application creates a short HTML based report from vmstat";
    print "output. The report includes plots tha thelp analyze the output";
    print "This version has only been tested with CentOS 6.5. ";
    print " ";
    print "To run the application first gather the vmstat information using: ";
    print "the following example.";
    print " ";
    print "[laytonjb ~]$ vmstat -n -t 1 100 > vmstat.out ";
    print " ";
    print "where \"1 100\" tells vmstat to use \"1\" second intervals and ";
    print "\"100\" means to gather data for 100 intervals (or 100 seconds in this";
    print "case). The output from vmstat is sent to a file which is ";
    print "\"vmstat.out\". You can name the file anything you want but be sure ";
    print "note the name of the file.";
    print " ";
    print "You can run vmstat in one of four modes and get time dependent output.";
    print "The first mode is referred to as the \"VM\" mode which is also the ";
    print "default mode for vmstat. It prints out some information about processes, ";
    print "memory usage, swap usage, IO usage, and CPU metrics. The second mode ";
    print "is referred to as the \"disk\" mode althought it covers all block devices. ";
    print "It uses the \"-d\" option. The third mode is the \"slabinfo\" mode and ";
    print "gives uses the \"-m\" option. The fourth mode is the \"partition\" mode ";
    print "and uses the \"-p <partition>\" option. ";
    print " ";
    print "There are other operating modes with vmstat but they don't produce any ";
    print "time dependent data. If you use these modes and then try to plot the data, ";
    print "the vmstat plotter code will fail in spectacular and unknown ways. ";
    print " ";
    print "Then to run vmstat_plotter using the vmstat output file, the command is, ";
    print " ";
    print "[laytonjb ~]$ ./vmstat_plotter_v2.py vmstat.out ";
    print " ";
    print "where \"vmstat.out\" is the output from vmstat. The code is written ";
    print "in Python (obviously) and uses the shlex, time, os, and matplotlib ";
    print "modules. Be sure this libraries are installed on your system. The code ";
    print "broken into several files and it is easiest to put them all in the same ";
    print "directory and copy the vmstat.out file to that directory for processing. ";
    print " ";
    print "When you run vmstat_plotter it will discover if which mode you used with ";
    print "vmstat. Please note that only the default mode can use the \"-t\" option ";
    print "in the output. The other modes should ignore that option. ";
    print " ";
    print "To get the help for vmstat_plotter, just use the \"-h\" option. ";
    print " ";

# end def


# ===================
# Main Python section
# ===================

if __name__ == '__main__':
    
    # Get the command line inputs
    input_options = sys.argv;
    help_flag = 0;
    for item in input_options:
        item2 = item.lower();
        if (item2 == "-h"):
            help_flag = 1;
        # end if
    # end for
    if (help_flag == 1):
        help_out();
        sys.exit();
    # end if
    
    # vmstat output file name (input to this code)
    input_filename = input_options[-1];
    
    print "vmstat plotting script";
    print " ";
    print "input filename: ",input_filename;
    
    # Initialize lists that will store data
    date_list = [];
    time_list = [];
    meridian_list = [];
    
    open_success = 0;
    if os.path.isfile(input_filename):
        open_success = 1;
    # end if
    
    # Open file
    if (open_success == 1):
        f = open(input_filename,'r');
    # end if
    
    # Instanitate objects
    mode_obj = modeclass();
    disk_obj = diskclass();
    slab_obj = slabclass();
    partition_obj = partitionclass();
    
    # Read first line of output
    junk = f.readline();
    junk2 = shlex.split(junk);
    mode = junk2[0];   # Guess at vmstat mode
    
    # Default: (includes -a can include times -t)
    # procs
    # Disk mode: (-d)
    # disk-   (repeats - need to read devices first - read until repeat)
    # Partition: (-p)
    # <partition> (if -p option is used)
    # Slabinfo: (-m)
    # Cache = slabinfo (-m) (repeats - need to read items first - read until repeat)
    # 
    # Read second line of output and read headers
    if ( (mode == "procs") or (mode == "disk-") or (mode == "Cache") ):
        line = f.readline();
        col_headers = shlex.split(line);
    else:
        partition = mode;
    # end if
    
    # Read in data
    if (mode == "procs"):
        print "VMSTAT in default mode"
        
        inact_flag = 0;
        if (col_headers[4] == "inact"):
            inact_flag = 1;
        # end if   
        
        for line in f.readlines():
            currentline = shlex.split(line);
            mode_obj.store(currentline);
        # end for
        time_flag = 0;
        if (len(currentline) > 17):
            time_flag = 1;
        # end if
    # end for
    elif (mode == "disk-"):
        print "VMSTAT in disk mode"
        # IFELD DESCRIPTION FOR DISK MODE
        # Reads
        #    total: Total reads completed successfully
        #    merged: grouped reads (resulting in one I/O)
        #    sectors: Sectors read successfully
        #    ms: milliseconds spent reading
        # Writes
        #    total: Total writes completed successfully
        #    merged: grouped writes (resulting in one I/O)
        #    sectors: Sectors written successfully
        #    ms: milliseconds spent writing
        #  IO
        #    cur: I/O in progress
        #    s: seconds spent for I/O
        for line in f.readlines():
            currentline = shlex.split(line);
            device = currentline[0];
            disk_obj.store_append(device, currentline[1:]);
        # end for
    elif (mode == "Cache"):
        print "VMSTAT in slabinfo mode"
        # FIELD DESCRIPTION FOR SLAB MODE
        #    cache: Cache name
        #    num: Number of currently active objects
        #    total: Total number of available objects
        #    size: Size of each object
        #    pages: Number of pages with at least one active object
        #    totpages: Total number of allocated pages
        #    pslab: Number of pages per slab
        for line in f.readlines():
            currentline = shlex.split(line);
            metric = currentline[0];
            slab_obj.store_append(metric, currentline[1:]);
        # end for
    else:
        # has to be partition (we hope)
        print "VMSTAT in partition mode"
        # FIELD DESCRIPTION FOR DISK PARTITION MODE
        #    reads: Total number of reads issued to this partition
        #    read sectors: Total read sectors for partition
        #    writes : Total number of writes issued to this partition
        #    requested writes: Total number of write requests made for partition
        vmstat_partition = [];
        for line in f.readlines():
            currentline = shlex.split(line);
            partition_obj.store_append(currentline[0:]);
        # end for
    # end if

    
    # 
    # HTML Report initialization
    #    Write all data files to subdirectory called HTML_REPORT
    #    File is report.html
    
    # Define report location
    dirname ="./HTML_REPORT";
    if not os.path.exists(dirname):
        os.makedirs(dirname);
    # end if
    html_filename = dirname + '/report.html';
    f_html = open(html_filename, 'w')
    
    # Print HTML Report header
    output_str = "<H2>\n";
    output_str = output_str + "vmstat Report for file: " + input_filename + " \n";
    output_str = output_str + "</H2>\n";
    output_str = output_str + " \n";
    f_html.write(output_str);
    
    # HTML Introduction
    output_str = "<H3>\n";
    output_str = output_str + "Introduction \n";
    output_str = output_str + "</H3> \n \n";
    f_html.write(output_str);
    
    output_str = "<P>This report plots the vmstat output contained in file: \n";
    output_str = output_str + sys.argv[1] + ". ";
    f_html.write(output_str);
    if (mode == "procs"):
        iplot = 0;
        iplot = mode_obj.output(f_html, dirname, iplot, time_flag, inact_flag);
    elif (mode == "disk-"):
        iplot = 0;
        iplot = disk_obj.output(f_html, dirname, iplot);
    elif (mode == "Cache"):
        iplot = 0;
        iplot = slab_obj.output(f_html, dirname, iplot);
    else:
        print "partiion duck";
        iplot = 0;
        iplot = partition_obj.output(f_html, dirname, iplot, partition);
    # end if
    output_str = "</P>\n";
    output_str = output_str + " \n";
    f_html.write(output_str);

# end

