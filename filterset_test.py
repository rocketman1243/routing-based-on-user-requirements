from filterset import Filterset
from collections import namedtuple

# https://stackoverflow.com/questions/36385035/python-syntax-for-namedtuple-inside-a-namedtuple
def dict2namedtuple(name, d):
    values, keys = [], []
    for k in d:
        keys.append(k)

        v = d[k]
        if isinstance(v, dict):
            values.append(dict2namedtuple(k, v))
        else:
            values.append(v)

    T = namedtuple(name, keys)
    return T(*values)

pro_dict = {
  "as_source": "1",
  "as_destination": "2",
  "privacy": {
    "strict": [1],
    "best_effort": [2, 3, 4],
    "best_effort_mode": "biggest_subset"
  },
  "security": {
    "strict": [  ],
    "best_effort": [ ],
    "best_effort_mode": "ordered_list"
  },
  "geolocation": {
    "exclude": [ "GB", "DE" ]
  },
  "path_optimization": "minimize_total_latency",
  "multipath": {
    "target_amount_of_paths": 1,
    "minimum_number_of_paths": 1
  }
}
pro = dict2namedtuple("pro", pro_dict)

nio_dict = {
  "as_number": "104",
  "geolocation": [ "US" ],
  "lat": "39.9110267765371",
  "lon": "-105.278285615138",
  "connections": [ "209", "14041" ],
  "privacy": [1, 2, 3],
  "security": []
} 
nio = dict2namedtuple("nio", nio_dict)

filterset = Filterset(pro)

print("as has to be dropped:", filterset.as_has_to_be_removed(nio, "best-effort", "verbose"))