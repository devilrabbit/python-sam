import yaml
import json
import sys

args = sys.argv
file = args[1]

with open(file, 'r') as yml:
    config = yaml.safe_load(yml)

paths = config['paths']

db = dict()
for path_key in paths:
    db[path_key] = dict()

    path = paths[path_key]
    for method_key in path:
        method = path[method_key]

        allows = None
        if 'security' in method:
            for security in method['security']:
                for security_key in security:
                    if security_key == 'customAuth':
                        allows = security[security_key]

        if allows == None:
            db[path_key][method_key.upper()] = ['public']
        else:
            db[path_key][method_key.upper()] = allows

with open('db.json', 'w') as f:
    json.dump(db, f)