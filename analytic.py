import argparse
import sys
import random
import time
import re
import datetime
import matplotlib.pyplot as plot

from datetime import datetime as dt
from logs.logs import Log
from utilities.utilities import Sort

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLA for analytic statistic of status code in apache log")
    parser.add_argument('-t', help="-- duration time in minute for read statistic status code, example : 10m")
    parser.add_argument('-d', help="-- directory target log file location, example : sample/")
    args = parser.parse_args()

    duration, dir = None, None
    duration_format = re.compile('^[0-9]+[m]{1}$')

    try:
        duration = args.t
        dir = args.d
    except Exception as identifier:
        print('error getting args', identifier)
        sys.exit(2)
    
    if not duration or not dir:
        print('wrong input, --help to see how to usage')
        sys.exit(2)

    if not duration_format.match(duration):
        print('wrong input format duration, --help to see how to usage')
        sys.exit(2)

    duration = int(duration.split('m')[0])
    to_duration = dt.now()
    from_duration = to_duration - datetime.timedelta(minutes=duration)
    # we can remove or set contains to None
    # contains = to_duration.strftime('http-%Y%m%d')
    contains = None

    log = Log(sourcedir=dir, from_duration=from_duration, to_duration=to_duration, contains=contains)
    responsecodes = log.get('RESPONSE_CODE')
    rescodes = Sort(responsecodes)
    rescodescounter = rescodes.count()
    
    print('Statistics for the last %d minutes' % (duration))
    print('Status codes:')
    keys, values = [], []
    for k, v in rescodescounter:
        print('%d : %d'%(k, v))
        keys.append(k) 
        values.append(v)
    print(keys, values)
    plot.plot(keys, values)
    plot.xlabel('status')
    plot.ylabel('statistics')
    plot.title('Statistics response code for %d minutes'%(duration))
    plot.show()
