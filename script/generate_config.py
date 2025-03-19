from jinja2 import Environment, FileSystemLoader # type: ignore
import os 

def extract_variable_names(template_str):
    """Extract variable names from a Jinja2 template string."""
    env = Environment()
    parsed_content = env.parse(template_str)
    print(parsed_content.iter_child_nodes())
    
    variable_names = set()

    # Walk through the parsed nodes to find variable names
    for nodes in parsed_content.iter_child_nodes():
        for node in nodes.iter_child_nodes():
            for node in node.iter_fields():
                if node[0] == "name":
                    variable_names.add(node[1])

    return variable_names

env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('config.jinja2')

Dirname = os.path.dirname(__file__) # current directory
Filename = os.path.join(Dirname, '../src/config/config.yml') # relative path 
template_path = os.path.join(Dirname, './templates/config.jinja2')

with open(template_path, 'r') as file:
    template_content = file.read()

variable_names = extract_variable_names(template_content)
vars = {}
for i in variable_names:
    vars[i] = input(str(i)+": ")
    print(vars)
    vars.update(vars)
rendre = template.render(vars)

# write config
with open(Filename, 'w') as file:
    file.write(rendre)