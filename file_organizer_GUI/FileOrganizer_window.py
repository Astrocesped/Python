#!/usr/bin/python
"""
FileOrganizer_window.py: Creates the interface's main window.
                         Contains subclasses of Qt/PySide's widgets and
                         related utility functions.
"""
__author__ = "Carlos Montes"

from os.path import expanduser
import FileOrganizer
from FileOrganizer_utils import (QtGui, QtCore, Signal,
                                 norm_pathname,
                                 retrieve_directory_content)

# --------- CLASSES AND SUBCLASSES ----------

class FileOrganizerWindow(QtGui.QMainWindow):
    """
    Main QtGui window of the package.
    """

    def __init__(self):
        # Standard reference to QtGui.QMainWindow"s __init__
        super(FileOrganizerWindow, self).__init__()

        # Create and set the container"s central widget of the window
        main_container = QtGui.QWidget(self)
        self.setCentralWidget(main_container)

        # Horizontal container of all the layouts in the window
        main_layout = QtGui.QHBoxLayout()

        # --------- LEFT SIDE FOLDER (ORIGIN) ---------

        # Horizontal layout for the origin folder
        left_side_layout = QtGui.QVBoxLayout()

        # Origin folder label
        origin_label = new_label("Origin Folder", 10, bold=True)

        # Browse origin folder textbox and button
        browse_origin_layout = QtGui.QHBoxLayout()
        self.browse_textbox1 = BrowserTextbox()
        self.browse_button1 = new_button("Browse", 8)

        # Toggle All button (Origin folder)
        check_origin_layout = QtGui.QHBoxLayout()
        self.toggle_all_left = new_checkbox("Toggle All Files")

        # Directory content list
        self.origin_content = DirectoryContentList()

        # Fill the origin_content list with the user's Home content
        # which will differ with the right side in that it's checkable
        self.origin_content.populate_list(retrieve_directory_content(
                                          expanduser("~")), True)

        # Set the content of the origin textbox to Home too
        self.browse_textbox1.setText(norm_pathname(expanduser("~")))

        # --------- RIGHT SIDE FOLDER (DESTINATION) ---------

        # Horizontal layout for the destination folder
        right_side_layout = QtGui.QVBoxLayout()

        # Destination folder label
        destination_label = new_label("Destination Folder", 10, True)

        # Browse origin folder text and button
        browse_destination_layout = QtGui.QHBoxLayout()
        self.browse_textbox2 = BrowserTextbox(left_side=False)
        self.browse_button2 = new_button("Browse", 8)

        destination_content_label = new_label("Current Files:", 9)

        # Destination directory content list
        self.destination_content = DirectoryContentList()

        # Fill the Destination Content list with the script's location
        self.destination_content.populate_list(retrieve_directory_content(
                                               norm_pathname()), False)

        # Set the content of the destination textbox to getcwd() too
        self.browse_textbox2.setText(norm_pathname())

        # Options layout
        options_layout = QtGui.QVBoxLayout()

        # Pre-order Frame and Layout
        order_frame = new_frame(main_container, "preorder_frame", raised=True)
        order_layout = QtGui.QVBoxLayout()
        order_label = new_label("Pre-Order By:", 9, True)

        # Pre-order's Radio Button Group
        self.button_group = QtGui.QButtonGroup(self)

        # Pre-order Radio options (layout, button and label for each)
        # Set an incremental id for each radio button
        abc_layout = QtGui.QHBoxLayout()
        abc_radio = QtGui.QRadioButton()
        abc_radio.setChecked(True)
        self.button_group.addButton(abc_radio)
        self.button_group.setId(abc_radio, 0)
        abc_label = new_label("A - Z", 8)

        zyx_layout = QtGui.QHBoxLayout()
        zyx_radio = QtGui.QRadioButton()
        self.button_group.addButton(zyx_radio)
        self.button_group.setId(zyx_radio, 1)
        zyx_label = new_label("Z - A", 8)

        date_layout = QtGui.QHBoxLayout()
        date_radio = QtGui.QRadioButton()
        self.button_group.addButton(date_radio)
        self.button_group.setId(date_radio, 2)
        date_label = new_label("Creation Date", 8)

        custom_layout = QtGui.QHBoxLayout()
        custom_radio = QtGui.QRadioButton()
        custom_layout.addStretch(1)
        self.button_group.addButton(custom_radio)
        self.button_group.setId(custom_radio, 3)
        self.custom_combo = new_combo(("Detect numbers after this pattern:",
                                       "Detect numbers before this pattern:"))
        self.custom_textbox = new_line_edit(120)

        # Rename Frame
        rename_frame = new_frame(main_container, "rename_frame", raised=True)
        rename_layout = QtGui.QVBoxLayout()
        rename_label = new_label("Rename Pattern (Optional):", 9, True)

        # Rename Frame's widgets
        numbering_layout = QtGui.QHBoxLayout()
        self.numbering_check = new_checkbox("Insert numeration with ")
        self.numbering_digits = new_line_edit(40)
        self.numbering_digits.setText("4")
        numbering_label = new_label("digits", 9)
        self.numbering_combo = new_combo(("after this string:",
                                          "before this string:"))
        self.numbering_rename = new_line_edit(120)

        remove_layout = QtGui.QHBoxLayout()
        self.remove_check = new_checkbox("Remove the following characters: ")
        self.remove_textbox = new_line_edit(80)

        lowercase_layout = QtGui.QHBoxLayout()
        self.lowercase_check = new_checkbox("Transform to lowercase")

        # Process options combo
        self.duplicate_check = new_checkbox("Duplicate files instead")

        # Replace existing files checkbox
        self.replace_files = new_checkbox("Avoid replacing existing files")

        # Move Files button
        self.apply_button = new_button("Move Files", 10, 350)

        # --------- CONNECTIONS AND SIGNALS ---------

        # Origin folder Browse button connection
        self.connect(self.browse_button1, Signal("clicked()"),
                     self.file_dialog1)

        # Destination folder Browse button connection
        self.connect(self.browse_button2, Signal("clicked()"),
                     self.file_dialog2)

        # Origin folder's "Toggle All" checkbox connection
        self.connect(self.toggle_all_left, Signal("clicked()"),
                     self.toggle_origin_items)

        # Move Files button signal connection
        self.connect(self.apply_button, QtCore.SIGNAL("clicked()"),
                     self.move_files)

        # --------- LAYOUTS ---------

        # Origin folder's layout
        left_side_layout.addWidget(origin_label)
        add_space(left_side_layout, 0, 10)

        browse_origin_layout.addWidget(self.browse_textbox1)
        add_space(browse_origin_layout, 15, 0)
        browse_origin_layout.addWidget(self.browse_button1)
        add_space(browse_origin_layout, 15, 0)
        left_side_layout.addLayout(browse_origin_layout)
        add_space(left_side_layout, 0, 10)

        check_origin_layout.addWidget(self.toggle_all_left)
        check_origin_layout.setAlignment(QtCore.Qt.AlignLeft)
        left_side_layout.addLayout(check_origin_layout)
        add_space(left_side_layout, 0, 10)

        left_side_layout.addWidget(self.origin_content)

        main_layout.addLayout(left_side_layout)

        # Destination folder's layout
        right_side_layout.addWidget(destination_label)
        add_space(right_side_layout, 0, 10)

        browse_destination_layout.addWidget(self.browse_textbox2)
        add_space(browse_destination_layout, 15, 0)
        browse_destination_layout.addWidget(self.browse_button2)
        add_space(browse_destination_layout, 15, 0)
        right_side_layout.addLayout(browse_destination_layout)
        add_space(right_side_layout, 0, 10)

        right_side_layout.addWidget(destination_content_label)
        add_space(right_side_layout, 0, 10)
        right_side_layout.addWidget(self.destination_content)

        # Options' layout
        options_vbox = QtGui.QVBoxLayout()

        # Pre-Order Layout
        order_layout.addWidget(order_label)
        abc_layout.addWidget(abc_radio)
        abc_layout.addWidget(abc_label)
        abc_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(order_layout, 0, 5)
        order_layout.addLayout(abc_layout)

        zyx_layout.addWidget(zyx_radio)
        zyx_layout.addWidget(zyx_label)
        zyx_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(order_layout, 0, 5)
        order_layout.addLayout(zyx_layout)

        date_layout.addWidget(date_radio)
        date_layout.addWidget(date_label)
        date_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(order_layout, 0, 5)
        order_layout.addLayout(date_layout)

        custom_layout.addWidget(custom_radio)
        custom_layout.addWidget(self.custom_combo)
        custom_layout.addWidget(self.custom_textbox)
        custom_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(order_layout, 0, 5)
        order_layout.addLayout(custom_layout)

        order_frame.setLayout(order_layout)
        add_space(options_vbox, 0, 20)
        options_vbox.addWidget(order_frame)

        # Rename Frame's Layout
        rename_layout.addWidget(rename_label)

        numbering_layout.addWidget(self.numbering_check)
        numbering_layout.addWidget(self.numbering_digits)
        numbering_layout.addWidget(numbering_label)
        numbering_layout.addWidget(self.numbering_combo)
        numbering_layout.addWidget(self.numbering_rename)
        numbering_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(rename_layout, 0, 10)
        rename_layout.addLayout(numbering_layout)

        remove_layout.addWidget(self.remove_check)
        remove_layout.addWidget(self.remove_textbox)
        remove_layout.addStretch(1)
        remove_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(rename_layout, 0, 10)
        rename_layout.addLayout(remove_layout)

        lowercase_layout.addWidget(self.lowercase_check)
        lowercase_layout.setAlignment(QtCore.Qt.AlignLeft)
        add_space(rename_layout, 0, 10)
        rename_layout.addLayout(lowercase_layout)

        rename_layout.setAlignment(QtCore.Qt.AlignLeft)
        rename_frame.setLayout(rename_layout)
        add_space(options_vbox, 0, 20)
        options_vbox.addWidget(rename_frame)
        add_space(options_vbox, 0, 20)

        # Additional Options' addition to layout
        options_vbox.addWidget(self.duplicate_check)
        add_space(options_vbox, 0, 5)
        options_vbox.addWidget(self.replace_files)
        add_space(options_vbox, 0, 15)
        options_vbox.addWidget(self.apply_button)
        options_vbox.setAlignment(QtCore.Qt.AlignTop)

        # Add each of the elements with a separation of 20 pixels
        # between them; add a line between them
        add_space(main_layout, 20, 0)
        main_layout.addWidget(add_line(200))
        add_space(main_layout, 20, 0)
        main_layout.addLayout(right_side_layout)
        add_space(main_layout, 20, 0)
        main_layout.addWidget(add_line(200))
        add_space(main_layout, 20, 0)
        main_layout.addLayout(options_vbox)

        # Add the main Window's StatusBar for warnings
        self.status_label = new_label("", 8)
        self.statusBar().addPermanentWidget(self.status_label)

        main_container.setLayout(main_layout)
        self.setWindowTitle("File Organizer")
        self.setObjectName("fileorganizerUI")

    # --------- CALLBACK FUNCTIONS -----------

    def file_dialog1(self):
        """
        Opens QFileDialog for the Origin Folder's Browse button.
        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
               norm_pathname(self.browse_textbox1.text()),
               QtGui.QFileDialog.ShowDirsOnly)

        if path:
            self.browse_textbox1.setText(path)
            self.origin_content.populate_list(retrieve_directory_content(path), True)

    def file_dialog2(self):
        """
        Opens QFileDialog for the Destination Folder's Browse button.
        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
               norm_pathname(self.browse_textbox2.text()),
               QtGui.QFileDialog.ShowDirsOnly)

        if path:
            self.browse_textbox2.setText(path)
            self.destination_content.populate_list(retrieve_directory_content(path), False)

    def move_files(self):
        """
        Callback function that invokes FileOrganizer's move_files function
        """

        # Skip the first two spaces displayed in each filename of the
        # Destination directory. Only consider the checked items
        origin_filenames = [self.origin_content.model.item(i).text()[2:] for i
                            in range(self.origin_content.model.rowCount())
                            if self.origin_content.model.item(i).checkState()]

        try:
            FileOrganizer.move_files(self.browse_textbox1.text(),
                                     origin_filenames,
                                     self.browse_textbox2.text(),
                                     self.button_group.checkedId(),
                                     (self.custom_combo.currentIndex(),
                                     self.custom_textbox.text()),
                                     (self.numbering_check.isChecked(),
                                     self.numbering_digits.text(),
                                      self.numbering_combo.currentIndex(),
                                      self.numbering_rename.text()),
                                     (self.remove_check.isChecked(),
                                      self.remove_textbox.text()),
                                     self.lowercase_check.isChecked(),
                                     self.duplicate_check.isChecked(),
                                     self.replace_files.isChecked())

        except FileOrganizer.NoSelectedFiles:
            self.status_label.setText("No selected files to move!")
            return

        # Refill the ListViews with their new file content after
        # the last operation
        self.origin_content.populate_list(retrieve_directory_content(
            self.browse_textbox1.text()), True)
        self.destination_content.populate_list(retrieve_directory_content(
            self.browse_textbox2.text()), False)

        # Set the Toggle All Checkbox Off too
        self.toggle_all_left.setChecked(False)

        # Update the status bar
        self.status_label.setText("Moved files from {} to {}".format(
            self.browse_textbox1.text(), self.browse_textbox2.text()))

    def toggle_origin_items(self):
        """
        Checks or unchecks all of the origin folder list's items at once.
        """
        check_state = {
            True: QtCore.Qt.Checked,
            False: QtCore.Qt.Unchecked
        }[self.toggle_all_left.isChecked()]

        # Travel through each item and check or uncheck it
        [self.origin_content.model.item(i).setCheckState(check_state)
         for i in range(self.origin_content.model.rowCount())]


