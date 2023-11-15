from PySide2.QtWidgets import QApplication
from src.gui.MainWindow import MainWindow
from src.core.LogParser import LogParser
from src.core.LogContainer import LogContainer
import sys

if __name__ == '__main__':

    uuid_regex = '^([0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12})'
    ts_regex = '([0-9]{4}\-[0-9]{2}\-[0-9]{2}\\s[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6})'
    lvl_regex = '\\[(DEBUG|INFO|NOTICE|WARNING|ERR|CRIT|ALERT)\\]'

    parser = LogParser(
        'uuid',
        uuid_regex,
        {
            'ts': ts_regex,
            'lvl': lvl_regex
        }
    )
    container = LogContainer(parser)

    app = QApplication(sys.argv)

    window = MainWindow(container)
    window.showMaximized()

    sys.exit(app.exec_())
