from base_factory import BaseFactory
import os

class AddonFactory(BaseFactory):
    def __init__(self, addon, environments):
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/') + 'copilot/environments/' + '/addons/'
        output_filename = addon['name'] + '.yml'
        template_filepath = os.path.dirname(os.path.realpath(__file__)) + '/' + addon['blueprint']['name'] + '.yml.jinja'
        super().__init__(
            output_file=prefix + output_filename,
            overwrites_files=[prefix + output_filename, prefix + addon['name'] + '.yaml'],
            template_file=template_filepath,
            context={
                'addon': addon,
                'environments': environments,
            }
        )
