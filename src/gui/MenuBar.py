from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar, QMenu, QAction, QMenuBar, QLabel, \
    QStatusBar, QCheckBox, QFileDialog, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QSize
import sys
from typing import Callable


class MenuBar(QMenuBar):

    def __init__(self, onLoad: Callable, onClear: Callable):
        super().__init__()

        btn_load = QAction(QIcon("bug.png"), "&Load", self)
        btn_load.setStatusTip("Load File")
        btn_load.triggered.connect(onLoad)

        btn_clear = QAction(QIcon("bug.png"), "&Clear", self)
        btn_clear.setStatusTip("list uuids")
        btn_clear.triggered.connect(onClear)

        file_menu = self.addMenu("&File")
        file_menu.addAction(btn_load)
        file_menu.addAction(btn_clear)
