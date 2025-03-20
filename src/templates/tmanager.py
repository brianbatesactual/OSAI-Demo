from jinja2 import Environment, FileSystemLoader
import os

class TManager:
    def __init__(self, template_dir=None):
        if template_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_dir = script_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_template(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)
