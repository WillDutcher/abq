============================
 ABQ Data Entry Application
============================

Description
===========

This program provides a data entry form for ABQ Agrilabs laboratory data.

Features
--------

* Provides a validated entry form to ensure correct data
* Stores data to ABQ-format CSV files
* Auto-fills form fields whenever possible

Authors
=======

Alan D Moore, 2018
William C Dutcher, 2019

Requirements
============

* Python 3
* Tkinter

Usage
=====

To start the application, run::

  python3 ABQ_Data_Entry/abq_data_entry.py


General Notes
=============

The CSV file will be saved to your current directory in the format "abq_data_record_CURRENTDATE.csv", where CURRENTDATE is today's date in ISO format.

This program only appends to the CSV file.  You should have a spreadsheet program installed in case you need to edit or check the file.
#-----------------------------------------#
There's no prescribed set of contents for a README file, but as a basic guideline, consider the following sections:

  +  Description: A brief description of the program and its function. We can reuse the description from our specification, or something like it. This might also contain a brief list of the main features.
  +  Author information: The names of the authors and copyright date. This is especially important if you plan to share your software, but even for something in-house it's useful for future maintainers to know who created the software and when.
  +  Requirements: A list of the software and hardware requirements for the software, if any.
  +  Installation: Instructions for installing the software, its prerequisites, dependencies, and basic setup.
  +  Configuration: How to configure the application and what options are available. This is generally aimed at the command-line or configuration file options, not options set interactively in the program.
  +  Usage: A description of how to launch the application, command-line arguments, and other notes a user would need to know to use the basic functionality of the application.
  +  General notes: A catch-all for notes or critical information users should be aware of.
  +  Bugs: A list of known bugs or limitations in the application.

