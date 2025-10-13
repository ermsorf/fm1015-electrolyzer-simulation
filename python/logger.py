from typing import Optional
import csv
import os
from warnings import warn

def csv_check(filepath: str):
    """makes sure filename ends with .csv"""
    if not filepath.endswith(".csv"):
        filepath += ".csv"
    return filepath

def clear_logs(filepath: str = "logged_state"):
    """
    Delete browser hist- erm i mean delete contents of log file.
    """
    filepath = csv_check(filepath)
    with open(filepath, "w"): pass

def verify_file_exists(filepath):
    """create file if it is not made already"""
    if not os.path.exists(filepath):
        clear_logs(filepath) # clearing also creates the file

def read_headers(filepath):
    """return a list of the header names"""
    filepath = csv_check(filepath)
    verify_file_exists(filepath)
    with open(filepath, "r", newline='') as file:
        reader = csv.reader(file)
        lines = list()
        for line in reader:
            lines.append(line)
        if len(lines) == 0:
            return lines
        return lines[0]

def log_state(state: dict, filepath: str = "logged_state"):
    """Append state to the log file specified by filepath"""
    filepath = csv_check(filepath)
    verify_file_exists(filepath)
    with open(filepath, "r+", newline='') as file:
        # r+: read file first to see if headers are added
        # then: file pointer at end of file --> equivalent to 'a'
        # --> writing begins at end of file
        headers_just_written = False
        writer = csv.writer(file)
        if file.read() == "":
            writer.writerow(sorted(state.keys()))
            headers_just_written = True
        # Sort values by key to standardize order, then extract values
        # TODO there should be some smarter way to do this
        items = sorted(state.items())
        values = list()
        for item in items: 
            _, value = item
            values.append(value)
        if len(values) != len(read_headers(filepath)) and not headers_just_written:
            warn("there are missing values!")
        writer.writerow(values)
        
def read_logs(filepath: str = "logged_state"):
    """return a dict with all the logs in filepath."""
    filepath = csv_check(filepath)
    logs = dict()
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        lines = list()
        for line in reader:
            lines.append(line)
    headers = lines.pop(0)
    for i, header in enumerate(headers):
        column = list()
        for line in lines:
            column.append(line[i])
        logs[header] = column
    return logs

if __name__ == "__main__":
    clear_logs()
    for i in range(3):
        state = {"c": 1+i, "halge": 2+i, "a": 3+i}
        log_state(state)
    print(read_logs())