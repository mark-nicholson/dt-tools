dt-tools
========

Python tools to manage Flattened Device Trees

Intent
------

The goal of this effort is to create Python based utilities which will allow developers to manage, manipulate and verify flattened device trees.


Tools, Classes:

    - devicetree/fdt.py  This is the baseline parser for .dtb files
    - devicetree/dtc.py  A wrapper script around the "dtc" tool (ie. compiler) so it can be easily automated
    - devicetree/gui/*   A PySide/Qt4 based GUI which will provide graphical views of the device tree


Requirements:
------------

  To develop and/or use these, different packages have different needs.

    * devicetree/fdt.py

         Requires nothing more than a basic python interpreter

    * devicetree/dtc.py

         Requires that you have 'dtc' and 'libfdt' installed and working

    * devicetree/gui/*

         Requires PySide, Qt4, QT4-utilities



	 