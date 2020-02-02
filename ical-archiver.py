from io import BufferedReader, BufferedWriter
from datetime import datetime
from icalendar import Calendar
from argparse import ArgumentParser, FileType

parser = ArgumentParser()
parser.add_argument('inputFile', nargs=1, type=FileType('rb'))
parser.add_argument('-n', '--newFile', nargs=1, type=FileType('wb'),
                    help='''if this parameters is provided, the archived items are not removed from the inputFile but 
                    added to a new file. Provide the file name using --newFile''')
parser.add_argument('archiveFile', nargs=1, type=FileType('wb'))
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
        continue
    dtendDt = datetime.combine(dtend.dt, datetime.min.time())
    if dtendDt < maxDate:
        archiveCal.add_component(event)
        count += 1
    else:
        kept += 1

for event in archiveCal.subcomponents:
    if event.name != 'VEVENT':
        continue
    currentCal.subcomponents.remove(event)

try:
    newFile = args.newFile[0]
except TypeError:
    newFile = open(args.inputFile[0].name, 'wb')
newFile.write(currentCal.to_ical(False))
newFile.close()

archiveFile: BufferedWriter = args.archiveFile[0]
archiveFile.write(archiveCal.to_ical(False))
archiveFile.close()

print(str(count) + " events archived, " + str(kept) + ' events kept')
