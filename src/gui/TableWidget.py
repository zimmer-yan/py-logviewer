from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar, QMenu, QAction, QMenuBar, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QStatusBar, QCheckBox, QFileDialog, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide2.QtGui import QIcon, QContextMenuEvent, QCursor
from PySide2.QtCore import Qt, QSize
import sys
from src.gui.MenuBar import MenuBar
from src.core.LogContainer import LogContainer
from typing import Callable


class TableWidget(QTableWidget):
    def __init__(self, header: list[str], applyCallback: Callable[[str], None]):
        super().__init__()
        self.applyCallback = applyCallback

        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def displayRows(self, rows: list[list[str]]) -> int:
        self.removeAll()
        # print(f">> {self.rowCount()}")
        insertRow = -1
        for row in rows:
            insertRow = self.rowCount()
            self.insertRow(insertRow)
            for insertColumn, value in enumerate(row):
                self.setItem(insertRow, insertColumn, QTableWidgetItem(value))

        self.resizeColumnsToContents()
        return insertRow + 1

    def removeAll(self):
        self.clearContents()
        self.setRowCount(0)

        # print(f">> {self.rowCount()}")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        self.menu = QMenu(self)
        applyAsFilterEqualsAction = QAction('Apply as filter "="', self)
        applyAsFilterEqualsAction.triggered.connect(
            lambda: self.applyAsFilterSlot(event, True))
        applyAsFilterMatchesAction = QAction('Apply as filter "matches"', self)
        applyAsFilterMatchesAction.triggered.connect(
            lambda: self.applyAsFilterSlot(event, False))
        self.menu.addAction(applyAsFilterEqualsAction)
        self.menu.addAction(applyAsFilterMatchesAction)
        self.menu.exec_(QCursor.pos())
        # self.menu.popup(QCursor.pos())

    def applyAsFilterSlot(self, event: QContextMenuEvent, equals: True) -> None:
        print("apply slot called")
        # get the selected row and column
        row = self.rowAt(event.pos().y())
        col = self.columnAt(event.pos().x())
        # get the selected cell
        cell = self.item(row, col)
        # get the text inside selected cell (if any)
        cellText = cell.text()
        colHeader = self.horizontalHeaderItem(col).text()
        if not cellText or not colHeader:
            return
        # get the widget inside selected cell (if any)
        print(f"Apply {cellText} as filter for {colHeader}")
        self.applyCallback(
            colHeader + (' = ' if equals else ' matches ') + cellText)
