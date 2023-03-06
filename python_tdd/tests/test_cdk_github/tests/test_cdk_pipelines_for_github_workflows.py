import jadecobra.toolkit

class TestCDKPipelinesGitHub(jadecobra.toolkit.TestCase):

    def test_failure(self):
        self.create_cdk_templates()
        self.assert_cdk_templates_equal('CdkPipelinesGitHub')
