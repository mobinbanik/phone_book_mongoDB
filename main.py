"""Phonebook application."""
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget,
    QTableWidgetItem, QDockWidget, QFormLayout,
    QLineEdit, QWidget, QPushButton,
    QToolBar, QMessageBox, QLabel,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
import sys
import database


class Table(QTableWidget):
    def __init__(self, row=1, col=5, parent=None):
        super().__init__(parent)
        self.setColumnCount(col)
        self.setRowCount(row)
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 0)
        # Fill table title
        self.setHorizontalHeaderLabels([
            "First Name", "Last Name", "Phone", "Address"
        ])

    def update_data(self, data=None):
        self.setRowCount(0)
        row = 0
        if data is not None:
            for contact in data:
                self.add_row(row, contact)
                row += 1
        else:
            for contact in database.get_contacts():
                self.add_row(row, contact)
                row += 1

    def add_row(self, row: int, contact: dict) -> None:
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(contact["First Name"]))
        self.setItem(row, 1, QTableWidgetItem(contact["Last Name"]))
        self.setItem(row, 2, QTableWidgetItem(contact["Number"]))
        self.setItem(row, 3, QTableWidgetItem(contact["Address"]))
        self.setItem(row, 4, QTableWidgetItem(contact["Id"]))


class MainWindow(QMainWindow):
    """Main window.

    Our main window class that creates a QMainWindow.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the main window."""
        super().__init__(*args, **kwargs)
        # Set some attribute for main window
        self.setWindowTitle("Phonebook")
        self.setWindowIcon(QIcon('/assets/phone-book.png'))
        self.setGeometry(100, 100, 815, 400)

        # Create Table
        self.table = Table(parent=self)
        self.setCentralWidget(self.table)

        # Add data to table
        self.table.update_data()

        # Add dock to the main window
        dock = QDockWidget("New Contact")
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        # Create form to add to the dock
        form = QWidget()
        layout = QFormLayout(form)
        form.setLayout(layout)

        # Create Some widgets
        self.first_name = QLineEdit(form)
        self.first_name.setPlaceholderText("Necessary")
        self.last_name = QLineEdit(form)
        self.last_name.setPlaceholderText("Necessary")
        self.number = QLineEdit(form)
        self.number.setPlaceholderText("Necessary")
        self.address = QLineEdit(form)
        self.address.setPlaceholderText("Optional")

        # Add widgets to form layout
        layout.addRow("First Name:", self.first_name)
        layout.addRow("Last Name:", self.last_name)
        layout.addRow("Number:", self.number)
        layout.addRow("Address:", self.address)

        # Add a button to form layout
        btn_add = QPushButton("Add")
        btn_add.clicked.connect(self.add_contact)
        layout.addRow(btn_add)

        # Add form to the dock
        dock.setWidget(form)

        # Create toolbar and add it to the main window
        self.toolbar = QToolBar("main toolbar")
        self.toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(self.toolbar)

        # Add delete button to the toolbar
        self.delete_action = QAction(QIcon("./assets/delete.png"), "&Delete", self)
        self.delete_action.triggered.connect(self.delete)
        self.toolbar.addAction(self.delete_action)
        # Add delete label to the toolbar
        delete_label = QLabel("Delete Contact")
        self.toolbar.addWidget(delete_label)
        # Add separator
        self.toolbar.addSeparator()
        # Add search bar to the toolbar
        self.search_line = QLineEdit(self.toolbar)
        self.search_line.textChanged.connect(self.search)
        self.search_line.setFixedWidth(150)
        # Add search label to the toolbar
        self.search_label = QLabel("Search")
        self.toolbar.addWidget(self.search_line)
        self.toolbar.addWidget(self.search_label)
        # Add separator
        self.toolbar.addSeparator()
        # Add edit button to the toolbar
        pass

    def search(self, text):
        self.table.update_data(database.search_contact(text))

    def delete(self):
        """Delete Contact.

        delete selected contact in the table.
        :return: QMessageBox.warning()
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, "Warning", "Please select a record to delete")

        message = "\n".join(
         [
             "Are you sure that you want to delete the selected contact?",
             "",
             f"first name: {self.table.item(current_row, 0).text()}",
             f"last name: {self.table.item(current_row, 1).text()}",
             f"number: {self.table.item(current_row, 2).text()}",
             f"address: {self.table.item(current_row, 3).text()}",
         ]
        )
        button = QMessageBox.question(
            self,
            "Confirmation",
            message,
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            contact_id = self.table.item(current_row, 4).text()
            database.delete_contact(contact_id)
            self.table.removeRow(current_row)

    def valid(self):
        """Validate form.

        Checks if the form is valid and necessary fields are filled.
        :return:
        """
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        number = self.number.text().strip()

        if not first_name:
            QMessageBox.critical(self, "Error", "Please enter the first name")
            self.first_name.setFocus()
            return False

        if not last_name:
            QMessageBox.critical(self, "Error", "Please enter the last name")
            self.last_name.setFocus()
            return False

        if not number:
            QMessageBox.critical(self, "Error", "Please enter the Number")
            self.number.setFocus()
            return False

        try:
            number = self.number.text().strip()
            digit = number.isdigit()
            if not digit:
                raise ValueError
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter a valid number"
            )
            self.number.setFocus()
            return False

        if not 7 < len(number) < 12:
            QMessageBox.critical(
                self,
                "Error",
                "The phone number must be between 8 and 11 digits"
            )
            return False

        return True

    def reset(self):
        """Reset form widgets."""
        self.first_name.clear()
        self.last_name.clear()
        self.number.clear()
        self.address.clear()

    def add_contact(self):
        """Add new contact."""
        if not self.valid():
            return

        database.add_contact(
            self.first_name.text().strip(),
            self.last_name.text().strip(),
            self.number.text().strip(),
            self.address.text().strip(),
        )
        self.table.update_data()
        self.reset()


def main():
    """Main function."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
