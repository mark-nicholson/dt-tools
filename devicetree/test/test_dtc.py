#
# Testing infra for DTC ...
#

import random
import unittest

from devicetree.dtc import DTC

class TestDTC(unittest.TestCase):

    def setUp(self):
        pass

    def test_construction(self):

        # check basic instance
        self.assertNotEqual(None, DTC)

        # proper value
        path = '/scratch/mjnichol/github/dt-tools/venv/bin/dtc'
        self.assertNotEqual(None, DTC, path)

        # bogus path
        path = '/this/does/not/exist'
        with self.assertRaises(ValueError) as cm:
            dtc = DTC('/this/does/not/exist')
        self.assertIn(path, str(cm.exception))
        
    def test_build(self):
        dtc = DTC()
        dtc.in_file = 'devicetree/test/spear1310-evb.dts'
        dtc.out_file = 'devicetree/test/spear1310-evb.dtb'
        dtc.includes.append( 'devicetree/test')

        self.assertEqual( dtc.in_format, 'dts' )
        self.assertEqual( dtc.out_format, 'dtb' )

        rv, log = dtc.build()
        self.assertEqual(rv, 0)

    #def test_sample(self):
    #    with self.assertRaises(ValueError):
    #        random.sample(self.seq, 20)
    #    for element in random.sample(self.seq, 5):
    #        self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
