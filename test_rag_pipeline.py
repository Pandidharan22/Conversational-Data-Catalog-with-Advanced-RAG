import unittest
from rag_pipeline import search_metadata

class TestRAGPipeline(unittest.TestCase):
    def test_search_metadata(self):
        # Test a typical query
        query = "Which dataset has the most columns with null values?"
        results = search_metadata(query, top_k=2)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertTrue(any("nulls" in r.lower() for r in results))

    def test_search_metadata_empty_query(self):
        # Test with an empty query
        results = search_metadata("", top_k=2)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_search_metadata_unrelated_query(self):
        # Test with a query unlikely to match
        results = search_metadata("completely unrelated query", top_k=2)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

if __name__ == "__main__":
    unittest.main()
