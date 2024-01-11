from base_factory import BaseFactory
import os

class ManifestFactory(BaseFactory):
    def __init__(self, environment_name, context):
        self.environment_name = environment_name
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/') + 'copilot/environments/' + environment_name + '/'
        super().__init__(
            output_file=prefix + 'manifest.yml',
            overwrites_files=[prefix + 'manifest.yaml', prefix + 'manifest.yml'],
            template_file=os.path.dirname(os.path.realpath(__file__)) + '/template.yml.jinja',
            context=context
        )
