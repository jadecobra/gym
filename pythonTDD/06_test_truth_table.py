import unittest

from truth_table import TruthTable


class TestUnaryOperations(unittest.TestCase):

	def test_logical_true(self):
		self.assertTrue(TruthTable().logical_true(True))
		self.assertTrue(TruthTable().logical_true(False))

	def test_logical_false(self):
		self.assertFalse(TruthTable().logical_false(True))
		self.assertFalse(TruthTable().logical_false(False))

	def test_logical_identity(self):
		self.assertTrue(TruthTable().logical_identity(True))
		self.assertFalse(TruthTable().logical_identity(False))

	def test_logical_negation(self):
		self.assertFalse(TruthTable().logical_negation(True))
		self.assertTrue(TruthTable().logical_negation(False))


class TestBinaryOperations(unittest.TestCase):

	def test_logical_conjunction(self):
		self.assertTrue(TruthTable().logical_conjunction(True, True))
		self.assertFalse(TruthTable().logical_conjunction(True, False))
		self.assertFalse(TruthTable().logical_conjunction(False, True))
		self.assertFalse(TruthTable().logical_conjunction(False, False))

	def test_logical_disjunction(self):
		self.assertTrue(TruthTable().logical_disjunction(True, True))
		self.assertTrue(TruthTable().logical_disjunction(True, False))
		self.assertTrue(TruthTable().logical_disjunction(False, True))
		self.assertFalse(TruthTable().logical_disjunction(False, False))

	def test_logical_implication_aka_material_implication(self):
		self.assertTrue(TruthTable().logical_implication(True, True))
		self.assertFalse(TruthTable().logical_implication(True, False))
		self.assertTrue(TruthTable().logical_implication(False, True))
		self.assertTrue(TruthTable().logical_implication(False, False))

	def test_logical_equality_aka_logical_biconditional_aka_xnor(self):
		self.assertTrue(TruthTable().logical_equality(True, True))
		self.assertFalse(TruthTable().logical_equality(True, False))
		self.assertFalse(TruthTable().logical_equality(False, True))
		self.assertTrue(TruthTable().logical_equality(False, False))

	def test_exclusive_disjunction(self):
		self.assertFalse(TruthTable().exclusive_disjunction(True, True))
		self.assertTrue(TruthTable().exclusive_disjunction(True, False))
		self.assertTrue(TruthTable().exclusive_disjunction(False, True))
		self.assertFalse(TruthTable().exclusive_disjunction(False, False))

	def test_logical_nand(self):
		self.assertFalse(TruthTable().logical_nand(True, True))
		self.assertTrue(TruthTable().logical_nand(True, False))
		self.assertTrue(TruthTable().logical_nand(False, True))
		self.assertTrue(TruthTable().logical_nand(False, False))

	def test_logical_nor(self):
		self.assertFalse(TruthTable().logical_nor(True, True))
		self.assertFalse(TruthTable().logical_nor(True, False))
		self.assertFalse(TruthTable().logical_nor(False, True))
		self.assertTrue(TruthTable().logical_nor(False, False))

	def test_converse_nonimplication(self):
		self.assertFalse(TruthTable().converse_nonimplication(True, True))
		self.assertFalse(TruthTable().converse_nonimplication(True, False))
		self.assertTrue(TruthTable().converse_nonimplication(False, True))
		self.assertFalse(TruthTable().converse_nonimplication(False, False))

	def test_material_nonimplication(self):
		self.assertFalse(TruthTable().material_nonimplication(True, True))
		self.assertTrue(TruthTable().material_nonimplication(True, False))
		self.assertFalse(TruthTable().material_nonimplication(False, True))
		self.assertFalse(TruthTable().material_nonimplication(False, False))

	def test_negate_first(self):
		self.assertFalse(TruthTable().negate_first(True, True))
		self.assertFalse(TruthTable().negate_first(True, False))
		self.assertTrue(TruthTable().negate_first(False, True))
		self.assertTrue(TruthTable().negate_first(False, False))

	def test_negate_second(self):
		self.assertFalse(TruthTable().negate_second(True, True))
		self.assertTrue(TruthTable().negate_second(True, False))
		self.assertFalse(TruthTable().negate_second(False, True))
		self.assertTrue(TruthTable().negate_second(False, False))

	def test_project_second(self):
		self.assertTrue(TruthTable().project_second(True, True))
		self.assertFalse(TruthTable().project_second(True, False))
		self.assertTrue(TruthTable().project_second(False, True))
		self.assertFalse(TruthTable().project_second(False, False))

	def test_project_first(self):
		self.assertTrue(TruthTable().project_first(True, True))
		self.assertTrue(TruthTable().project_first(True, False))
		self.assertFalse(TruthTable().project_first(False, True))
		self.assertFalse(TruthTable().project_first(False, False))

	def test_converse_implication(self):
		self.assertTrue(TruthTable().converse_implication(True, True))
		self.assertTrue(TruthTable().converse_implication(True, False))
		self.assertFalse(TruthTable().converse_implication(False, True))
		self.assertTrue(TruthTable().converse_implication(False, False))

	def test_tautology(self):
		self.assertTrue(TruthTable().tautology(True, True))
		self.assertTrue(TruthTable().tautology(True, False))
		self.assertTrue(TruthTable().tautology(False, True))
		self.assertTrue(TruthTable().tautology(False, False))

	def test_contradiction(self):
		self.assertFalse(TruthTable().contradiction(True, True))
		self.assertFalse(TruthTable().contradiction(True, False))
		self.assertFalse(TruthTable().contradiction(False, True))
		self.assertFalse(TruthTable().contradiction(False, False))
