import io
from unittest import TestCase

from s_o.recognizer.params import parse_config, Configuration, WrongConfigurationError

CORRECT_YAML = '''confidence_threshold: 0.4
duration: 15000
fragments: 15
next_phrase_timeout: 3000
working_directory: /tmp
'''

INCORRECT_YAML = '''
fragments: 15
next_phrase_timeout: 3000
working_directory: /tmp
'''



class TestParse_config(TestCase):

    def test_parse_config_works_as_expected(self):
        file = io.StringIO(CORRECT_YAML)
        configuration = parse_config(file)
        self.assertEqual(
            configuration,
            Configuration(0.4, 15000, 3000)
        )

    def test_parse_config_fails(self):
        file = io.StringIO(INCORRECT_YAML)
        with self.assertRaises(WrongConfigurationError):
            configuration = parse_config(file)
            print(configuration)
