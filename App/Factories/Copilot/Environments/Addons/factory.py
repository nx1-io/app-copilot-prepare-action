from base_factory import BaseFactory
import os

class AddonFactory(BaseFactory):
    def __init__(self, addon, environments, shared_data):
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/') + 'copilot/environments/' + '/addons/'
        output_filename = addon['name'] + '.yml'
        template_dir = os.path.dirname(os.path.realpath(__file__)) + '/catalog/' + addon['blueprint']['name'] + '/'
        template_filepath = template_dir + 'template.yml.jinja'

        service_override_filepath = template_dir + 'service_overrides.yml.jinja'
        if os.path.isfile(service_override_filepath):
            service_overrides = super().__init__(template_file=service_override_filepath, context={'addon': addon})._render_and_load()
            shared_data['service_overrides'].append(service_overrides)

        super().__init__(
            output_file=prefix + output_filename,
            overwrites_files=[prefix + output_filename, prefix + addon['name'] + '.yaml'],
            template_file=template_filepath,
            context={
                'addon': addon,
                'environments': environments,
            }
        )