class BrowserTextbox(QtGui.QLineEdit):
    """
    Create a customizable QLineEdit that reacts to a click
    by opening a QFileDialog.
    """

    def __init__(self, left_side=True):
        """
        Initializes the Custom QlineEdit.
        :param left_side: Boolean that allows differentiation between widgets,
        so that the corresponding one can have its contents modified
        """

        super(BrowserTextbox, self).__init__()
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setReadOnly(True)
        self.setMinimumWidth(200)
        self.setMaximumHeight(28)
        self.setStyleSheet("background-color:#AAAAAA; border:none;")
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

        self.left_side = left_side

    def mousePressEvent(self, event):
        """
        Override the QLineEdit's normal Mouse Press Event
        """
        path = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
                norm_pathname(self.text()), QtGui.QFileDialog.ShowDirsOnly)

        # If a path was defined, set the corresponding textbox with that path
        if path:
            self.setText(path)

            # Also fill the corresponding ListView with the directory content
            if self.left_side:
                self.parent().parent().origin_content.populate_list(
                    norm_pathname(path), True)
            else:
                self.parent().parent().destination_content.populate_list(
                    norm_pathname(path), False)


class DirectoryContentList(QtGui.QListView):
    """
    Custom QListView that displays the file content of the chosen directory.
    """

    def __init__(self):
        """
        Initializaes the ListView; sets an StandardItemModel.
        """
        super(DirectoryContentList, self).__init__()

        self.setMinimumHeight(450)
        self.setStyleSheet("background-color:#AAAAAA;")
        self.model = QtGui.QStandardItemModel(self)
        self.setModel(self.model)

    def populate_list(self, files, checkable):
        """
        Fills the ListView with the passed list of files.
        :param files: List of filenames to populate the view
        :param checkable: Boolean for the item to have a checkbox beside
        :return: None
        """
        # Clear the ListView's model first
        self.model.clear()

        # Create a new QStandardItem for each filename
        for filename in files:
            self.model.appendRow(self.new_item(filename, checkable))

    def new_item(self, name, checkable):
        """
        Create a new QStandardItem for the model.
        :param files: Text to display
        :param checkable: Boolean for the item to be checkable
        """
        item = QtGui.QStandardItem("  " + name)
        item.setCheckable(checkable)
        item.setSizeHint(QtCore.QSize(0, 40))
        return item

