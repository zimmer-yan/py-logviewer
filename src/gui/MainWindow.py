from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar, QMenu, QAction, QMenuBar, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QStatusBar, QCheckBox, QFileDialog, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QSize
import sys
from src.gui.MenuBar import MenuBar
from src.gui.TableWidget import TableWidget
from src.gui.SearchBar import SearchBar
from src.core.LogContainer import LogContainer


class MainWindow(QMainWindow):

    def __init__(self, container: LogContainer):
        super().__init__()
        self.logContainer: LogContainer = container

        self.setWindowTitle("Log Viewer")

        self.setStatusBar(QStatusBar(self))

        menu = MenuBar(self.onFileLoad, self.onClear)
        self.setMenuBar(menu)

        self.searchBar = SearchBar(self.applyFilter)

        header = self.logContainer.getHeader(True)
        self.table = TableWidget(header, self.applyFilter)

        containerWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.searchBar)
        mainLayout.addWidget(self.table)
        containerWidget.setLayout(mainLayout)
        self.setCentralWidget(containerWidget)

    def onFileLoad(self):
        print('load')
        (fileName, filter) = QFileDialog.getOpenFileName(
            self, "Open Image", "~", 'Log files (*.log*)')
        self.logContainer.load(fileName)

        num = self.table.displayRows(self.logContainer.fetchAllRows())

        self.notifyShow(num)

    def notifyShow(self, num: int) -> None:
        total = len(self.logContainer)
        if total == 0:
            return
        percent = 100 if num == total else round((num / total) * 100, 1)
        self.statusBar().showMessage(
            f'Showing {num}/{total} ({percent}%) rows'
        )

    def onClear(self):
        print('clear')
        self.logContainer.clear()
        self.table.removeAll()
        self.notifyShow(0)

    def applyFilter(self, text: str):
        print("apply:")
        print(text)
        self.searchBar.setText(text)

        if not text.strip():
            num = self.table.displayRows(self.logContainer.fetchAllRows())
            self.notifyShow(num)
            return

        key, value = [e.strip() for e in text.split(' matches ', 2)]
        filter = {key: value}
        print(filter)

        num = self.table.displayRows(
            self.logContainer.fetchAllRowsFiltered(filter=filter)
        )

        self.notifyShow(num)
