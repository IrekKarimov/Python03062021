import unittest
import time

class Base(unittest.TestCase):
    name = None
    def setUp(self):
        name = self.name

    def test_run(self):
        t = int(time.time())
        m = t % 2
        self.assertEqual(m, 0)


if __name__ == '__main__':
    unittest.main()