# ------ UTILITY WIDGET FUNCTIONS ---------

def add_space(layout, x, y):
    """
    Add a spacer in the window"s layouts
    :param layout: Layout where the spacer will be added
    :param x: Width of spacer
    :param y: Height of spacer
    :return: None
    """
    spacer = QtGui.QSpacerItem(x, y)
    layout.addSpacerItem(spacer)

def add_line(length):
    """
    Return a thick line to add in the layouts
    :param length: Length of the line
    :return: QFrame in the form of a line
    """
    line = QtGui.QFrame()
    line.setMinimumHeight(length)
    line.setGeometry(QtCore.QRect(0, 0, 0, length))
    line.setObjectName("line")
    line.setStyleSheet("#line { border: 2px solid #555555; }")
    line.setFrameShape(QtGui.QFrame.VLine)
    return line

def new_button(text, font_size=None, length=None):
    """
    Returns a new button
    :param text: Text that the button will contain
    :param font_size: Optional Font size of the button"s text
    :return: QPushButton
    """
    button = QtGui.QPushButton("  " + text + "  ")
    button.setStyleSheet("background-color:#444444; color:#CCCCCC;")
    button.setFixedHeight(30)
    if font_size is not None:
        font = QtGui.QFont()
        font.setPointSize(font_size)
        button.setFont(font)
    if length is not None:
        button.setFixedWidth(length)
    return button

