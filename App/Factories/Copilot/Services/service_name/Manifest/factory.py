from base_factory import BaseFactory
import os

class ManifestFactory(BaseFactory):
    def __init__(self, service_name, context, shared_data):
        self.service_name = service_name
        self.context = context
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/') + 'copilot/' + service_name + '/'
        super().__init__(
            output_file=prefix + 'manifest.yml',
            overwrites_files=[prefix + 'manifest.yaml', prefix + 'manifest.yml'],
            overwrites=shared_data['addon_service_manifest_overrides'],
            template_file=self.build_template_path(os.path.dirname(os.path.realpath(__file__)) + '/'),
            context=self.context
        )


    def build_template_path(self, prefix = ''):
        match self.context['service']['type']:
            case 'CONTAINER_BACKEND':
                return prefix + 'backend_template.yml.jinja'
            case 'CONTAINER_LOAD_BALANCED':
                return prefix + 'load_balanced_template.yml.jinja'
            case 'STATIC_WEBSITE':
                return prefix + 'static_template.yml.jinja'
            case 'CONTAINER_SCHEDULED_JOB':
                return prefix + 'scheduled_job.yml.jinja'