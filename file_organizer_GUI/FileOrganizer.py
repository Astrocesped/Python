"""
FileOrganizer.py: Provides main function to move, order and rename files.
                  To be invoked by FileOrganizer_window.
"""
__author__ = "Carlos Montes"

import os
from stat import ST_CTIME
from time import localtime
from shutil import copyfile as shutil_copyfile
from FileOrganizer_utils import sort_list

def move_files(origin, files, destination, id_order, custom_preorder,
               numbering, removing, lowercase=False, duplicate=False,
               replace_files=False):
    """
    Moves or duplicates files from one directory to another.
    :param origin: Directory from which the files are moved/duplicated
    :param files: Filenames of the items to be moved
    :param destination: Pathname to contain the specified files
    :param id_order: Pre-ordering (0: alphabetical, 1: inverse alpha,
    2: creation order, 3: string of numbers before/after pattern)
    :param custom_preorder:  Tuple of pair (Int before/after pattern,
    String pattern)
    :param numbering: Tuple of pattern (Boolean to actually rename with
    numbers, number of digits for the renaming, 0: after 1: before the
    custom pattern, string containing the custom pattern)
    :param removing: Tuple containing boolean to determine if to replace or
    not and the characters to be removed from the filenames
    :param lowercase: Boolean for whether to transform filenames to lowercase
    :param duplicate: Boolean for whether to move or duplicate the files
    :param replace_files: Boolean for whether to overwrite in destination
    :return: None
    """

    # ------ UTILITY CLOSURES ---------

    def replace_lower(string):
        """
        Modifies the final name of a file according to the 'replace
        characters' and 'lowercase' options.
        :param string: String to be modified
        :return: Modified string
        """

        return_string = ""

        if removing[0] and lowercase:
            # The string has to have the specified characters out
            # before making it lowercase
            temp_string = ""
            for character in removing[1]:
                temp_string = string.replace(character, "")
            return_string = temp_string.lower()

        elif removing[0] and removing[1]:
            for character in removing[1]:
                return_string = string.replace(character, "")

        elif lowercase:
            return_string = string.lower()

        else:
            # No change at all
            return_string = string

        return return_string

    def move_file(origin_name, destination_name):
        """
        Moves or duplicates a file into a destination directory. Deletes
        a file in the destination if replace_files is True. Otherwise, avoids
        the operation in case the filename already exists.
        :param origin_name: File's original name
        :param destination_name: Name of the file in its new directory
        :return: None
        """

        # Create the name of the file in its new directory
        # Take care of removing or lowercase transformation if desired
        final_pathname = os.path.join(destination,
                                      replace_lower(destination_name)
                                      if removing[0] or lowercase
                                      else destination_name)

        # If files should be replaced, get rid of any file
        # that already has the same name in the destination folder
        if replace_files and os.path.exists(final_pathname):
            os.remove(final_pathname)

        # If the files should not be deleted from the original folder,
        # use shutil_copyfile to move the file; don't try if file exists
        if duplicate and not os.path.exists(final_pathname):
            shutil_copyfile(os.path.join(origin, origin_name), final_pathname)

        # Else, if the files are to be moved and the filename doesn't
        # already exist in the destination folder, move with os' rename
        elif not os.path.exists(final_pathname):
            os.rename(os.path.join(origin, origin_name), final_pathname)

    # ------ END OF UTILITY CLOSURES ---------

    if not files:
        # No files were checked; abort
        raise NoSelectedFiles("No files selected to move in origin folder")

    # Check pre-order to apply before moving/renaming the files
    if id_order == 0:
        # Pre-order alphabetically
        original_files = sort_list(files)

    elif id_order == 1:
        # Pre-rder reverse alphabetically
        original_files = sort_list(files, rev=True)

    elif id_order == 2:
        # Order by creation time
        # List comprehension of tuples containing creation time, name of file
        c_times = [(localtime(os.stat(os.path.join(origin, f))[ST_CTIME]), f)
                   for f in files]

        # Sort filenames by creation time
        original_files = sort_list(c_times, pairs=True)

    else:
        # Pre-order by a number found after/before a pattern in the filenames
        pattern = custom_preorder[1]
        list_to_order = []

        for f in files:
                # If there is no defined pattern, maybe the name of the files
                # themselves is just a number... Take the name until its
                # extension suffix period
                if not pattern:
                    try:
                        file_tuple = (int(f[:f.find(".")]), f)

                    except ValueError:
                        # Well, this file doesn't follow what we expected..
                        # Improvise with a simple 0 in the first tuple value
                        file_tuple = (0, f)

                # If the number pattern is before the specified string:
                elif custom_preorder[0]:
                    # Create a tuple with the number of the file and its name.
                    # Number determined from start of name to pattern location
                    try:
                        file_tuple = (int(f[:f.find(pattern)]), f)

                    except ValueError:
                        # The file does not follow the pattern, improvise
                        file_tuple = (0, f)

                else:
                    # Number determined from pattern location to period before
                    # the file extension
                    try:
                        file_tuple = (int(f[f.find(pattern)+len(pattern):
                                            f.find(".")]), f)

                    except ValueError:
                        file_tuple = (0, f)

                list_to_order.append(file_tuple)

        original_files = sort_list(list_to_order, pairs=True)

    # If the new filenames will follow a prefixed/suffixed number pattern
    # then create their names according to the ordered original_files
    if numbering[0]:

        try:
            # Create a format string with the number of digits
            digits = "{{:0{}d}}".format(int(numbering[1]))
        except ValueError:
            # Just put a default of four digits
            digits = "{{:04d}}"

        for i, f in enumerate(original_files):
            # If the user checked the numeration checkbox but inserted no
            # pattern, maybe they just want the number to be the filename
            if not numbering[3]:
                move_file(f, "{}{}".format(digits.format(i), f[f.rfind("."):]))

            # If the numbering pattern should go after the custom pattern,
            # name should be: custom pattern, digits, extension
            elif numbering[2] == 0:
                move_file(f, "{}{}{}".format(numbering[3],
                                             digits.format(i),
                                             f[f.rfind("."):]))

            # But if the numbering pattern should go before the custom pattern
            # the new name should be: digits, custom pattern, extension
            else:
                move_file(f, "{}{}{}".format(digits.format(i),
                                             numbering[3],
                                             f[f.rfind("."):]))

    # Else there is not a special numbering pattern to rename the files with
    else:
        # Move or duplicate the files with their same original name
        # (although maybe with lowercase and replace options, if so desired)
        for f in original_files:
            move_file(f, f)

class NoSelectedFiles(Exception):
    " Custom Exception to Raise and fill the Status Bar. "
    pass
