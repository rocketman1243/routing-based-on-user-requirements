from itertools import chain, combinations

class Filterset():

    def powerset(self, input_list):
        s = list(input_list)  # allows duplicate elements
        result = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
        result.reverse()
        return result

    def decreasing_lists(self, input_list):
        result = []
        for i in range(len(input_list) + 1):
            result.append(input_list[:i])
        result.reverse()
        return result
  
    def __init__(self, pro_object):
        self.strict_security_requirements = pro_object.security.strict 
        self.strict_privacy_requirements = pro_object.privacy.strict 

        # Combine only_use and exclude list into one exclude list,
        # where the only_use is interpreted as "exclude everything but this"
        # and the result is union'ed to combine both approaches into one representation
        full_geo_list = set(["EU", "AS", "NA", "SA", "AF", "OC", "AN"])
        self.geolocations_to_exclude = set(pro_object.geolocation.exclude).union(full_geo_list.difference(set(pro_object.geolocation.only_use)))

        # Generate the subsets for security
        self.best_effort_security_subsets = []
        if pro_object.security.best_effort_mode == "biggest_subset":
            self.best_effort_security_subsets = self.powerset(pro_object.security.best_effort)
        else: # the mode is ordered_list
            self.best_effort_security_subsets = self.decreasing_lists(pro_object.security.best_effort)

        # Generate the subsets for privacy
        self.best_effort_privacy_subsets = []
        if pro_object.privacy.best_effort_mode == "biggest_subset":
            self.best_effort_privacy_subsets = self.powerset(pro_object.privacy.best_effort)
        else: # the mode is ordered_list
            self.best_effort_privacy_subsets = decreasing_lists(pro_object.privacy.best_effort)

        # Initially set the best effort requirement sets to the biggest subset in the list of sets
        self.best_effort_security_subset_index = 0
        self.best_effort_security_requirements = self.best_effort_security_subsets[0]

        self.best_effort_privacy_subset_index = 0
        self.best_effort_privacy_requirements = self.best_effort_privacy_subsets[0]


    def as_has_to_be_removed(self, nio_object, verbose=False) -> bool:
        drop: bool = False

        security_requirements = self.strict_security_requirements + list(self.best_effort_security_requirements)
        privacy_requirements = self.strict_privacy_requirements + list(self.best_effort_privacy_requirements)

        # check security: The required security requirements have to be a subset of the security
        # requirements of the AS to have self AS handle our path. If self is NOT the case, we
        # drop self AS from our graph. Same for privacy...
        if not(set(security_requirements).issubset(set(nio_object.security))):
            drop = True
            if verbose:
                print(security_requirements, "are not a security subset of", nio_object.security)
        if not(set(privacy_requirements).issubset(set(nio_object.privacy))):
            drop = True
            if verbose:
                print(privacy_requirements, "are not a privacy subset of", nio_object.privacy)

        # Check whether the geolocation(s) of self AS fall in the list of geolocations that we
        # want to EXCLUDE. If so, we drop self AS
        for geolocation in nio_object.geolocation:
            if geolocation in self.geolocations_to_exclude:
                drop = True
                break

        return drop