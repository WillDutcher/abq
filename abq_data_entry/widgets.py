import tkinter as tk
from tkinter import ttk
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .constants import FieldTypes as FT

##################
# Widget Classes #
##################

class ValidatedMixin:                   # Validation main class that other subclasses will base validations on
  """Adds a validation functionality to an input widget."""

  def __init__(self, *args, error_var=None, **kwargs): # Instantiate class and accept args, error_var, and kwargs
    """Instantiate class; takes arguments, error_var, and kwargs, if available."""
    self.error = error_var or tk.StringVar()  # Set self.error to error_var arg or make callable with StringVar()
    super().__init__(*args, **kwargs)         # Cause base class we mix with to execute its constructor

    # Set up validation
    vcmd = self.register(self._validate)      # If valid command, set as vcmd
    invcmd = self.register(self._invalid)     # If invalid command, set as invcmd

    self.config(validate='all',               # Validate on all event types
                validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),   # Pass all but %w substitution code
                invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d'))  # Pass all but %w substitution code

  def _toggle_error(self, on=False):                    # Function that will...(display change when error)
    """Display foreground color will change if there is an error."""
    self.config(foreground=('red' if on else 'black'))  # ...change text color red if error, otherwise black
  
  def _validate(self, proposed, current, char, event, index, action): # Validate function takes multiple arguments
    """Validate function; takes any of the above arguments."""
    self._toggle_error(False)     # Toggle off error on _validate call (innocent until proven guilty)
    self.error.set('')            # Clear error message
    valid = True                  # Set valid to True (innocent until proven guilty)
    if event == 'focusout':       # If user leaves widget...
      valid = self._focusout_validate(event=event)  # Set boolean value based on condition validate('focusout')
    elif event == 'key':          # If the event type is a key...
      valid = self._key_validate(proposed=proposed, # Set boolean value based on requisite called argument
          current=current, char=char, event=event,
          index=index, action=action)
    return valid                  # Return the boolean value, based on if it passes or fails validation

  def _focusout_validate(self, **kwargs): # On focusout, validate based on args provided
    """Function to validate information in widget on focusout event."""
    return True   # Focus events don't return anything usefl for any of the other args; no point in passing them

  def _key_validate(self, **kwargs): # On key event, validate based on args provided
    """Function to validate information in widget on key event."""
    return True # Key events return useful information in variety of ways
  
  def _invalid(self, proposed, current, char, event, index, action):
    """Perform function in event of invalid data entered in widget."""
    if event == 'focusout':   # If event type is focusout...
      self._focusout_invalid(event=event)   # Call _focusout_invalid function and set event argument to focusout
    elif event == 'key':  # If event type is a key event...
      self._key_invalid(proposed=proposed, current=current, # Call _key_invalid function, set args as appropriate
                           event=event, index=index, action=action)

  def _focusout_invalid(self, **kwargs):  # Function call when information is invalid on focusout...
    """If, on focusout, the information is determined to be invalid, set error to True."""
    self._toggle_error(True)              # Toggle the error to True and change text color

  def _key_invalid(self, **kwargs):       # Function call when information is invalid on key entry...
    """If, on key entry, the information is determined to be invalid, set error to True."""
    pass                                  # For invalid keys, we do nothing by default

  # Duplicating logic that occurs on focusout event: run validation function, if fail, run invalid handler
  def trigger_focusout_validation(self):  # Function manually called after text entered and user leaves widget
    """Manually run focusout checks since it effectively checks a completely entered value."""
    valid = self._validate('', '', '', 'focusout', '', '')  # Set boolean on if focusout validation passes or not
    if not valid:                               # If no valid status yet...
      self._focusout_invalid(event='focusout')  # ...call _focusout_invalid with argument of focusout
    return valid                                # Return boolean value of whether or not entered info is valid


