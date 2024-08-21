import sys
import os
import unittest

# Manually specifying the path to the src directory
# The src directory contains the log_tagger.py module which we need to import
src_dir = os.path.abspath(os.path.join(os.getcwd(), '../src'))
sys.path.insert(0, src_dir)

from log_tagger import LogTagger

class TestLogTagger(unittest.TestCase):

    def setUp(self):
        # Using absolute paths to reference the files in the src directory
        self.lookup_filename = os.path.join(src_dir, 'lookup.txt')
        self.logs_filename = os.path.join(src_dir, 'sampleFlowLogs.txt')
        self.output_filename = os.path.join(src_dir, 'output_test')

    def test_lookup_file_not_found(self):
        """Test case for handling nonexistent lookup files.
        It checks that the lookup table is empty when the file is not found.
        """
        log_tagger = LogTagger('nonexistent_lookup.txt')
        self.assertEqual(log_tagger.lookup, {}, "Lookup table should be empty if file not found")

    def test_logs_file_not_found(self):
        """Test case for handling nonexistent logs files.
        It ensures that a FileNotFoundError is raised when the log file does not exist.
        """
        log_tagger = LogTagger(self.lookup_filename)
        with self.assertRaises(FileNotFoundError):
            log_tagger.apply_tags_to_logs('nonexistent_logs.txt', self.output_filename)

    def test_valid_logs_processing(self):
        """Test case for processing logs with a valid lookup file.
        It checks that the output files are created and contain the expected number of lines.
        """
        log_tagger = LogTagger(self.lookup_filename)
        log_tagger.apply_tags_to_logs(self.logs_filename, self.output_filename)

        self.assertTrue(os.path.exists(self.output_filename + '.csv'), "Output file should exist")

        # Check the number of lines in the tag counts output file
        with open(self.output_filename + '_tag_counts.csv', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 5)  # Header + 4 tags

        # Check the number of lines in the port/protocol counts output file
        with open(self.output_filename + '_port_protocol_counts.csv', 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 15)  # Header + 14 port/protocol combinations

if __name__ == '__main__':
    unittest.main()