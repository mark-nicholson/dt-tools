Flattened Device Tree Tools
===========================

Python tools to manage Flattened Device Trees

Intent
------

The goal of this effort is to create Python based utilities which will allow developers to manage, manipulate and verify flattened device trees.


Tools, Classes:

    - devicetree/fdt.py  This is the baseline parser for .dtb files
    - devicetree/dtc.py  A wrapper script around the "dtc" tool (ie. compiler) so it can be easily automated
    - devicetree/gui/*   A PySide/Qt4 based GUI which will provide graphical views of the device tree

   Within the GUI, the hope is to be able to:
   	  * decode a DTB file
	  * display the tree hierarchy
	  * draw an "address space map" which identifies where each section relates in the physical map


Requirements:
-------------

  To develop and/or use these, different packages have different needs.

    * devicetree/fdt.py

         Requires nothing more than a basic python interpreter

    * devicetree/dtc.py

         Requires that you have 'dtc' and 'libfdt' installed and working

    * devicetree/gui/*

         Requires PySide, Qt4, QT4-utilities


To Do List:
-----------

    * Add search capabilities for the FDT
      	  - name by text, regex, ...
	  - boolean logic to combine value match

    * if a DTS is selected, open the "conversion" dialogue
         - create the conversion dialog to drive DTC

    * create display widget to show the "address map" tab

    * create display widget to show the "interrupt map" tab

    * create a statistics display
      	     File size
	     version
	     header size
	     table size
	     num blocks
	     num properties
	     max depth
	     strings size
	     strings count
	     ...

    * put in docstrings!
         - Run Sphinx to generate docs
