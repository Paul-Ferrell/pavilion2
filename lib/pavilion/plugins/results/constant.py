from pavilion import result_parsers
import yaml_config as yc
import re

class Constant(result_parsers.ResultParser):
    """Set a constant as result."""

    def __init__(self):
        super().__init__(name='constant')

    def get_config_items(self):

        config_items = super().get_config_items()
        config_items.extend([
            yc.StrElem(
                'const', required=True,
                help_text="Constant that will be placed in result."
            )
        ])

        return config_items

    def _check_args(self, const=None):
        
        if const == "":
            raise result_parsers.ResultParserError(
                "Constant required."
        )

    def __call__(self, test, file, const=None):

        return const
