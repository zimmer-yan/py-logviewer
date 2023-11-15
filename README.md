# py-logviewer

This project is made to be like wireshark but for general text files.

Running the main will open a small viewer window.

## Config

First set the regexes in the `main.py` file for the parser. Example:
```python
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
```

The Parsers first arg is the name of the grouping column, the second arg the regex for the grouping column, the thrid arg is a dict of name => regex for the remaining columns. In the above example the grouping column is a uuid. The other columns are a timestamp and a loglevel.

## Usage

Use the Menubar to load a logfile or clear the table again.

Use the the searchbar for simple filtering: `<column_name> matches <value>`.
