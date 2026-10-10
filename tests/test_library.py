"""
test_library.py - Tests for the Library Management System.

Tests cover:
- Creating multiple libraries
- Adding multiple books to different libraries
- Viewing and searching books
- Duplicate ID prevention
- Invalid input handling
- Empty / missing CSV file handling
- Data persistence across LibraryManager reloads
"""

import os
import sys
import unittest
import shutil

# Add project root to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import csv_storage
from library_manager import LibraryManager


class TestSetup(unittest.TestCase):
    """Base class that sets up a temporary data directory for each test."""

    def setUp(self):
        """Redirect CSV storage to a temporary test directory."""
        self.original_data_dir = csv_storage.DATA_DIR
        self.original_lib_csv = csv_storage.LIBRARIES_CSV
        self.original_book_csv = csv_storage.BOOKS_CSV

        # Use a temporary test data directory
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), "test_data"
        )
        csv_storage.DATA_DIR = self.test_data_dir
        csv_storage.LIBRARIES_CSV = os.path.join(self.test_data_dir, "libraries.csv")
        csv_storage.BOOKS_CSV = os.path.join(self.test_data_dir, "books.csv")

    def tearDown(self):
        """Restore original paths and clean up test files."""
        csv_storage.DATA_DIR = self.original_data_dir
        csv_storage.LIBRARIES_CSV = self.original_lib_csv
        csv_storage.BOOKS_CSV = self.original_book_csv

        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)


# -----------------------------------------------------------------------
# 1. Library creation tests
# -----------------------------------------------------------------------
class TestLibraryCreation(TestSetup):
    """Test creating libraries."""

    def test_add_single_library(self):
        manager = LibraryManager()
        success, msg = manager.add_library("L1", "City Library")
        self.assertTrue(success)
        self.assertIn("Success", msg)
        self.assertEqual(len(manager.get_all_libraries()), 1)

    def test_add_multiple_libraries(self):
        manager = LibraryManager()
        manager.add_library("L1", "City Library")
        manager.add_library("L2", "Town Library")
        manager.add_library("L3", "School Library")
        self.assertEqual(len(manager.get_all_libraries()), 3)

    def test_duplicate_library_id(self):
        manager = LibraryManager()
        manager.add_library("L1", "City Library")
        success, msg = manager.add_library("L1", "Another Library")
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_duplicate_library_id_case_insensitive(self):
        manager = LibraryManager()
        manager.add_library("L1", "City Library")
        success, msg = manager.add_library("l1", "Another Library")
        self.assertFalse(success)

    def test_empty_library_id(self):
        manager = LibraryManager()
        success, msg = manager.add_library("", "Empty ID Library")
        self.assertFalse(success)
        self.assertIn("empty", msg.lower())

    def test_empty_library_name(self):
        manager = LibraryManager()
        success, msg = manager.add_library("L1", "")
        self.assertFalse(success)
        self.assertIn("empty", msg.lower())

    def test_whitespace_only_inputs(self):
        manager = LibraryManager()
        success, msg = manager.add_library("   ", "Test")
        self.assertFalse(success)


# -----------------------------------------------------------------------
# 2. Book creation tests
# -----------------------------------------------------------------------
class TestBookCreation(TestSetup):
    """Test adding books to libraries."""

    def _setup_library(self, manager):
        """Helper to add a library."""
        manager.add_library("L1", "City Library")

    def test_add_single_book(self):
        manager = LibraryManager()
        self._setup_library(manager)
        success, msg = manager.add_book("B1", "Python 101", "Author A", "111-222", "2023", "L1")
        self.assertTrue(success)
        self.assertIn("Success", msg)

    def test_add_multiple_books(self):
        manager = LibraryManager()
        self._setup_library(manager)
        manager.add_book("B1", "Python 101", "Author A", "111-222", "2023", "L1")
        manager.add_book("B2", "Java 101", "Author B", "333-444", "2022", "L1")
        manager.add_book("B3", "C++ Guide", "Author C", "555-666", "2021", "L1")
        self.assertEqual(len(manager.get_all_books()), 3)

    def test_add_books_to_different_libraries(self):
        manager = LibraryManager()
        manager.add_library("L1", "City Library")
        manager.add_library("L2", "Town Library")
        manager.add_book("B1", "Book One", "Auth A", "111", "2020", "L1")
        manager.add_book("B2", "Book Two", "Auth B", "222", "2021", "L2")
        self.assertEqual(len(manager.get_books_by_library("L1")), 1)
        self.assertEqual(len(manager.get_books_by_library("L2")), 1)

    def test_duplicate_book_id(self):
        manager = LibraryManager()
        self._setup_library(manager)
        manager.add_book("B1", "Book One", "Auth A", "111", "2020", "L1")
        success, msg = manager.add_book("B1", "Book Two", "Auth B", "222", "2021", "L1")
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    def test_book_to_nonexistent_library(self):
        manager = LibraryManager()
        success, msg = manager.add_book("B1", "Book", "Author", "123", "2020", "L999")
        self.assertFalse(success)
        self.assertIn("does not exist", msg)

    def test_empty_book_fields(self):
        manager = LibraryManager()
        self._setup_library(manager)
        success, _ = manager.add_book("", "Title", "Auth", "123", "2020", "L1")
        self.assertFalse(success)
        success, _ = manager.add_book("B1", "", "Auth", "123", "2020", "L1")
        self.assertFalse(success)
        success, _ = manager.add_book("B1", "Title", "", "123", "2020", "L1")
        self.assertFalse(success)

    def test_invalid_publication_year(self):
        manager = LibraryManager()
        self._setup_library(manager)
        success, msg = manager.add_book("B1", "Title", "Auth", "123", "abcd", "L1")
        self.assertFalse(success)
        self.assertIn("number", msg.lower())

    def test_publication_year_out_of_range(self):
        manager = LibraryManager()
        self._setup_library(manager)
        success, _ = manager.add_book("B1", "Title", "Auth", "123", "500", "L1")
        self.assertFalse(success)
        success, _ = manager.add_book("B2", "Title", "Auth", "123", "2200", "L1")
        self.assertFalse(success)


