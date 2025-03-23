from jinja2 import Environment, FileSystemLoader
import os
import random
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TManager:
    def __init__(self, template_dir=None):
        if template_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_dir = script_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template_dir = template_dir

    def get_template_variations(self, template_name):
        template_path = os.path.join(self.template_dir, template_name)
        # try:
        #     variations = [f for f in os.listdir(template_path) if f.endswith('.j2')]
        #     if not variations:
        #         logger.warning(f"No template variations found in '{template_name}'.")
        #     else:
        #         logger.debug(f"Found {len(variations)} variations for '{template_name}'.")
        # except FileNotFoundError:
        #     logger.error(f"Template path not found: '{template_path}'.")
        #     return variations
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"The directory '{template_name}' is not found.")
        return [f for f in os.listdir(template_path) if f.endswith('.j2')]
    
    def render_random_template(self, template_name, context):
        variations = self.get_template_variations(template_name)
        selected_template = random.choice(variations)
        template = self.env.get_template(os.path.join(template_name, selected_template))
        return template.render(context)
    
    def render_all_templates(self, template_name, context):
        variations = self.get_template_variations(template_name)
        rendered_templates = []
        for template_file in variations:
            template = self.env.get_template(os.path.join(template_name, template_file))
            rendered_templates.append(template.render(context))
        return rendered_templates

    def render_template(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)
