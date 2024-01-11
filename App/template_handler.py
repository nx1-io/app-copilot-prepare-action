from jinja2 import Environment, FileSystemLoader


class TemplateHandler:
    def __init__(self, template_file):
        self.template_file = template_file
        self.context = {}

    def load(self):
        with open(self.template_file, 'r') as file:
            return file.read()

    def render(self):
        yaml_template = self.load()

        template_dir = '.'
        env = Environment(loader=FileSystemLoader(template_dir))

        rendered_template = env.from_string(yaml_template).render(self.context)

        return rendered_template

    def set_context(self, context):
        self.context = context
        return self
