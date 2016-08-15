# fileparser
Parse files and load into database

## Python Version
Python 2.7.10

## Run App
`python fileparser.py None None data specs test.db _ .`

## Run Tests
`python testfileparser.py`

## Caveats
* Not enough error checking
* Not enough data sanitation/cleaning
* Assumes only three columns
* Incomplete unit tests
* Assumes width column is after column name
* Expects "column name" to appear with double quotes

## Assumptions
- assumes that there are only ever three columns
- assume when files come to the system, they come in pairs
- assume data and spec for a given day is unique (not currently handled)
- the filenames are not repeated
- repeated filetypes would have different dates
- the most recent filetype would have the most recent date
    - this assumes that the files are loaded/dropped once a day
- assume file paths are for linux/unix system
- sqlite3 dbs end with .db extensions

## Problem definition

You receive drops of data files and specification files. Write an application
in language of choice that will load these files into a database.

## Problem details

Data files will be dropped in the folder "data/" relative to your application
and specification files will be dropped in the folder "specs/" relative to
your application.

Specification files will have filenames equal to the file type they specify and
extension of ".csv". So "fileformat1.csv" would be the specification for files
of type "fileformat1".

Data files will have filenames equal to their file format type, followed by
an underscore, followed by the drop date and an extension of ".txt".
For example, "fileformat1_2007-10-01.txt" would be a
data file to be parsed using "specs/fileformat1.csv", which arrived on 10/01/2007.

Format files will be csv formated with columns "column name", "width", and
"datatype".

* "column name" will be the name of that column in the database table
* "width" is the number of characters taken up by the column in the data file
* "datatype" is the SQL data type that should be used to store the value
in the database table.

Data files will be flat text files with rows matching single records for the
database. Rows are formatted as specified by the associated format file.

## Examples

This is an example file pair; other files may vary in structure while still
fitting the structure of the problem details (above):

specs/testformat1.csv

```text
"column name",width,datatype
name,10,TEXT
valid,1,BOOLEAN
count,3,INTEGER
```

data/testformat1_2015-06-28.txt

```text
Foonyor   1  1
Barzane   0-12
Quuxitude 1103
```

Sample table output:
```text
name      | valid | count
--------- | ----- | -----
Foonyor   | True  |     1
Barzane   | False |   -12
Quuxitude | True  |   103
```

## Expectations

- Your application can be written with language/libraries of your choosing.
- Database type and connection mechanism is left to your discretion.
- You should include tests that cover, at least, the examples given.
- You should implement the conversions for the SQL data types: TEXT, BOOLEAN,
and INTEGER
- Files can be assumed to use UTF-8 encoding
- You should be prepared to discuss implementation decisions and possible
extensions to your application.

REFERENCE:
https://gist.githubusercontent.com/dmshann0n/6dfba5ebdebe1098d579/raw/ccc74cec150a3580f8399ade58f4dd247df28456/file_parser.md
