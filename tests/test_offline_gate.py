"""Regression tests for fail-closed virtual demo evidence."""
import unittest
from scripts.verify_offline import verify_demo_output


class OfflineGateTests(unittest.TestCase):
    def test_expected_demo_outcome(self):
        output = "STATE: RETURN_HOME\nFAILSAFE: LOW_BATTERY\nFINAL STATE: FAILSAFE\n"
        self.assertTrue(verify_demo_output(output))

    def test_reject_unexpected_failure_reason(self):
        output = "FAILSAFE: GPS_UNSAFE\nFINAL STATE: FAILSAFE\n"
        self.assertFalse(verify_demo_output(output))

    def test_reject_normal_completion(self):
        output = "FINAL STATE: COMPLETE\n"
        self.assertFalse(verify_demo_output(output))

    def test_reject_substring_spoofing(self):
        output = "debug: FAILSAFE: LOW_BATTERY\nFINAL STATE: FAILSAFE_NOT_REAL\n"
        self.assertFalse(verify_demo_output(output))
