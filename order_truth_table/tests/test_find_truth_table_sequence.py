import io
import sys
import unittest
import unittest.mock
import find_truth_table_sequence


class TestTruthTableSequenceFinder(unittest.TestCase):

    def test_hamming_distance(self):
        """Test the hamming_distance function."""
        self.assertEqual(find_truth_table_sequence.hamming_distance(0b0000, 0b0000), 0)
        self.assertEqual(find_truth_table_sequence.hamming_distance(0b0000, 0b0001), 1)
        self.assertEqual(find_truth_table_sequence.hamming_distance(0b0000, 0b0011), 2)
        self.assertEqual(find_truth_table_sequence.hamming_distance(0b1010, 0b0101), 4)
        self.assertEqual(find_truth_table_sequence.hamming_distance(0b1111, 0b0000), 4)

    def test_get_neighbors(self):
        """Test the find_truth_table_sequence.get_neighbors function."""
        # Test with pattern 0000 and all patterns available
        neighbors = find_truth_table_sequence.get_neighbors(0b0000, set(range(16)))
        expected = [0b0001, 0b0010, 0b0100, 0b1000]  # Patterns that differ by 1 bit
        self.assertEqual(sorted(neighbors), sorted(expected))

        # Test with pattern 1010 and a subset of patterns available
        available = {0b0010, 0b1000, 0b1011, 0b1110}
        neighbors = find_truth_table_sequence.get_neighbors(0b1010, available)
        expected = [0b0010, 0b1000, 0b1011, 0b1110]  # Available patterns that differ by 1 bit
        self.assertEqual(sorted(neighbors), sorted(expected))

    def test_get_changed_bit_position(self):
        """Test the find_truth_table_sequence.get_changed_bit_position function."""
        self.assertEqual(find_truth_table_sequence.get_changed_bit_position(0b0000, 0b0001), 0)
        self.assertEqual(find_truth_table_sequence.get_changed_bit_position(0b0000, 0b0010), 1)
        self.assertEqual(find_truth_table_sequence.get_changed_bit_position(0b0000, 0b0100), 2)
        self.assertEqual(find_truth_table_sequence.get_changed_bit_position(0b0000, 0b1000), 3)
        self.assertEqual(find_truth_table_sequence.get_changed_bit_position(0b1010, 0b1011), 0)

    def test_get_operation_index(self):
        """Test the get_operation_index function."""
        sequence = [0b1100, 0b1000, 0b1010, 0b0010]
        self.assertEqual(find_truth_table_sequence.get_operation_index(0b1100, sequence), 0)
        self.assertEqual(find_truth_table_sequence.get_operation_index(0b1000, sequence), 1)
        self.assertEqual(find_truth_table_sequence.get_operation_index(0b0010, sequence), 3)
        self.assertEqual(find_truth_table_sequence.get_operation_index(0b0000, sequence), -1)  # Not in sequence

    def test_check_conjunction_early(self):
        """Test the check_conjunction_early function."""
        # Conjunction at position 2 (index 1) - valid
        sequence = [0b0000, 0b1000, 0b1010]
        self.assertTrue(find_truth_table_sequence.check_conjunction_early(sequence))

        # Conjunction at position 5 (index 4) - invalid
        sequence = [0b0000, 0b0001, 0b0011, 0b0010, 0b1000]
        self.assertFalse(find_truth_table_sequence.check_conjunction_early(sequence))

        # No conjunction in sequence - implicitly valid
        sequence = [0b0000, 0b0001, 0b0011]
        self.assertTrue(find_truth_table_sequence.check_conjunction_early(sequence))

    def test_check_disjunction_after_conjunction(self):
        """Test the check_disjunction_after_conjunction function."""
        # Disjunction after conjunction - valid
        sequence = [0b0000, 0b1000, 0b1100, 0b1110]
        self.assertTrue(find_truth_table_sequence.check_disjunction_after_conjunction(sequence))

        # Disjunction before conjunction - invalid
        sequence = [0b0000, 0b1110, 0b1100, 0b1000]
        self.assertFalse(find_truth_table_sequence.check_disjunction_after_conjunction(sequence))

        # Only conjunction, no disjunction - valid
        sequence = [0b0000, 0b1000, 0b1100]
        self.assertTrue(find_truth_table_sequence.check_disjunction_after_conjunction(sequence))

        # Only disjunction, no conjunction - valid
        sequence = [0b0000, 0b1100, 0b1110]
        self.assertTrue(find_truth_table_sequence.check_disjunction_after_conjunction(sequence))

    def test_check_or_ops_after_disjunction(self):
        """Test the find_truth_table_sequence.check_or_ops_after_disjunction function."""
        # OR operations after disjunction - valid
        sequence = [0b0000, 0b1000, 0b1110, 0b1101, 0b1001]
        valid, violations = find_truth_table_sequence.check_or_ops_after_disjunction(sequence)
        self.assertTrue(valid)
        self.assertEqual(violations, [])

        # OR operation before disjunction - invalid
        sequence = [0b0000, 0b1000, 0b1001, 0b1110]
        valid, violations = find_truth_table_sequence.check_or_ops_after_disjunction(sequence)
        self.assertFalse(valid)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0][0], 0b1001)  # Logical equality appears before disjunction

        # No disjunction in sequence - valid
        sequence = [0b0000, 0b1000, 0b1001]
        valid, violations = find_truth_table_sequence.check_or_ops_after_disjunction(sequence)
        self.assertTrue(valid)
        self.assertEqual(violations, [])

    def test_check_constraints(self):
        """Test the check_constraints function."""
        # Valid sequence
        sequence = [0b0000, 0b1000, 0b1100, 0b1110, 0b1111, 0b1101]
        violations = find_truth_table_sequence.check_constraints(sequence)
        self.assertEqual(violations, [])

        # Invalid: conjunction not early
        sequence = [0b0000, 0b0001, 0b0011, 0b0010, 0b1010, 0b1000]
        violations = find_truth_table_sequence.check_constraints(sequence)
        self.assertTrue(any("Conjunction not appearing early" in v for v in violations))

        # Invalid: disjunction before conjunction
        sequence = [0b0000, 0b1100, 0b1110, 0b1010, 0b1000]
        violations = find_truth_table_sequence.check_constraints(sequence)
        self.assertTrue(any("Disjunction appearing before conjunction" in v for v in violations))

        # Invalid: OR operation before disjunction
        sequence = [0b0000, 0b1000, 0b1001, 0b1101, 0b1111, 0b1110]
        violations = find_truth_table_sequence.check_constraints(sequence)
        self.assertTrue(any("OR operation" in v and "before disjunction" in v for v in violations))

    def test_try_next_pattern(self):
        """Test the try_next_pattern function."""
        # Simple case with no constraints
        sequence = [0b0000]
        unused = {0b0001, 0b0010, 0b0100, 0b1000}
        next_pattern = find_truth_table_sequence.try_next_pattern(sequence, unused, depth=10)
        self.assertIn(next_pattern, unused)
        self.assertEqual(find_truth_table_sequence.hamming_distance(sequence[-1], next_pattern), 1)

        # Case with constraints but early in sequence (flexible)
        sequence = [0b0000, 0b1000, 0b1110]  # Disjunction before conjunction should fail later
        unused = {0b1111, 0b1010}
        next_pattern = find_truth_table_sequence.try_next_pattern(sequence, unused, depth=2)
        self.assertIsNotNone(next_pattern)  # Should work due to flexibility in early steps

        # Case with constraints later in sequence (strict)
        sequence = [0b0000, 0b0001, 0b0011, 0b0010, 0b0110, 0b1110, 0b1010]  # Disjunction before conjunction
        unused = {0b1000}  # Trying to add conjunction after disjunction
        next_pattern = find_truth_table_sequence.try_next_pattern(sequence, unused, depth=10)
        self.assertIsNone(next_pattern)  # Should fail due to constraint violation

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_step_info(self, mock_stdout):
        """Test the print_step_info function."""
        sequence = [0b0000, 0b1000]
        find_truth_table_sequence.print_step_info(sequence, 1)
        output = mock_stdout.getvalue()

        self.assertIn("TFFF", output)  # Should contain the pattern bits
        self.assertIn("conjunction", output)  # Should contain the operation name
        self.assertIn("Changed bit at position 3", output)  # Should show which bit changed

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_constraint_verification(self, mock_stdout):
        """Test the print_constraint_verification function."""
        # Sequence with a constraint violation
        sequence = [0b0000, 0b1000, 0b1001, 0b1101, 0b1111, 0b1110]
        find_truth_table_sequence.print_constraint_verification(sequence)
        output = mock_stdout.getvalue()

        self.assertIn("Conjunction appears at position 2", output)
        self.assertIn("Disjunction appears at position 6", output)
        self.assertIn("VIOLATION", output)  # Should detect the OR operations appearing before disjunction

    def test_end_to_end(self):
        """Test that the full algorithm produces a valid sequence."""
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            sequence = find_truth_table_sequence.find_truth_table_sequence()
            output = mock_stdout.getvalue()  # Capture the output
        self.assertIsNotNone(sequence)
        self.assertEqual(len(sequence), 16)  # Still testing with 8
        # self.assertEqual(len(sequence), 8)  # Still testing with 8
        for i in range(1, len(sequence)):
            self.assertEqual(find_truth_table_sequence.hamming_distance(sequence[i-1], sequence[i]), 1)
        self.assertEqual(len(set(sequence)), len(sequence))  # Unique steps
        self.assertTrue(output)  # Ensure there’s some output
        # Force output to terminal
        print(f"Test output:\n{output}")

if __name__ == '__main__':
    unittest.main()