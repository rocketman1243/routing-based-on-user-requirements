from path_calculator import calculate_paths
import os
import json
from types import SimpleNamespace

# Read in PRO objects
pro_objects = []

for _, _, filenames in os.walk("pro_files/"):
    for filename in filenames:
        with open("pro_files/" + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)


pro = pro_objects[15]
calculate_paths("nio_files/", pro)