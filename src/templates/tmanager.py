from jinja2 import Environment, FileSystemLoader
import os
import random
import logging

logger = logging.getLogger(__name__)

class TManager:
    def __init__(self, template_dir=None):
        if template_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_dir = script_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template_dir = template_dir

    def get_template_variations(self, template_name):
        template_path = os.path.join(self.template_dir, template_name)
        try:
            variations = [f for f in os.listdir(template_path) if f.endswith('.j2')]
            if not variations:
                logger.warning(f"No template variations found in '{template_name}'.")
            else:
                logger.debug(f"Found {len(variations)} variations for '{template_name}'.")
            return variations
        except FileNotFoundError:
            logger.error(f"The directory '{template_name}' is not found.")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while getting variations for '{template_path}'.")
            return []

        # if not os.path.exists(template_path):
        #     raise FileNotFoundError(f"The directory '{template_name}' is not found.")
        # return [f for f in os.listdir(template_path) if f.endswith('.j2')]
    
    def render_random_template(self, template_name, context):
        variations = self.get_template_variations(template_name)
        if not variations:
            logger.warning(f"No template variations found in '{template_name}'.")
            return ""
        
        selected_template = random.choice(variations)
        logger.debug(f"Selected template: {selected_template} for template {template_name}.")

        try:
            template = self.env.get_template(os.path.join(template_name, selected_template))
            rendered = template.render(context)
            logger.debug(f"Successfully rendered random template for {template_name}.")
            return rendered
        except Exception as e:
            logger.error(f"Error rendering random template for {template_name}.")
            return ""
    
    def render_all_templates(self, template_name, context):
        variations = self.get_template_variations(template_name)
        rendered_outputs = []

        for template_file in variations:
            try:
                template = self.env.get_template(os.path.join(template_name, template_file))
                rendered = template.render(context)
                rendered_outputs.append(rendered)
            except Exception as e:
                logger.error(f"Error rendering template {template_file} for {template_name}: {e}")

        logger.info(f"Rendered {len(rendered_outputs)} of {len(variations)} templates for {template_name}.")
        return rendered_outputs

    def render_template(self, template_name, context):
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(context)
            logger.debug(f"Successfully rendered static template {template_name}.")
            return rendered
        except Exception as e:
            logger.error(f"Error rendering static template {template_name}: {e}")
            return ""
