"""
This is considered the CONTROLLER in MVC.
Starts and stops the application.
Calls for data manipulation--but data is *not* here, in models.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import views as v
from . import models as m

class Application(tk.Tk):
  """Application root window."""

  def __init__(self, *args, **kwargs):        # No parent identified since this is the root window
    """Instantiate any objects from the class; subclassed from tkinter root class."""
    super().__init__(*args, **kwargs)             # Take arguments from class it was subclassed from

    self.title("ABQ Data Entry Application")  # Title of application
    self.resizable(width=False, height=False) # Do not allow user to resize window

    ttk.Label(self,
              text="ABQ Data Entry Application",      # Start with Label constructor for the main window
              font=("TKDefaultFont", 16)).grid(row=0) # Column not necessary because this is overall window layout

    self.recordform = v.DataRecordForm(self, m.CSVModel.fields)    # Create recordform that calls DataRecordForm class; pass self
    self.recordform.grid(row=1, padx=10)      # Set the recordform in row 1

    # Create the save button for the form
    self.savebutton = ttk.Button(self, text="Save",   # Construct save button; perform on_save function on click
                          command=self.on_save)
    self.savebutton.grid(row=2, padx=10, sticky=tk.E) # Place button underneath record form on right side

    # Status bar
    self.status = tk.StringVar()              # Allow status to be callable so it may be edited
    self.statusbar = ttk.Label(self,          # Construct label with default status set to status
                         textvariable=self.status)
    self.statusbar.grid(row=3, padx=10, sticky=(tk.W + tk.E)) # Place statusbar at the bottom, stretched across

    self.records_saved = 0

  def on_save(self):
    """Perform function when user clicks Save button."""
    
    # Check for errors in form; if there are, do not allow user to save
    errors = self.recordform.get_errors()
    if errors:
      self.status.set(
              "Cannot save, error in fields:\n{}".format(', '.join(errors.keys())))
      message = "Cannot save record"
      detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
      messagebox.showerror(title='Form Error', message=message, detail=detail)
      return False

    

    # For now, we save to a hardcoded filename with a datestring
    datestring = datetime.today().strftime("%Y-%m-%d")    # Create variable datestring in yyyy-mm-dd format
    filename = "abq_data_record_{}.csv".format(datestring)# Append the datestring to filename variable
    model = m.CSVModel(filename)     # Identify the model in model module and pass in filename
    
    # Get data from the DataEntryForm
    data = self.recordform.get()                          # Set values identified from record form in data variable

    # Save the record via the model module
    model.save_record(data)

    # Increment record saved message
    self.records_saved += 1
    self.status.set(
      "{} records saved this session".format(self.records_saved))
    self.recordform.reset()





























































