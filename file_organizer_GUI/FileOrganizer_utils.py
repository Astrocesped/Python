""""
FileOrganizer_utils.py: Provides utilities for the GUI package.
                        Mainly imports either PySide or PyQt4 in order
                        to display a GUI for the user, along with logging
                        and other utility functions.
"""

try:
    # GUI namespaces pulled from PySide, if present in the system.
    # based on Robert Galanakis' "Practical Maya Programming with Python"
    # available at https://books.google.ca/books?id=ESAZBAAAQBAJ

    from PySide import QtCore, QtGui
    import shiboken

    # Signal class aliases the PySide.QtCore.Signal class
    Signal = QtCore.SIGNAL

except ImportError:
    # Namespaces pulled from PyQt implementation, in the absence of PySide
    from PyQt4 import QtCore, QtGui
    import sip

    # Signal class aliases the PyQt4.QtCore.pyqtSignal class
    Signal = QtCore.SIGNAL

import os
import logging

# ------- UTILITY FUNCTIONS ----------

def norm_pathname(pathname=""):
    """
    Normalize a pathname; if no pathname is passed, return current directory.
    :param pathname: Pathname to be normalized
    :return: String containing pathname
    """
    if not pathname:
        return os.path.normpath(os.getcwd())
    else:
	# Convert QString to str to avoid posix difficulties
        return os.path.normpath(str(pathname))

def retrieve_directory_content(directory):
    """
    Retrieves and sorts the filenames inside a specified directory.
    :param directory: Normalized pathname of a directory
    :return: List of filenames (directories skipped)
    """
    # Convert directory to explicit str, to avoid posixpath complications
    directory = str(directory)

    content = [f for f in os.listdir(directory)
               if os.path.isfile(os.path.join(directory, f))]
    content.sort()
    return content

def sort_list(lst, pairs=False, rev=False):
    """
    Sorts a list and returns it.
    :param lst: List to sort and return
    :param pairs: Boolean that tells if the list contains tuples
    that will contain a first value with purposes of ordering
    :param rev: Boolean that tells whether to reverse sort the list
    :return: List
    """
    lst.sort(reverse=rev)
    if pairs:
        return [filename for organizer, filename in lst]
    else:
        return lst
