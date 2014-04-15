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


    * estimate the size of treeview name column and set the default width to that

    * if a DTS is selected, open the "conversion" dialogue
         - create the conversion dialog to drive DTC

    * create display widget to show the "address map"

    * put in docstrings!
         - Run Sphinx to generate docs

    * Tidy up FDT to ensure that python variables hold TRANSLATED data (endianness corrected integers and decoded strings)

    * Remove hacks to work around 'bytes' being passed to QT constructors
