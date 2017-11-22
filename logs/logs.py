import os
import sys
import re
import progressbar
import datetime
import time
from datetime import datetime as dt
from fnmatch import fnmatch


class Log():
    __LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)'

    def __init__(self, sourcedir, from_duration, to_duration, contains=None, filename=None):
        # private var
        self.__logs = list()
        # self.__to_duration = time.mktime(dt.now().timetuple())
        # self.__from_duration = time.mktime((dt.now() - datetime.timedelta(minutes=duration)).timetuple())
        # self.__name_contains = to_duration.strftime('http-%Y%m%d')
        self.__from_duration = time.mktime(from_duration.timetuple())
        self.__to_duration = time.mktime(to_duration.timetuple())
        self.__name_contains = contains

        # check if filename is included in sourcedir
        cleansourcedir = sourcedir
        if '.log' in sourcedir:
            cleansourcedir = sourcedir.rsplit('/', 1)[0] + '/'
            filename = sourcedir.split('/')[-1]
        self.__sourcedir = cleansourcedir
        self.__filename = filename

        self.__read__()

    def __read__(self):
        if self.__filename:
            self.__readfile__()
            return

        self.__readfiles__()

    def __readfile__(self):
        try:
            filepath = os.path.join(self.__sourcedir, self.__filename)
        except Exception as identifier:
            print("file path doesn't exist ")
            sys.exit(2)
        
        file = open(filepath, 'r')
        self.__add__(file)

    def __readfiles__(self):
        try:
            files = os.listdir(self.__sourcedir)
        except Exception as identifier:
            print("file path doesn't exist ")
            sys.exit(2)
        
        for file in files:
            if file.endswith('.log') and self.__contains__(file):
                print('log file :', file)
                filepath = os.path.join(self.__sourcedir, file)
                file = open(filepath, 'r')
                self.__add__(file)
                file.close()

    def __contains__(self, file):
        if not self.__name_contains or fnmatch(file, self.__name_contains + '*'):
            return True
        return False

    def __add__(self, file):
        lines = file.readlines()
        bar = progressbar.ProgressBar(max_value=len(lines), widgets=[
            progressbar.Counter(format='read and collecting %(value)02d line from %(max_value)d') ,
            progressbar.Bar(),
            ' (', progressbar.ETA(), ') ',
        ])

        bar.start()
        for i, line in enumerate(reversed(lines)):
            line = self.__lineformatted__(line)
            bar.update(i)
            if line:
                if self.__induration__(line):
                    self.__logs.append(line)
                else:
                    break
                    
        bar.finish(end='\n\n')

    def __induration__(self, line):
        log_timestamp = time.mktime(line.get('DATETIME'))
        return self.__from_duration <= log_timestamp <= self.__to_duration

    def __lineformatted__(self, rawLine):
        rawLine = re.match(self.__LOG_PATTERN, rawLine)
        if not rawLine:
            return rawLine

        date_log = dt.strptime(rawLine.group(4), "%d/%b/%Y:%H:%M:%S %z").timetuple()
        return dict((
            ('IP', rawLine.group(1)),
            ('CLIENT_ID', rawLine.group(2)),
            ('USER_ID', rawLine.group(3)),
            ('DATETIME', date_log),
            ('METHOD', rawLine.group(5)),
            ('ENDPOINT', rawLine.group(6)),
            ('PROTOCOL', rawLine.group(7)),
            ('RESPONSE_CODE', int(rawLine.group(8))),
            ('CONTENT_SIZE', rawLine.group(9)),
        ))

    def get(self, key=None):
        if not key:
            return self.__logs

        tLogs = list()
        for log in self.__logs:
            tLogs += [log.get(key)]

        return tLogs

    def count(self):
        return len(self.__logs)
