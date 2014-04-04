from os import path
import unittest
# from docutils.nodes import danger

from comp61542.database import database
from comp61542.visualization import network

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-2], 1,
            "incorrect total")

    def test_get_author_statistics(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_author_statistics()
        self.assertEqual(header[4], "Total", "The header of the 5th column is not correct")
        self.assertEqual(data[0][1], 2, "The number of times author 1 appears 1st is not right")
        self.assertEqual(data[0][2], 0, "The number of times author 1 appears last is not right")
        self.assertEqual(data[0][3], 0, "The number of times author 1 appears other is not right")
        self.assertEqual(data[1][3], 1, "The number of times author 2 appears other is not right")
        self.assertEqual(data[1][4], 2, "The total number of publications of author 2 is not right")
        self.assertEqual(data[2][4], 1, "The total number of publications of author 3 is not right")
        
    def test_get_author_statistics_with_sole(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple4.xml")))
        header, data = db.get_author_statistics_with_sole(4)
        self.assertEqual(header[3], "Sole author", "The header of the 5th column is not correct")
        # Testing author A
        self.assertEqual(data[0][1], 1, "The number of times author A appears first is not right")
        self.assertEqual(data[0][2], 0, "The number of times author A appears last is not right")
        self.assertEqual(data[0][3], 1, "The number of times author A appears sole is not right")
        self.assertEqual(data[0][4], 0, "The number of times author A appears other is not right")
        # Testing author B
        self.assertEqual(data[1][1], 0, "The number of times author B appears first is not right")
        self.assertEqual(data[1][2], 1, "The number of times author B appears last is not right")
        self.assertEqual(data[1][3], 0, "The number of times author B appears sole is not right")
        self.assertEqual(data[1][4], 1, "The number of times author B appears other is not right")
        # Testing author C
        self.assertEqual(data[2][1], 1, "The number of times author C appears first is not right")
        self.assertEqual(data[2][2], 1, "The number of times author C appears last is not right")
        self.assertEqual(data[2][3], 1, "The number of times author C appears sole is not right")
        self.assertEqual(data[2][4], 0, "The number of times author C appears other is not right")

        header, data = db.get_author_statistics_with_sole(0)
        self.assertEqual(header[3], "Sole author", "The header of the 5th column is not correct")
        # Testing author A
        self.assertEqual(data[0][1], 1, "The number of times author A appears first is not right")
        self.assertEqual(data[0][2], 0, "The number of times author A appears last is not right")
        self.assertEqual(data[0][3], 0, "The number of times author A appears sole is not right")
        self.assertEqual(data[0][4], 0, "The number of times author A appears other is not right")
        # Testing author B
        self.assertEqual(data[1][1], 0, "The number of times author B appears first is not right")
        self.assertEqual(data[1][2], 0, "The number of times author B appears last is not right")
        self.assertEqual(data[1][3], 0, "The number of times author B appears sole is not right")
        self.assertEqual(data[1][4], 1, "The number of times author B appears other is not right")
        # Testing author C
        self.assertEqual(data[2][1], 0, "The number of times author C appears first is not right")
        self.assertEqual(data[2][2], 1, "The number of times author C appears last is not right")
        self.assertEqual(data[2][3], 0, "The number of times author C appears sole is not right")
        self.assertEqual(data[2][4], 0, "The number of times author C appears other is not right")


        header, data = db.get_author_statistics_with_sole(1)
        self.assertEqual(header[3], "Sole author", "The header of the 5th column is not correct")
        # Testing author A
        self.assertEqual(data[0][1], 0, "The number of times author A appears first is not right")
        self.assertEqual(data[0][2], 0, "The number of times author A appears last is not right")
        self.assertEqual(data[0][3], 0, "The number of times author A appears sole is not right")
        self.assertEqual(data[0][4], 0, "The number of times author A appears other is not right")
        # Testing author B
        self.assertEqual(data[1][1], 0, "The number of times author B appears first is not right")
        self.assertEqual(data[1][2], 1, "The number of times author B appears last is not right")
        self.assertEqual(data[1][3], 0, "The number of times author B appears sole is not right")
        self.assertEqual(data[1][4], 0, "The number of times author B appears other is not right")
        # Testing author C
        self.assertEqual(data[2][1], 1, "The number of times author C appears first is not right")
        self.assertEqual(data[2][2], 0, "The number of times author C appears last is not right")
        self.assertEqual(data[2][3], 0, "The number of times author C appears sole is not right")
        self.assertEqual(data[2][4], 0, "The number of times author C appears other is not right")


        header, data = db.get_author_statistics_with_sole(2)
        self.assertEqual(header[3], "Sole author", "The header of the 5th column is not correct")
        # Testing author A
        self.assertEqual(data[0][1], 0, "The number of times author A appears first is not right")
        self.assertEqual(data[0][2], 0, "The number of times author A appears last is not right")
        self.assertEqual(data[0][3], 1, "The number of times author A appears sole is not right")
        self.assertEqual(data[0][4], 0, "The number of times author A appears other is not right")
        # Testing author B
        self.assertEqual(data[1][1], 0, "The number of times author B appears first is not right")
        self.assertEqual(data[1][2], 0, "The number of times author B appears last is not right")
        self.assertEqual(data[1][3], 0, "The number of times author B appears sole is not right")
        self.assertEqual(data[1][4], 0, "The number of times author B appears other is not right")
        # Testing author C
        self.assertEqual(data[2][1], 0, "The number of times author C appears first is not right")
        self.assertEqual(data[2][2], 0, "The number of times author C appears last is not right")
        self.assertEqual(data[2][3], 0, "The number of times author C appears sole is not right")
        self.assertEqual(data[2][4], 0, "The number of times author C appears other is not right")


        header, data = db.get_author_statistics_with_sole(3)
        self.assertEqual(header[3], "Sole author", "The header of the 5th column is not correct")
        # Testing author A
        self.assertEqual(data[0][1], 0, "The number of times author A appears first is not right")
        self.assertEqual(data[0][2], 0, "The number of times author A appears last is not right")
        self.assertEqual(data[0][3], 0, "The number of times author A appears sole is not right")
        self.assertEqual(data[0][4], 0, "The number of times author A appears other is not right")
        # Testing author B
        self.assertEqual(data[1][1], 0, "The number of times author B appears first is not right")
        self.assertEqual(data[1][2], 0, "The number of times author B appears last is not right")
        self.assertEqual(data[1][3], 0, "The number of times author B appears sole is not right")
        self.assertEqual(data[1][4], 0, "The number of times author B appears other is not right")
        # Testing author C
        self.assertEqual(data[2][1], 0, "The number of times author C appears first is not right")
        self.assertEqual(data[2][2], 0, "The number of times author C appears last is not right")
        self.assertEqual(data[2][3], 1, "The number of times author C appears sole is not right")
        self.assertEqual(data[2][4], 0, "The number of times author C appears other is not right")
        
    def test_get_author_statistics_detailed(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "test-author-stat-detailed.xml")))
        # Testing all publications (4) for author A
        data = db.get_author_statistics_detailed("AUTHOR A", 4)
        self.assertEqual(data[0], 2, "The number of publications of author A as first is not right")
        self.assertEqual(data[1], 1, "The number of publications of author A as last is not right")
        self.assertEqual(data[2], 1, "The number of publications of author A as sole is not right")
        self.assertEqual(data[3], 3, "The number of co-authors of author A is not right")
        self.assertEqual(data[4], 5, "The number of overall publications of author A is not right")
        # Testing inproceedings (0) for author B
        data = db.get_author_statistics_detailed("AUTHOR B", 0)
        self.assertEqual(data[0], 0, "The number of conference papers of author B as first is not right")
        self.assertEqual(data[1], 1, "The number of conference papers of author B as last is not right")
        self.assertEqual(data[2], 0, "The number of conference papers of author B as sole is not right")
        self.assertEqual(data[3], 2, "The number of co-authors in conference papers of author B is not right")
        self.assertEqual(data[4], 2, "The number of overall conference papers of author B is not right")
        data = db.get_author_statistics_detailed("AUTHOR C", 4)
        self.assertEqual(data[0], 0, "The number of publications of author C as first is not right")
        self.assertEqual(data[1], 2, "The number of publications of author C as last is not right")
        self.assertEqual(data[2], 0, "The number of publications of author C as sole is not right")
        self.assertEqual(data[3], 2, "The number of co-authors in publications of author C is not right" + str(data[3]))
        self.assertEqual(data[4], 2, "The number of overall publications of author C is not right")
        # Testing exception case on the type index
        self.assertRaises(ValueError, lambda: db.get_author_statistics_detailed(0, 5))

    def test_get_author_statistics_detailed_all(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "test-author-stat-detailed.xml")))
        header = ("", "First Author", "Last Author", "Sole Author", "Co-Authors", "All")
        body = [['Conference Papers', 2, 0, 0, 2, 2], ['Journal', 0, 0, 0, 0, 0], ['Book', 0, 1, 1, 3, 3], ['Book Chapter', 0, 0, 0, 0, 0], ['All Publication', 2, 1, 1, 3, 5]]
        self.assertEqual(db.get_author_statistics_detailed_all("AUTHOR A"), (header, body), "The statistics detail for AUTHOR A is not right")
        body = [['Conference Papers', 0, 1, 0, 2, 2], ['Journal', 0, 0, 0, 0, 0], ['Book', 2, 0, 0, 3, 2], ['Book Chapter', 0, 0, 0, 0, 0], ['All Publication', 2, 1, 0, 3, 4]]
        self.assertEqual(db.get_author_statistics_detailed_all("AUTHOR B"), (header, body), "The statistics detail for AUTHOR B is not right")
        body = [['Conference Papers', 0, 1, 0, 2, 1], ['Journal', 0, 0, 0, 0, 0], ['Book', 0, 1, 0, 2, 1], ['Book Chapter', 0, 0, 0, 0, 0], ['All Publication', 0, 2, 0, 2, 2]]
        self.assertEqual(db.get_author_statistics_detailed_all("AUTHOR C"), (header, body), "The statistics detail for AUTHOR C is not right")
        body = [['Conference Papers', 0, 0, 0, 0, 0], ['Journal', 0, 0, 0, 0, 0], ['Book', 0, 0, 0, 2, 1], ['Book Chapter', 0, 0, 0, 0, 0], ['All Publication', 0, 0, 0, 2, 1]]
        self.assertEqual(db.get_author_statistics_detailed_all("AUTHOR D"), (header, body), "The statistics detail for AUTHOR D is not right")

    def test_get_author_by_name(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-story-5.xml")))
        data = db.get_author_by_name("sam")
        self.assertEqual(len(data), 11, "the length is mismatching")
        if len(data)>0:
            for i in range(0, len(data)-1):
                self.assertIn("sam".lower(), data[i].lower(), "incorrect author name")

    def test_sort_author_by_name(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-story-5.xml")))
        data = db.sort_author_by_name("sam")
        self.assertEqual(data[0][0], "Alice Sam", "incorrect order, 1st author should be Alice Sam")
        self.assertEqual(data[1][0], "Brian Sam", "incorrect order, 2nd author should be Brian Sam")
        self.assertEqual(data[2][0], "Alice Samming", "incorrect order, 3rd author should be Alice Samming")
        self.assertEqual(data[3][0], "Brian Samming", "incorrect order, 4th author should be Brian Samming")
        self.assertEqual(data[4][0], "Uli Samtler", "incorrect order, 4th author should be Uli Samtler")
        self.assertEqual(data[5][0], "Sam Alice", "incorrect order, 5th author should be Sam Alice")
        self.assertEqual(data[6][0], "Sam Brian", "incorrect order, 6th author should be Sam Brian")
        self.assertEqual(data[7][0], "Samuel Alice", "incorrect order, 7th author should be Samuel Alice")
        self.assertEqual(data[8][0], "Samuel Brian", "incorrect order, 8th author should be Samuel Brian")
        self.assertEqual(data[9][0], "Alice Esam", "incorrect order, 9th author should be Alice Esam")
        self.assertEqual(data[10][0], "Brian Esam", "incorrect order, 10th author should be Brian Esam")
        
    def test_split_author_name(self):
        db = database.Database()
        # Expected return: [full name, last name, first name]
        # No middlename
        data = db.split_author_name("Samuel Alexander")
        self.assertEqual(len(data), 4, "There's a mismatch between the table length and the expected name split")
        self.assertEqual(data[0], "Samuel Alexander", "The full name is wrong")
        self.assertEqual(data[1], "Alexander", "The last name is wrong")
        self.assertEqual(data[2], "Samuel", "The first name is wrong")
        # One middlename
        data = db.split_author_name("Samuel Alexander Checkov")
        self.assertEqual(len(data), 4, "There's a mismatch between the table length and the expected name split")
        self.assertEqual(data[0], "Samuel Alexander Checkov", "The full name is wrong")
        self.assertEqual(data[1], "Checkov", "The last name is wrong")
        self.assertEqual(data[2], "Samuel", "The first name is wrong")
        # Two middlenames
        data = db.split_author_name("Leonard Alexander R. Qwerty")
        self.assertEqual(len(data), 4, "There's a mismatch between the table length and the expected name split")
        self.assertEqual(data[0], "Leonard Alexander R. Qwerty", "The full name is wrong")
        self.assertEqual(data[1], "Qwerty", "The last name is wrong")
        self.assertEqual(data[2], "Leonard", "The first name is wrong")
        # Special case: only one name
        data = db.split_author_name("Uli")
        self.assertEqual(len(data), 4, "There's a mismatch between the table length and the expected name split")
        self.assertEqual(data[0], "Uli", "The name is wrong")
        self.assertEqual(data[1], "Uli", "The name is wrong")
        self.assertEqual(data[2], "", "The special case is not well handled")
        
    def test_get_degree_of_separation(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "test-separation.xml")))
        self.assertEqual(db.get_degree_of_separation("Author C", "Author D"), 1, "Incorrect DoS between C and D")
        self.assertEqual(db.get_degree_of_separation("Author A", "Author B"), 0, "Incorrect DoS between A and B")
        self.assertEqual(db.get_degree_of_separation("Author E", "Author C"), 2, "Incorrect DoS between E and C")
        self.assertEqual(db.get_degree_of_separation("Author A", "Author F"), "X", "Incorrect DoS between A and F")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_average_authors_per_publication_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")

    def test_network(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "test-separation.xml")))
        network.D3JsonGraph(db.authors_graph)

if __name__ == '__main__':
    unittest.main()
