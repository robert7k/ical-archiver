from io import BufferedReader, BufferedWriter
from datetime import datetime
from icalendar import Calendar

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('inputFile', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('newFile', nargs=1, type=argparse.FileType('wb'))
parser.add_argument('archiveFile', nargs=1, type=argparse.FileType('wb'))
parser.add_argument('date', nargs=1, type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                    help='date in the format "Y-m-d". All events before this date are moved into the archive file')
args = parser.parse_args()
inputFile: BufferedReader = args.inputFile[0]
maxDate: datetime = args.date[0]

currentCal: Calendar = Calendar.from_ical(inputFile.read())
inputFile.close()
archiveCal = Calendar()
archiveCal.add('prodid', 'ical-archiver')

count = 0
kept = 0

for event in currentCal.subcomponents:
    if event.name != 'VEVENT':
        archiveCal.add_component(event)
        continue
    dtend = event.get('dtend')
    if not hasattr(dtend, 'dt'):
        print(event.get('summary') + " has no end")
        continue
    dtendDt = datetime.combine(dtend.dt, datetime.min.time())
    if (dtendDt < maxDate):
        archiveCal.add_component(event)
        count += 1
    else:
        kept += 1

for event in archiveCal.subcomponents:
    if event.name != 'VEVENT':
        continue
    currentCal.subcomponents.remove(event)

newFile: BufferedWriter = args.newFile[0]
newFile.write(currentCal.to_ical(False))
newFile.close()

archiveFile: BufferedWriter = args.archiveFile[0]
archiveFile.write(archiveCal.to_ical(False))
archiveFile.close()

print(str(count) + " events archived, " + str(kept) + ' events kept')
