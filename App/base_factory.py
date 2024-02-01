from template_handler import TemplateHandler
import os
from ruamel.yaml import YAML
from mergedeep import merge

yaml = YAML()

class BaseFactory:
    def __init__(self, context=None, output_file=None, overwrites_files=None, template_file=None, overwrite_as_list=False, overwrites=[]):
        self.context = context
        self.output_file = output_file
        self.overwrites_files = overwrites_files
        self.template_file = template_file
        self.overwrite_as_list = overwrite_as_list
        self.overwrites = overwrites
        yaml.allow_duplicate_keys = True

        return self

    def _render_and_load(self):
        return yaml.load(TemplateHandler(self.template_file).set_context(self.context).render())

    def _merge(self, rendered_template):
        overwrites = {}

        if self.overwrites_files is None or len([x for x in self.overwrites_files if os.path.isfile(x)]) == 0:
            return rendered_template

        with open([x for x in self.overwrites_files if os.path.isfile(x)][0], 'r') as file:
            overwrites = yaml.load(file.read())

        if self.overwrite_as_list:
            if isinstance(overwrites, list) and isinstance(rendered_template, list):
                return overwrites + rendered_template
            else:
                return rendered_template

        return merge(rendered_template, overwrites)

    def _merge_overwrites(self, content):
        for overwrite in self.overwrites:
            content = merge(content, overwrite)

        return content

    def build(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        yaml.indent(mapping=2, sequence=4, offset=2)

        content = self._merge(self._render_and_load())
        content = self._merge_overwrites(content)

        with open(self.output_file, 'w') as file:
            yaml.dump(content, file)
