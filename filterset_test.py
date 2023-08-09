pro = {
  "as_source": "63872",
  "as_destination": "54222",
  "security": {
    "strict": [ 17, 26 ],
    "best_effort": [ 2, 3, 4 ],
    "best_effort_mode": "ordered_list"
  },
  "privacy": {
    "strict": [],
    "best_effort": [ 1, 2, 3 ],
    "best_effort_mode": "biggest_subset"
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

nio = {
  "as_number": "104",
  "geolocation": [ "US" ],
  "lat": "39.9110267765371",
  "lon": "-105.278285615138",
  "connections": [ "209", "14041" ],
  "privacy": [ 1, 3 ],
  "security": [ 2, 3, 5]
} 

