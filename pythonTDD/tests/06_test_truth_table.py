import unittest
import truth_table


class TestUnaryOperations(unittest.TestCase):

    def test_logical_true(self):
        self.assertTrue(truth_table.TruthTable().logical_true(True))
        self.assertTrue(truth_table.TruthTable().logical_true(False))

    def test_logical_false(self):
        self.assertFalse(
            truth_table.TruthTable().logical_false(True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_false(False)
        )

    def test_logical_identity(self):
        self.assertTrue(
            truth_table.TruthTable().logical_identity(True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_identity(False)
        )

    def test_logical_negation(self):
        self.assertFalse(
            truth_table.TruthTable().logical_negation(True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_negation(False)
        )


class TestBinaryOperations(unittest.TestCase):

    def test_logical_conjunction(self):
        self.assertTrue(
            truth_table.TruthTable().logical_conjunction(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_conjunction(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_conjunction(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_conjunction(False, False)
        )

    def test_logical_disjunction(self):
        self.assertTrue(
            truth_table.TruthTable().logical_disjunction(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_disjunction(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_disjunction(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_disjunction(False, False)
        )

    def test_logical_implication_aka_material_implication(self):
        self.assertTrue(
            truth_table.TruthTable().logical_implication(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_implication(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_implication(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_implication(False, False)
        )

    def test_logical_equality_aka_logical_biconditional_aka_xnor(self):
        self.assertTrue(
            truth_table.TruthTable().logical_equality(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_equality(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_equality(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_equality(False, False)
        )

    def test_exclusive_disjunction(self):
        self.assertFalse(
            truth_table.TruthTable().exclusive_disjunction(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().exclusive_disjunction(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().exclusive_disjunction(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().exclusive_disjunction(False, False)
        )

    def test_logical_nand(self):
        self.assertFalse(
            truth_table.TruthTable().logical_nand(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_nand(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_nand(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_nand(False, False)
        )

    def test_logical_nor(self):
        self.assertFalse(
            truth_table.TruthTable().logical_nor(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_nor(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().logical_nor(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().logical_nor(False, False)
        )

    def test_converse_nonimplication(self):
        self.assertFalse(
            truth_table.TruthTable().converse_nonimplication(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().converse_nonimplication(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().converse_nonimplication(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().converse_nonimplication(False, False)
        )

    def test_material_nonimplication(self):
        self.assertFalse(
            truth_table.TruthTable().material_nonimplication(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().material_nonimplication(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().material_nonimplication(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().material_nonimplication(False, False)
        )

    def test_negate_first(self):
        self.assertFalse(
            truth_table.TruthTable().negate_first(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().negate_first(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().negate_first(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().negate_first(False, False)
        )

    def test_negate_second(self):
        self.assertFalse(
            truth_table.TruthTable().negate_second(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().negate_second(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().negate_second(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().negate_second(False, False)
        )

    def test_project_second(self):
        self.assertTrue(
            truth_table.TruthTable().project_second(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().project_second(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().project_second(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().project_second(False, False)
        )

    def test_project_first(self):
        self.assertTrue(
            truth_table.TruthTable().project_first(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().project_first(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().project_first(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().project_first(False, False)
        )

    def test_converse_implication(self):
        self.assertTrue(
            truth_table.TruthTable().converse_implication(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().converse_implication(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().converse_implication(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().converse_implication(False, False)
        )

    def test_tautology(self):
        self.assertTrue(
            truth_table.TruthTable().tautology(True, True)
        )
        self.assertTrue(
            truth_table.TruthTable().tautology(True, False)
        )
        self.assertTrue(
            truth_table.TruthTable().tautology(False, True)
        )
        self.assertTrue(
            truth_table.TruthTable().tautology(False, False)
        )

    def test_contradiction(self):
        self.assertFalse(
            truth_table.TruthTable().contradiction(True, True)
        )
        self.assertFalse(
            truth_table.TruthTable().contradiction(True, False)
        )
        self.assertFalse(
            truth_table.TruthTable().contradiction(False, True)
        )
        self.assertFalse(
            truth_table.TruthTable().contradiction(False, False)
        )

if __name__ == "__main__":
    unittest.main()