class DateEntry(ValidatedMixin, ttk.Entry):     # Validation settings for Date field
  """Class to check validity of date entered in Date field."""

  def _key_validate(self, action, index, char, **kwargs):   # Validate key input
    """Function to validate keys within Date entry field."""
    valid = True                                            # "Innocent until proven guilty"

    if action == '0':                                       # If action is delete...
      valid = True                                          # valid is True
    elif index in ('0', '1', '2', '3', '5', '6', '8', '9'): # If index in range...
      valid = char.isdigit()                                # It is valid if the character is a digit
    elif index in ('4', '7'):                               # If index at 4 or 7...
      valid = char == '-'                                   # It is valid if the character is a hyphen (-)
    else:                                                   # Otherwise...
      valid = False                                         # It is NOT valid; valid is False
    return valid                                            # Return current valid boolean status

  def _focusout_validate(self, event):                      # Validate focusout event
    """Function to validate Entry field when focus is moved."""
    valid = True                                            # "Innocent until proven guilty"
    if not self.get():                                      # If the Entry field is empty...
      self.error.set('A value is required.')                # Instruct user information is required in this field
      valid = False                                         # Set valid to False until fixed
    try:                                                    # Try this...
      datetime.strptime(self.get(), '%Y-%m-%d')             # Get date value, check against format yyyy-mm-dd
    except ValueError:                                      # If user gets a ValueError...
      self.error.set('Invalid date.')                       # Instruct them the date is invalid
      valid = False                                         # Set valid to False until fixed
    return valid                                            # Return current valid boolean status


class RequiredEntry(ValidatedMixin, ttk.Entry): # Validation settings for Entry fields
  """Validation calls on information in Entry fields."""

  def _focusout_validate(self, event):
    """On focusout, validate the information."""
    valid = True            # Begin with assumption that the information is valid
    if not self.get():      # If the Entry field is empty...
      valid = False         # Set valid to False
      self.error.set('A value is required.')  # Instruct user that information is required in this field
    return valid            # Return valid status


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):  # Validation settings for Combobox field
  """Validation calls on information in Combobox fields."""
  
  def _key_validate(self, proposed, action, **kwargs):  # Method to test key input
    """Validation method for key input."""
    valid = True                # "Innocent until proven guilty"
    # If user tries to delete, clear the entire field
    if action == '0':           # If delete action...
      self.set('')              # Set the field to a cleared state
      return True               # Return a True boolean value
    
    # Logic to match proposed text to our values
    values = self.cget('values')          # Get values list; copied via .cget() method
    # Do a case-insensitve match against the entered text
    matching = [x for x in values if x.lower().startswith(proposed.lower())] # List of matching values
    if len(matching) == 0:      # If the matching list has 0 entries...
      valid = False             # Set valid to False
    elif len(matching) == 1:    # If there is 1 entry in matching list...
      self.set(matching[0])     # Match is made; set variable to that value
      self.icursor(tk.END)      # Send cursor to end of field using .icursor() method if match found
      valid = False             # Set valid to False (WHY??????)
    return valid                # Return valid boolean value

  def _focusout_validate(self, **kwargs):     # Function to validate focusout event
    """Focusout validation method."""
    valid = True                              # "Innocent until proven guilty"
    if not self.get():                        # If the Entry field is empty...
      valid = False                           # Set valid to False
      self.error.set('A value is required.')  # Instruct user information is required in this field
    return valid


