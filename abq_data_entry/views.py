import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import widgets as w

class DataRecordForm(tk.Frame):         # Build class as subclass of tkinter Frame class
  """The input form for our widgets."""

  def __init__(self, parent, fields, *args, **kwargs):  # Build ovr layout of data record form for constructor
    super().__init__(parent, *args, **kwargs)   # Inherit identified args and kwargs from the constructor
    self.inputs = {}        # Dictionary to hold references to all form's input widgets; field name is the key

    # Build the overall recordinfo frame; parent for all recordinfo widgets
    recordinfo = tk.LabelFrame(self, text="Record Information") # Set 'recordinfo' to below widgets

    # DataRecordForm: First row of widgets
    self.inputs['Date'] = w.LabelInput(recordinfo, "Date",    # Start of form's widgets, row 0, columns 0-2
                              field_spec=fields['Date'])
    self.inputs['Date'].grid(row=0, column=0)                 # Placed at 0, 0

    self.inputs['Time'] = w.LabelInput(recordinfo, "Time",    # parent, label, input_class, input_var, input_args
                              field_spec=fields['Time'])
    self.inputs['Time'].grid(row=0, column=1)                 # Placed at 0, 1

    self.inputs['Technician'] = w.LabelInput(recordinfo,      # parent, label, <default input_class>, input_var
                                    "Technician", 
                                    field_spec=fields['Technician'])
    self.inputs['Technician'].grid(row=0, column=2)           # Placed at 0, 2

    # DataRecordForm: Second row of widgets
    self.inputs['Lab'] = w.LabelInput(recordinfo, "Lab",      # parent, label, input_class, input_var, input_args
                             field_spec=fields['Lab'])
    self.inputs['Lab'].grid(row=1, column=0)                  # Placed at 1, 0

    self.inputs['Plot'] = w.LabelInput(recordinfo, "Plot",    # parent, label, input_class, input_var, input_args
                              field_spec=fields['Plot'])
    self.inputs['Plot'].grid(row=1, column=1)                 # Placed at 1, 1

    self.inputs['Seed sample'] = w.LabelInput(recordinfo,     # parent, label, <default input_class>, input_var
                                     "Seed sample",
                                     field_spec=fields['Seed sample'])
    self.inputs['Seed sample'].grid(row=1, column=2)          # Placed at 1, 2


    # Build the overall environmentinfo frame; parent for all environmentinfo widgets
    environmentinfo = tk.LabelFrame(self, text="Environment Data")  # Set 'environmentinfo' to below widgets

    # Environment Data: Third row of widgets
    self.inputs['Humidity'] = w.LabelInput(environmentinfo,   # parent, label, input_class, input_var, input_args
                                  "Humidity (g/m³)",
                                  field_spec=fields['Humidity'])
    self.inputs['Humidity'].grid(row=0, column=0)             # Placed at 0, 0


    self.inputs['Light'] = w.LabelInput(environmentinfo,      # parent, label, input_class, input_var, input_args
                               "Light (klx)", field_spec=fields['Light'])
    self.inputs['Light'].grid(row=0, column=1)                # Placed at 0, 1

    self.inputs['Temperature'] = w.LabelInput(environmentinfo,# parent, label, input_class, input_var, input_args
                                     "Temperature (°C)", field_spec=fields['Temperature'])
    self.inputs['Temperature'].grid(row=0, column=2)          # Placed at 0, 2

    # Environment Data: Fourth row of widgets
    self.inputs['Equipment Fault'] = w.LabelInput(              # parent, label, input_class, input_var
                                         environmentinfo, "Equipment Fault",
                                         field_spec=fields['Equipment Fault'])
    self.inputs['Equipment Fault'].grid(row=1, column=0,      # Place at 1, 0
                                      columnspan=3)

    # Build the overall plantinfo frame; parent for all plantinfo widgets
    plantinfo = tk.LabelFrame(self, text="Plant Data")  # Set 'plantinfo' to below widgets

    # Plant Data: Fifth row of widgets
    self.inputs['Plants'] = w.LabelInput(plantinfo, "Plants",   # parent, label, input_class, input_var, input_args
                                field_spec=fields['Plants'])      # Default incrementer is 1
    self.inputs['Plants'].grid(row=0, column=0)               # Place at 0, 0

    self.inputs['Blossoms'] = w.LabelInput(plantinfo,           # parent, label, input_class, input_var, input_args
                                  "Blossoms", field_spec=fields['Blossoms'])  # Default incrementer is 1
    self.inputs['Blossoms'].grid(row=0, column=1)               # Place at 0, 1

    self.inputs['Fruit'] = w.LabelInput(plantinfo, "Fruit",     # parent, label, input_class, input_var, input_args
                               field_spec=fields['Fruit'])     # Default incrementer is 1
    self.inputs['Fruit'].grid(row=0, column=2)               # Place at 0, 2

    # Plant Data: Sixth row of widgets
    # Height data# Create variables to be updated for min/max height
    # They can be referenced for min/max variables
    min_height_var = tk.DoubleVar(value='-infinity')
    max_height_var = tk.DoubleVar(value='infinity')

    self.inputs['Minimum Height'] = w.LabelInput(plantinfo,    # parent, label, input_class, input_var, input_args
                                    "Minimum Height (cm)", field_spec=fields['Minimum Height'],
                                    input_args={"max_var": max_height_var, "focus_update_var": min_height_var})     # Default incrementer is 1
    self.inputs['Minimum Height'].grid(row=1, column = 0)    # Place at 1, 0

    self.inputs['Maximum Height'] = w.LabelInput(plantinfo,    # parent, label, input_class, input_var, input_args
                                    "Maximum Height (cm)", field_spec=fields['Maximum Height'],
                                    input_args={"min_var": min_height_var, "focus_update_var": max_height_var})     # Default incrementer is 1
    self.inputs['Maximum Height'].grid(row=1, column = 1)    # Place at 1, 1

    self.inputs['Median Height'] = w.LabelInput(plantinfo,     # parent, label, input_class, input_var, input_args
                                    "Median Height (cm)", field_spec=fields['Median Height'],
                                    input_args={"min_var": min_height_var, "max_var": max_height_var})     # Default incrementer is 1
    self.inputs['Median Height'].grid(row=1, column = 2)     # Place at 1, 2


    # Notes section: Sevent (LAST) row
    self.inputs['Notes'] = w.LabelInput(self, "Notes", # self (placed directly on form, parent, input_class & args)
                               input_class=tk.Text, input_args={"width": 75, "height": 3})
    self.inputs['Notes'].grid(row=3, column=0, sticky=tk.W)
    # self.inputs['Notes'].grid(row=3, column=0, sticky=(tk.W + tk.E))  # Should I use this one?

    # Set the overall placement of each layout widget collective
    recordinfo.grid(row=0, column=0, sticky=(tk.W + tk.E))      # Place widgets in form's first row
    environmentinfo.grid(row=1, column=0, sticky=(tk.W + tk.E)) # Place widgets in form's second row
    plantinfo.grid(row=2, column=0, sticky=(tk.W + tk.E)) # Place widgets in form's third row
    # notesinfo.grid(row=3, column=0, sticky=(tk.W + tk.E)) # Place widget in form's fourth and final row # NO NEED

    # Default the form to have blank values
    self.reset()

  def get(self):                              # Method lives in form's class
    """Retrieve data from form."""
    data = {}                                 # Create empty library to collect all widget information
    for key, widget in self.inputs.items():   # For every key and value identified in self.inputs.items()...
      data[key] = widget.get()                # Populate data dictionary with key and requisite values(s)
    return data                               # When complete, return the library

  def reset(self):                            # Method lives in form's class
    """Reset the form once all information has been saved."""

    # Gather the values to keep for each lab
    lab = self.inputs['Lab'].get()
    time = self.inputs['Time'].get()
    technician = self.inputs['Technician'].get()
    plot = self.inputs['Plot'].get()
    plot_values = self.inputs['Plot'].input.cget('values')

    # Clear all values
    for widget in self.inputs.values():       # For every widget (keys in the dictionary)...
      widget.set('')                          # Set the value to blank/empty value

    current_date = datetime.today().strftime('%Y-%m-%d')
    self.inputs['Date'].set(current_date)
    self.inputs['Time'].input.focus()
  
    # Check if we need to put our values back, then do it.
    if plot not in ('', plot_values[-1]):
      self.inputs['Lab'].set(lab)
      self.inputs['Time'].set(time)
      self.inputs['Technician'].set(technician)
      next_plot_index = plot_values.index(plot) + 1
      self.inputs['Plot'].set(plot_values[next_plot_index])
      self.inputs['Seed sample'].input.focus()

  def get_errors(self):
    """Get a list of field errors in the form."""
    errors = {}
    for key, widget in self.inputs.items():
      if hasattr(widget.input, 'trigger_focusout_validation'):
        widget.input.trigger_focusout_validation()
      if widget.error.get():
        errors[key] = widget.error.get()
    return errors



