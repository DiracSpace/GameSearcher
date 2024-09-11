import unittest
from backend.core.find_query import FindQuery


class TestFindQuery(unittest.TestCase):

    def test_init(self):
        """
        Tests the initialization of the FindQuery class.
        """
        query = FindQuery(
            page_index=1, page_size=10, filter="name eq John", order_by="name"
        )
        self.assertEqual(query.page_index, 1)
        self.assertEqual(query.page_size, 10)
        self.assertEqual(query.filter, "name eq John")
        self.assertEqual(query.order_by, "name")


if __name__ == "__main__":
    unittest.main()
