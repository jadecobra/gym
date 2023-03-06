import unittest
import jadecobra.toolkit


class TestTemplates(jadecobra.toolkit.TestCase):

    def test_template(self):
        self.create_cdk_templates()
        self.assert_cdk_templates_equal('EcsFlask')