def new_checkbox(text):
    """
    Return a new Checkbox
    :param text: Text that will accompany the checkbox
    :return: QCheckbox
    """
    checkbox = QtGui.QCheckBox(text)
    checkbox.setStyleSheet("color:#EEEEEE;")

    cb_palette = checkbox.palette()
    cb_palette.setColor(QtGui.QPalette.Base, QtCore.Qt.gray)
    checkbox.setPalette(cb_palette)

    return checkbox

def new_combo(items):
    combo = QtGui.QComboBox()
    combo.setStyleSheet("background-color:#444444; color:#CCCCCC;")
    combo.setFixedHeight(35)
    for item in items:
        combo.addItem(item)
    return combo

def new_frame(parent, name, raised=False, fixed_size=True):
    """
    Create a QFrame instance.
    :param parent: Parent QWidget instance
    :param name: Name of the QFrame instance
    :param raised: Style the frame as a raised box
    :param fixed_size: Keep the same width and height?
    :return: QFrame instance
    """
    frame = QtGui.QFrame(parent)
    frame.setObjectName(name)
    frame.setStyleSheet("#{0} {{ border: 2px solid #555555; }}".format(name))

    if raised:
        frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
    if fixed_size:
        frame.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    return frame

def new_label(text, size, bold=False):
    """
    Return a new QLabel
    :param text: Text that will be contained by the label
    :param size: Size of the label"s text
    :param color: Color of the label"s text
    :param bold: Boolean that tells whether to bold the label or not
    :return: QLabel
    """
    label = QtGui.QLabel(text)
    label.setStyleSheet("color:#CCCCCC;")
    label.setAlignment(QtCore.Qt.AlignCenter)

    font = QtGui.QFont()
    font.setPointSize(size)
    if bold:
        font.setBold(bold)
    label.setFont(font)
    return label

def new_line_edit(size, readonly=False):
    """
    Return a new QLineEdit with standard styling
    :param size: Width of the textbox
    :param readonly: Boolean that tells whether to make it non-modifiable
    :return:
    """
    textbox = QtGui.QLineEdit()
    textbox.setMaximumWidth(size)
    textbox.setFixedHeight(25)
    textbox.setStyleSheet("background-color:#AAAAAA; border:none;")
    textbox.setReadOnly(readonly)
    textbox.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    return textbox

def main():
    # Show the main window instance
    app = QtGui.QApplication([])
    ex = FileOrganizerWindow()

    # Change the window"s background color
    background_palette = ex.palette()
    background_palette.setColor(ex.backgroundRole(), QtGui.QColor(60, 60, 60))
    ex.setPalette(background_palette)
    ex.show()

    app.exec_()

if __name__ == "__main__":
    main()
