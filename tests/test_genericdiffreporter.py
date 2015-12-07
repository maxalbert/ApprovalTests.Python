import json
import os
import unittest

from approvaltests.Approvals import verify
from approvaltests.GenericDiffReporterFactory import GenericDiffReporterFactory
from approvaltests.Namer import Namer


class GenericDiffReporterTests(unittest.TestCase):
    def setUp(self):
        self.factory = GenericDiffReporterFactory()
        self.reporter = self.factory.get('BeyondCompare4')

    def test_list_configured_reporters(self):
        verify(json.dumps(self.factory.list(), sort_keys=True, indent=4), self.reporter)

    def test_get_reporter(self):
        verify(str(self.factory.get("BeyondCompare4")), self.reporter)

    def test_get_winmerge(self):
        verify(str(self.factory.get("WinMerge")), self.factory.get("WinMerge"))

    def test_constructs_valid_diff_command(self):
        reporter = self.factory.get("BeyondCompare4")
        namer = Namer(1)
        received = namer.get_received_filename()
        approved = namer.get_approved_filename()
        command = reporter.get_command(
            received,
            approved
        )
        expected_command = [
            reporter.path,
            received,
            approved
        ]
        self.assertEqual(command, expected_command)

    def test_empty_approved_file_created_when_one_does_not_exist(self):
        namer = Namer(1)
        received = namer.get_received_filename()
        approved = namer.get_approved_filename()
        if os.path.isfile(approved):
            os.remove(approved)
        self.assertFalse(os.path.isfile(approved))

        reporter = self.factory.get("BeyondCompare4")
        reporter.run_command = lambda command_array: None
        reporter.report(received, approved)
        self.assertEqual(0, os.stat(approved).st_size)

    def test_approved_file_not_changed_when_one_exists_already(self):
        namer = Namer(1)
        approved_contents = "Approved"
        approved = namer.get_approved_filename()
        os.remove(approved)
        with open(approved, 'w') as approved_file:
            approved_file.write(approved_contents)
        reporter = self.factory.get("BeyondCompare4")
        reporter.run_command = lambda command_array: None

        reporter.report(namer.get_received_filename(), approved)

        with open(approved, 'r') as approved_file:
            actual_contents = approved_file.read()
        self.assertEqual(actual_contents, approved_contents)