class ValidatedSpinbox(ValidatedMixin, tk.Spinbox):     # Validation settings for Spinbox field
  """Validation calls on information in Spinbox fields."""
  
  def __init__(self, *args, min_var=None, max_var=None,   # Spinbox args taken in when instantiating this class
                   focus_update_var=None, from_='-Infinity',
                   to='Infinity', **kwargs):
    """Instantiate validation settings on Spinbox widget."""
    super().__init__(*args, from_=from_, to=to, **kwargs) # Take values from the tk.Spinbox widgets entered values
    # Save user from floating-point errors by using Decimal class
    self.resolution = Decimal(str(kwargs.get('increment', '1.0')))  # Get increment value from constructor args
    self.precision = self.resolution.normalize().as_tuple().exponent # Normalize number from resolution value

    # There should always be a variable or some of our code will fail
    self.variable = kwargs.get('textvariable') or tk.DoubleVar()    # Store variable
    
    if min_var:                                           # If there is a min_var identified...
      self.min_var = min_var                              # Store reference to min_var argument
      self.min_var.trace('w', self._set_minimum)          # Trace configured; points to appropriately-named method
    if max_var:                                           # If there is a max_var identified...
      self.max_var = max_var                              # Store reference to max_var argument
      self.max_var.trace('w', self._set_maximum)          # Trace configured; points to appropriately-named method
    self.focus_update_var = focus_update_var              # Store reference to focus_update_var argument
    self.bind('<FocusOut>', self._set_focus_update_var)   # Bind <FocusOut> event to method; will be used to update it

  def _set_focus_update_var(self, event):               # Internal method to get widget current value
    """Get widget's current value and, if focus_update_var present, set to same value."""
    value = self.get()                                  # Get widget's current value
    if self.focus_update_var and not self.error.get():  # If no error on widget and value is set...
      self.focus_update_var.set(value)                  # Set the value to the focus_update_var

  # Create callback for setting minimum value
  def _set_minimum(self, *args):                        # Internal method to set minimum value of spinbox
    """Set minimum value of spinbox."""
    current = self.get()                                # Set current variable to reference minimum value
    try:                                                # Try this...
      new_min = self.min_var.get()                      # Set a new variable to the current referenced minimum value
      self.config(from_=new_min)                        # Set the new_min value as the from_ value
    except (tk.TclError, ValueError):                   # If there is an error...
      pass                                              # Skip the error
    if not current:                                     # If the current value is not available...
      self.delete(0, tk.END)                            # Delete the value
    else:                                               # Otherwise...
      self.variable.set(current)                        # Set input variable to current value
    self.trigger_focusout_validation()                  # Method ends with call to another method to recheck value
                                                        # in field against the new minimum

  # Create callback for setting minimum value
  def _set_maximum(self, *args):                        # Internal method to set maximum value of spinbox
    """Set maximum value of spinbox."""
    current = self.get()                                # Set current variable to reference maximum value
    try:                                                # Try this...
      new_max = self.max_var.get()                      # Set a new variable to the current referenced maximum value
      self.config(to=new_max)                        # Set the new_min value as the from_ value
    except (tk.TclError, ValueError):                   # If there is an error...
      pass                                              # Skip the error
    if not current:                                     # If the current value is not available...
      self.delete(0, tk.END)                            # Delete the value
    else:                                               # Otherwise...
      self.variable.set(current)                        # Set input variable to current value
    self.trigger_focusout_validation()                  # Method ends with call to another method to recheck value
                                                        # in field against the new maximum

  def _key_validate(self, char, index, current, proposed, action, **kwargs):  # Method takes in several args
    """Validate key entry in Spinbox field."""
    valid = True                      # "Innocent until proven guilty"
    min_val = self.cget('from')       # Set min_val to value in from field
    max_val = self.cget('to')         # Set max_val to value in to field
    no_negative = min_val >= 0        # Set boolean value; True if min_val >= 0, otherwise False
    no_decimal = self.precision >= 0  # Set boolean value; True if self.precision >= 0, otherwise False

    if action == '0':                 # If user is deleting information...
      return True                     # Return True for _key_validate; Deletion should always work
    # First, filter out obviously invalid keystrokes
    if any([                          # If any of below conditions are met, keystrokes are bad
            (char not in ('-1234567890.')),                     # Valid characters are these
            (char == '-' and (no_negative or index != '0')),    # Hyphen only valid at index 0
            (char == '.' and (no_decimal or '.' in current))]): # decimal only valid if appears once
      return False                    # Return boolean False
    
    # At this point, proposed is either '-', '.', '-.', or a valid Decimal string
    if proposed in '-.':                  # If the value of proposed is in - or .
      return True                         # Return True
    
    # Proposed is a valid Decimal string; convert to Decimal and check more
    proposed = Decimal(proposed)      # Convert proposed to decimal
    proposed_precision = proposed.as_tuple().exponent

    if any([                                          # If any of these conditions are met...
            (proposed > max_val),                     
            (proposed_precision < self.precision)]):  # precision is given a negative value for decimal places
      return False                                    # If any scenario above is true, return False
    return valid                                      # valid status returned as safeguard if nothing yet returned

  def _focusout_validate(self, **kwargs):   # Method takes in args relevent to focusout
    """Method testing focusout."""
    valid = True                            # "Innocent until proven guilty"
    value = self.get()                      # set value to current status
    min_val = self.cget('from')             # Duplicate value in from field, set to min_val variable
    max_val = self.cget('to')               # Duplicate value in from field, set to max_val variable

    try:                                    # Try this...
      value = Decimal(value)                # Set the value to a decimal value
    except InvalidOperation:                # If exception InvalidOperation raised...
      self.error.set('Invalid number string: {}'.format(value))   # Set error message
      return False                          # Return False validation on focusout

    if value < min_val:                     # If the value is lower than expected minimum value...
      self.error.set('Value is too low (min {})'.format(min_val))   # Set error message
      valid = False                         # Set boolean valid value to False
    if value > max_val:                     # If the value is higher than expected maximum value...
      self.error.set('Value is too high (max {})'.format(max_val))  # Set error message
    return valid                            # Return valid status


##################
# Module Classes #
##################

