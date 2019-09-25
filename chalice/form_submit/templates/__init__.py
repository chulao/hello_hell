import os
import jinja2

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    print("path: {}, filename: {}".format(path, filename))
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./")).get_template(filename).render(context)
    # return jinja2.Environment(loader=jinja2.FileSystemLoader("templates")).get_template(filename).render(context)