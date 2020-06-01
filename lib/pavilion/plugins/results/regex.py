from pavilion.result import parsers

import pavilion.result.base
import yaml_config as yc
import re
import sre_constants


class Regex(parsers.ResultParser):
    """Find matches to the given regex in the given file. The matched string
    or strings are returned as the result."""

    def __init__(self):
        super().__init__(name='regex',
                         description="Find data using a basic regular "
                                     "expression.")
        self.range_re = re.compile('(-?[0-9]*\.?[0-9]*):(-?.*)')

    def get_config_items(self):

        config_items = super().get_config_items()
        config_items.extend([
            yc.StrElem(
                'regex', required=True,
                help_text="The python regex to use to search the given file. "
                          "See: 'https://docs.python.org/3/library/re.html' "
                          "You can use single quotes in YAML to have the "
                          "string interpreted literally. IE '\\n' is a '\\' "
                          "and an 'n'."
            ),
            parsers.MATCHES_ELEM,
        ])

        return config_items

    def _check_args(self, regex=None, match_type=None):

        try:
            re.compile(regex)
        except (ValueError, sre_constants.error) as err:
            raise pavilion.result.base.ResultError(
                "Invalid regular expression: {}".format(err))

    def __call__(self, test, file, regex=None, match_type=None):

        regex = re.compile(regex)

        matches = []

        for line in file.readlines():
            # Find all non-overlapping matches and return them as a list.
            # if more than one capture is used, list contains tuples of
            # captured strings.
            matches.extend(regex.findall(line))

        if match_type == parsers.MATCH_ALL:
            return matches
        elif match_type == parsers.MATCH_FIRST:
            return matches[0] if matches else None
        elif match_type == parsers.MATCH_LAST:
            return matches[-1] if matches else None
