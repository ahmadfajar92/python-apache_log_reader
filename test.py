import unittest
import datetime
from logs.logs import Log
from datetime import datetime as dt
from utilities.utilities import Sort

class TestMethod(unittest.TestCase):
    
    def test_count_statuscode(self):
        duration = 100000
        to_duration = dt.now()
        from_duration = to_duration - datetime.timedelta(minutes=duration)
        dir = 'samples/http-201701040000.log'

        log = Log(sourcedir=dir, from_duration=from_duration,
                to_duration=to_duration)

        responsecodes = log.get('RESPONSE_CODE')
        rescodes = Sort(responsecodes)
        rescodescounter = rescodes.count()
        
        print(rescodescounter, 'status code counter dict')
        # status code 100 must be 1 count depend on condition
        self.assertEqual(1, dict(rescodescounter).get(100))

        # status code 200 must be 208 count depend on condition
        self.assertEqual(208, dict(rescodescounter).get(200))
        
        # status code 301 must be 4 count depend on condition
        self.assertEqual(4, dict(rescodescounter).get(301))


if __name__ == '__main__':
    unittest.main()
