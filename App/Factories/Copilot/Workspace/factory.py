from base_factory import BaseFactory
import os


class WorkspaceFactory(BaseFactory):
    def __init__(self, context):
        prefix = os.getenv('OUTPUT_PATH', '/github/workspace/')
        super().__init__(
            output_file=prefix + 'copilot/.workspace',
            template_file=os.path.dirname(os.path.realpath(__file__)) + '/template.jinja',
            context=context
        )
