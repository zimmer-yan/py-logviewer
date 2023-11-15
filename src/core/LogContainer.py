try:
    from src.core.LogParser import LogParser, AccumulatedLog, LogLine
except:
    from LogParser import LogParser, AccumulatedLog, LogLine


class LogContainer:
    def __init__(self, parser: LogParser) -> None:
        self.parser = parser

        self.logs: dict[str, AccumulatedLog] = {}

    def load(self, fileName: str) -> None:
        self.logs = self.logs | self.parser.fetchLog(fileName)

    def loadNew(self, fileName: str) -> None:
        self.clear()
        self.load(fileName)

    def clear(self) -> None:
        self.logs = {}

    def getHeader(self, includeFull: bool = False) -> list[str]:
        return self.parser.getHeader(includeFull)

    def fetchAllRows(self, columns: list[str] = []) -> list[list[str | None]]:
        return self.fetchAllRowsFiltered(columns)

    def fetchAllRowsFiltered(self, columns: list[str] = [], filter: dict[str, str] = {}) -> list[list[str | None]]:
        filterColumns = columns if columns else self.getHeader(
            includeFull=True)
        rows: list[list[str]] = []
        for id, accumulatedLog in self.logs.items():
            for line in accumulatedLog.lines:
                row = self._buildRow(id, line, filterColumns, filter)
                if not row:
                    continue
                rows.append(row)
        return rows

    def _buildRow(self, id: str, line: LogLine, filterColumns: list[str], filterValues: dict[str, str]):
        # filter id
        idName = self.parser.idName
        # print(idName)
        # print(filterValues.keys())
        # print(id)
        # print(filterValues[idName] not in id)
        if idName in filterValues.keys() and filterValues[idName] not in id:
            return None

        row: list[str] = [id]
        for columnName in filterColumns:
            if not columnName in line.columns.keys():
                continue
            value = line.columns[columnName]
            if columnName in filterValues.keys():
                # print(filterValues[columnName])
                # print(value)
                if not value or filterValues[columnName] not in value:
                    # print("skip")
                    return None
            row.append(value)
        # print(row)
        # exit()
        return row

    def __len__(self):
        return len(self.fetchAllRows([self.parser.idName]))


if __name__ == '__main__':
    uuid_regex = '^([0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12})'
    ts_regex = '([0-9]{4}\-[0-9]{2}\-[0-9]{2}\\s[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{6})'
    lvl_regex = '\\[(DEBUG|INFO|NOTICE|WARNING|ERR|CRIT|ALERT)\\]'

    line = '1eefeb9c-10af-438e-a51c-f6adc3750b10 2023-10-25 05:13:10.082363 [NOTICE] switch_channel.c:1118 New Channel sofia/external/anonymous@anonymous.invalid [1eefeb9c-10af-438e-a51c-f6adc3750b10]'
    # print(re.search(uuid_regex, line))
    # print(re.search(ts_regex, line))
    # print(match := re.search(lvl_regex, line))
    # print(match.groups()[0])
    # exit()

    parser = LogParser(
        'uuid',
        uuid_regex,
        {
            'ts': ts_regex,
            'lvl': lvl_regex
        }
    )

    container = LogContainer(parser)

    container.load('./freeswitch.log')
    print("------------")
    print(container.getHeader())
    print("-------------------")
    rows = container.fetchAllRowsFiltered(filter={'uuid': '1eef'})
    print(len(rows))
    for row in rows:
        pass
        print(row)