# -----------------------------------------------------------------------
# 3. Viewing and searching tests
# -----------------------------------------------------------------------
class TestViewAndSearch(TestSetup):
    """Test viewing and searching books."""

    def _populate(self, manager):
        """Add sample data."""
        manager.add_library("L1", "City Library")
        manager.add_library("L2", "Town Library")
        manager.add_book("B1", "Learn Python", "Guido", "111-222", "2020", "L1")
        manager.add_book("B2", "Java Basics", "James", "333-444", "2019", "L1")
        manager.add_book("B3", "Web Design", "Alice", "555-666", "2021", "L2")

    def test_view_books_by_library(self):
        manager = LibraryManager()
        self._populate(manager)
        books = manager.get_books_by_library("L1")
        self.assertEqual(len(books), 2)

    def test_view_all_books(self):
        manager = LibraryManager()
        self._populate(manager)
        self.assertEqual(len(manager.get_all_books()), 3)

    def test_search_by_title(self):
        manager = LibraryManager()
        self._populate(manager)
        results = manager.search_books("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Learn Python")

    def test_search_by_author(self):
        manager = LibraryManager()
        self._populate(manager)
        results = manager.search_books("Guido")
        self.assertEqual(len(results), 1)

    def test_search_by_isbn(self):
        manager = LibraryManager()
        self._populate(manager)
        results = manager.search_books("555-666")
        self.assertEqual(len(results), 1)

    def test_search_case_insensitive(self):
        manager = LibraryManager()
        self._populate(manager)
        results = manager.search_books("python")
        self.assertEqual(len(results), 1)

    def test_search_no_results(self):
        manager = LibraryManager()
        self._populate(manager)
        results = manager.search_books("Nonexistent")
        self.assertEqual(len(results), 0)

    def test_format_library_table_empty(self):
        output = LibraryManager.format_library_table([])
        self.assertIn("No libraries found", output)

    def test_format_book_table_empty(self):
        manager = LibraryManager()
        output = manager.format_book_table([])
        self.assertIn("No books found", output)


# -----------------------------------------------------------------------
# 4. Persistence tests
# -----------------------------------------------------------------------
class TestPersistence(TestSetup):
    """Test that data survives across LibraryManager reloads."""

    def test_library_persistence(self):
        # Create data with one manager instance
        manager1 = LibraryManager()
        manager1.add_library("L1", "Persistent Library")

        # Reload from CSV with a new instance
        manager2 = LibraryManager()
        libs = manager2.get_all_libraries()
        self.assertEqual(len(libs), 1)
        self.assertEqual(libs[0]["library_name"], "Persistent Library")

    def test_book_persistence(self):
        manager1 = LibraryManager()
        manager1.add_library("L1", "Lib")
        manager1.add_book("B1", "Persistent Book", "Author", "999", "2023", "L1")

        manager2 = LibraryManager()
        books = manager2.get_all_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "Persistent Book")


# -----------------------------------------------------------------------
# 5. CSV edge-case tests
# -----------------------------------------------------------------------
class TestCSVEdgeCases(TestSetup):
    """Test handling of missing / empty CSV files."""

    def test_missing_data_directory(self):
        """LibraryManager should work even if data/ does not exist yet."""
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        manager = LibraryManager()
        self.assertEqual(len(manager.get_all_libraries()), 0)
        self.assertEqual(len(manager.get_all_books()), 0)

    def test_empty_csv_files(self):
        """Overwrite CSVs with empty content and ensure graceful handling."""
        os.makedirs(self.test_data_dir, exist_ok=True)
        open(csv_storage.LIBRARIES_CSV, "w").close()
        open(csv_storage.BOOKS_CSV, "w").close()

        manager = LibraryManager()
        self.assertEqual(len(manager.get_all_libraries()), 0)
        self.assertEqual(len(manager.get_all_books()), 0)

    def test_load_and_save_roundtrip(self):
        """Save data and load it back to verify CSV roundtrip integrity."""
        libs = [{"library_id": "X1", "library_name": "Roundtrip Lib"}]
        csv_storage.save_libraries(libs)
        loaded = csv_storage.load_libraries()
        self.assertEqual(loaded, libs)


if __name__ == "__main__":
    unittest.main()
