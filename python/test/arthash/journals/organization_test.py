import os, unittest
from arthash.journals import organization


class NextTest(unittest.TestCase):
    def test_next_file(self):
        org = organization.Organization()

        def test(before, after):
            self.assertEqual(org.next_file(before), after)

        test('00/00/00/00.json', '00/00/00/01.json')
        test('00/00/00/01.json', '00/00/00/02.json')
        test('00/00/00/fe.json', '00/00/00/ff.json')
        test('00/00/00/ff.json', '00/00/01/00.json')
        test('00/00/01/00.json', '00/00/01/01.json')
        test('00/00/ff/ff.json', '00/01/00/00.json')
        test('00/ff/ff/ff.json', '01/00/00/00.json')
        test('ff/ff/ff/ff.json', '100/00/00/00.json')
