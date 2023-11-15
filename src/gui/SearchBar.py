from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar, QMenu, QAction, QMenuBar, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QStatusBar, QCheckBox, QFileDialog, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QSize
import sys
from src.gui.MenuBar import MenuBar
from src.core.LogContainer import LogContainer
from typing import Callable


class SearchBar(QHBoxLayout):
    def __init__(self, applyCallback: Callable[[str], None]):
        super().__init__()

        self.applyCallback = applyCallback

        self.searchBar = QLineEdit()
        self.applyBtn = QPushButton('apply')
        self.applyBtn.clicked.connect(self.applyFilter)

        self.addWidget(self.searchBar)
        self.addWidget(self.applyBtn)

    def applyFilter(self):
        print("apply")
        self.applyCallback(self.searchBar.text())

    def setText(self, text: str) -> None:
        self.searchBar.setText(text)
