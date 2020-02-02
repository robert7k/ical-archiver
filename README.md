# ical-archiver

Archive old events fom an ICS file and save them to a new archive ICS file.

    usage: ical-archiver.py [-h] [-n NEWFILE] inputFile archiveFile date
    
    positional arguments:
      inputFile             Input ICS file to read events from
      archiveFile           Archive ICS file to output archived events into.
      date                  date in the format "Y-m-d". All events before this
                            date are moved into the archive file. Example:
                            2019-12-31
    
    optional arguments:
      -h, --help            show this help message and exit
      -n NEWFILE, --newFile NEWFILE
                            if this parameters is provided, the archived items are
                            not removed from the inputFile but added to a new
                            file. Provide the file name using --newFile