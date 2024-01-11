from base_factory import BaseFactory
import os


class CfnPatchesFactory(BaseFactory):
    def __init__(self, service_name, context, service_type = None):
        self.service_name = service_name
        self.service_type = service_type
        self.context = context
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/') + 'copilot/' + service_name + '/overrides/'
        super().__init__(
            output_file=prefix + 'cfn.patches.yml',
            overwrites_files=[prefix + 'cfn.patches.yml'],
            overwrite_as_list=True,
            template_file=self.build_template_path(),
            context=context
        )

    def build_template_path(self, template_prefix = os.path.dirname(os.path.realpath(__file__)) + '/'):
        match self.context['service']['type']:
            case 'STATIC_WEBSITE':
                return template_prefix + 'static_template.yml.jinja'
            case _:
                return template_prefix + 'default_template.yml.jinja'