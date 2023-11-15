import re


class LogLine:
    def __init__(self, cols: dict[str, str | None]) -> None:
        self.columns: dict[str, str | None] = cols


class AccumulatedLog:
    def __init__(self, idName: str, id: str) -> None:
        self.idName = idName
        self.id = id
        self.lines: list[LogLine] = []


class LogParser:
    def __init__(self, idName: str, idRegex: str, parseDefinition: dict[str, str]) -> None:
        self.idName = idName
        self.idRegex = idRegex
        self.definition: dict[str, str] = parseDefinition

    def getHeader(self, includeFull: bool = False) -> list[str]:
        return [self.idName] + list(self.definition.keys()) + (['_full'] if includeFull else [])

    @staticmethod
    def _readFile(fileName: str) -> list[str]:
        with open(fileName, 'r') as f:
            return f.readlines()

    def fetchLog(self, fileName: str) -> dict[str, AccumulatedLog]:
        lines = LogParser._readFile(fileName)

        logs: dict[str, AccumulatedLog] = {}

        for line in lines:
            if not (res := self._parseLine(line)):
                continue

            id, logLine = res

            if id in logs.keys():
                log = logs[id]
            else:
                log = AccumulatedLog(self.idName, id)
                logs[id] = log
            log.lines.append(logLine)

        return logs

    def _parseLine(self, line: str) -> tuple[str, LogLine] | None:
        if not re.search(self.idRegex, line):
            return None

        defs = self.definition
        defs[self.idName] = self.idRegex

        columns = self._matchDefs(line, defs)

        id = columns.pop(self.idName)

        columns['_full'] = line

        defs.pop(self.idName)
        return (id, LogLine(columns))

    def _matchDefs(self, line: str, defs: dict[str, str]) -> dict[str, str]:
        columns = {}
        for name, regex in defs.items():
            if not (match := re.search(regex, line)):
                columns[name] = None
                continue
            columns[name] = match.groups()[0]
            # beg, end = match.span()
            # line = line[:beg] + line[end:]
        # print(columns)
        return columns


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

    info = parser.fetchLog('./freeswitch.log')
    print("------------")
    print(parser.getHeader())
