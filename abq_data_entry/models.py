import csv
import os
from .constants import FieldTypes as FT

class CSVModel:
  """CSV file storage."""

  fields = {
    "Date": {'req': True, 'type': FT.iso_date_string},
    "Time": {'req': True, 'type': FT.string_list, 'values': ['08:00', '12:00', '16:00', '20:00']},
    "Technician": {'req': True, 'type': FT.string},
    "Lab": {'req': True, 'type': FT.string_list, 'values': ['A', 'B', 'C', 'D', 'E']},
    "Plot": {'req': True, 'type': FT.string_list, 'values': [str(x) for x in range(1, 21)]},
    "Seed sample": {'req': True, 'type': FT.string},
    "Humidity": {'req': True, 'type': FT.decimal, 'min': 0.5, 'max': 52.0, 'inc': .01},
    "Light": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 100.0, 'inc': .01},
    "Temperature": {'req': True, 'type': FT.decimal, 'min': 4, 'max': 40, 'inc': .01},
    "Equipment Fault": {'req': True, 'type': FT.boolean},
    "Plants": {'req': True, 'type': FT.integer, 'min': 0, 'max': 20},
    "Blossoms": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Fruit": {'req': True, 'type': FT.integer, 'min': 0, 'max': 1000},
    "Minimum Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
    "Maximum Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
    "Median Height": {'req': True, 'type': FT.decimal, 'min': 0, 'max': 1000, 'inc': .01},
    "Notes": {'req': True, 'type': FT.long_string}
  }

  def __init__(self, filename):
    """Allows passage of a filename."""
    self.filename = filename    # Takes filename parameter and stores it as a property

  def save_record(self, data):
    """Save a dict of data to the CSV file."""
    newfile = not os.path.exists(self.filename)
    with open(self.filename, 'a') as fh:
      csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
      if newfile:
        csvwriter.writeheader()
      csvwriter.writerow(data)
