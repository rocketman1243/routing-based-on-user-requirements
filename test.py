from path_calculator import calculate_paths
import os
import json
from types import SimpleNamespace

# Read in PRO objects
pro_objects = []

pro_folder = "test_files/pro_files/"
for _, _, filenames in os.walk(pro_folder):
    for filename in filenames:
        with open(pro_folder + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)

pro = pro_objects[0]



calculate_paths("test_files/nio_files/", pro)