class LabelInput(tk.Frame):             # Build class as subclass of tkinter Frame class
  """A widget containing a LABEL and its INPUT, together."""

  field_types = {
    FT.string: (RequiredEntry, tk.StringVar),
    FT.string_list: (ValidatedCombobox, tk.StringVar),
    FT.iso_date_string: (DateEntry, tk.StringVar),
    FT.long_string: (tk.Text, lambda: None),
    FT.decimal: (ValidatedSpinbox, tk.DoubleVar),
    FT.integer: (ValidatedSpinbox, tk.IntVar),
    FT.boolean: (ttk.Checkbutton, tk.BooleanVar)
  }

  def __init__(self, parent,            # Reference to parent widget
               label='',                # Text for the label part of widget
               input_class=None,   # Class of widget to create; default is Entry
               input_var=None,          # Tkinter variable to assign to input; optional
               input_args=None,         # Optional dictionary of add'l args for input constructor
               label_args=None,         # Optional dictionary of add'l args for label constructor
               field_spec=None,         # Dictionary of field specifications, if available
               **kwargs):               # Add'l kwargs passed to Frame constructor
    super().__init__(parent, **kwargs)  # Access to base class methods
    input_args = input_args or {}       # Ensure this is a dictionary
    label_args = label_args or {}       # Ensure this is a dictionary
    if field_spec:
      field_type = field_spec.get('type', FT.string)
      input_class = input_class or self.field_types.get(field_type)[0]
      var_type = self.field_types.get(field_type)[1]
      self.variable = input_var if input_var else var_type()
      # Min, Max, Increment
      if 'min' in field_spec and 'from_' not in input_args:
        input_args['from_'] = field_spec.get('min')
      if 'max' in field_spec and 'to' not in input_args:
        input_args['to'] = field_spec.get('max')
      if 'inc' in field_spec and 'increment' not in input_args:
        input_args['increment'] = field_spec.get('inc')
      # values
      if 'values' in field_spec and 'values' not in input_args:
        input_args['values'] = field_spec.get('values')
    else:
      self.variable = input_var           # Save reference to input variable as self.variable

    if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
      input_args["text"] = label              # This is the button's label; different than other input widgets
      input_args["variable"] = self.variable  # Set "variable" == whatever the passed input_var was set to
    else:
      self.label = ttk.Label(self, text=label, **label_args)  # Standard Label construction
      self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))  # Place label at 0, 0
      input_args["textvariable"] = self.variable              # Set "textvariable" so input can be manipulated

    self.input = input_class(self, **input_args)            # Call input class passed into Constructor with vars
    self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))  # Place input under the label
    self.columnconfigure(0, weight=1)                       # Fills entire widget column

    self.error = getattr(self.input, 'error', tk.StringVar())
    self.error_label = ttk.Label(self, textvariable=self.error, foreground="maroon")
    self.error_label.grid(row=2, column=0, sticky=(tk.W + tk.E))

  def grid(self, sticky=(tk.E + tk.W), **kwargs):   # Set up layout to auto-place, as appropriate
    super().grid(sticky=sticky, **kwargs)           # Call from parent widget grid information and any kwargs

  def get(self):                              # Get the value in the input box
    try:                                      # Try this; throw exception if error
      if self.variable:                       # If there is a value in the input box...
        return self.variable.get()            # Get that value and return it
      elif type(self.input) == tk.Text:       # If the inpub box is a Text box...
        return self.input.get('1.0', tk.END)  # Get the value from the first char to end
      else:                                   # Otherwise...
        return self.input.get()               # Return the value assigned to class widget value
    except (TypeError, tk.TclError):          # Happens when numeric fields are empty
      return ''                               # Return blank string

  def set(self, value, *args, **kwargs):        # Pass request to variable or widget
    if type(self.variable) == tk.BooleanVar:    # If it's True or False...
      self.variable.set(bool(value))            # Set 'variable' to passed True or False value
    elif self.variable:                         # Otherwise, if there is an identified variable listed...
      self.variable.set(value, *args, **kwargs) # Set variable to passed value with any other args or kwargs
    elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):  # If the input is Checkbutton or Radiobutton...
      if value:                                 # If a no variable but button-style class...
        self.input.select()                     # Use select method to select button value
      else:                                     # Otherwise...
        self.input.deselect()                   # Use deselect method to deselect button value
    elif type(self.input) == tk.Text:           # If the input type is a Text box...
      self.input.delete('1.0', tk.END)          # Delete all the existing text
      self.input.insert('1.0', value)           # Insert whatever is entered into value variable
    else:                                       # This input must be an Entry-type widget with no variable
      self.input.delete(0, tk.END)              # Use delete method to clear current value
      self.input.insert(0, value)               # Enter the appropriate value identified in value variable
