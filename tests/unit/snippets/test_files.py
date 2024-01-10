import unittest
from pyiron_workflow.snippets.files import DirectoryObject, FileObject
from pathlib import Path


class TestFiles(unittest.TestCase):
    def setUp(cls):
        cls.directory = DirectoryObject("test")

    def tearDown(cls):
        cls.directory.delete()

    def test_directory_exists(self):
        self.assertTrue(Path("test").exists() and Path("test").is_dir())

    def test_write(self):
        self.directory.write(file_name="test.txt", content="something")
        self.assertTrue(self.directory.file_exists("test.txt"))
        self.assertTrue(
            "test/test.txt" in [
                ff.replace("\\", "/")
                for ff in self.directory.list_content()['file']
            ]
        )
        self.assertEqual(len(self.directory), 1)

    def test_create_subdirectory(self):
        self.directory.create_subdirectory("another_test")
        self.assertTrue(Path("test/another_test").exists())

    def test_path(self):
        f = FileObject("test.txt", self.directory)
        self.assertEqual(str(f.path).replace("\\", "/"), "test/test.txt")

    def test_read_and_write(self):
        f = FileObject("test.txt", self.directory)
        f.write("something")
        self.assertEqual(f.read(), "something")

    def test_is_file(self):
        f = FileObject("test.txt", self.directory)
        self.assertFalse(f.is_file())
        f.write("something")
        self.assertTrue(f.is_file())
        f.delete()
        self.assertFalse(f.is_file())

    def test_is_empty(self):
        self.assertTrue(self.directory.is_empty)
        self.directory.write(file_name="test.txt", content="something")
        self.assertFalse(self.directory.is_empty)

    def test_delete(self):
        self.assertTrue(
            Path("test").exists() and Path("test").is_dir(),
            msg="Sanity check on initial state"
        )
        self.directory.write(file_name="test.txt", content="something")
        self.directory.delete(only_if_empty=True)
        self.assertFalse(
            self.directory.is_empty,
            msg="Flag argument on delete should have prevented removal"
        )
        self.directory.delete()
        self.assertFalse(
            Path("test").exists(),
            msg="Delete should remove the entire directory"
        )
        self.directory = DirectoryObject("test")  # Rebuild it so the tearDown works


if __name__ == '__main__':
    unittest.main()
