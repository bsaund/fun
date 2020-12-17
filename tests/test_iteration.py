from unittest import TestCase
from utils.iteration import subselect_2d


class Test(TestCase):
    def test_subselect_2d(self):
        arr = [[i for i in range(n, 5 + n)] for n in range(5)]
        ans1 = [[i for i in range(n + 1, 4 + n)] for n in range(1, 4)]
        self.assertEqual(ans1, subselect_2d(arr, 2, 2, 1, 1))

        ans2 = [[i for i in range(n, 2 + n)] for n in range(2)]
        self.assertEqual(ans2, subselect_2d(arr, 0, 0, 1, 1))

        ans3 = [[i for i in range(n+3, 5 + n)] for n in range(2, 5)]
        self.assertEqual(ans3, subselect_2d(arr, 4, 3, 1, 1))

