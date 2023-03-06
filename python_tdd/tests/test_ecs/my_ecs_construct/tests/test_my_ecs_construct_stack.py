import jadecobra.toolkit
import subprocess


class TestEcsConstruct(jadecobra.toolkit.TestCase):

    def test_ecs_construct(self):
        result = jadecobra.toolkit.time_it(
            subprocess.run,
            (
                'cdk ls '
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            ),
            description=f'cdk ls',
            shell=True,
            capture_output=True,
        )
        print(result.stderr.decode())
        print(result.stdout.decode())
        self.assertEqual(result.returncode, 0)

        self.assert_cdk_templates_equal('MyEcsConstructStack')