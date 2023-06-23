from itertools import chain, combinations

class Filterset():

    def powerset(self, input_list):
        s = list(input_list)  # allows duplicate elements
        sets = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
        lists = []
        for item in sets:
            lists.append(list(item))
        lists.reverse()
        return lists

    def decreasing_lists(self, input_list):
        result = []
        for i in range(len(input_list) + 1):
            result.append(input_list[:i])
        result.reverse()
        return result
  
    def __init__(self, pro_object):
        self.strict_security_requirements = pro_object.security.strict 
        self.strict_privacy_requirements = pro_object.privacy.strict 

        # DEBUG, REMOVE LATER
        print(pro_object.security.strict)


        # Combine only_use and exclude list into one exclude list,
        # where the only_use is interpreted as "exclude everything but this"
        # and the result is union'ed to combine both approaches into one representation
        self.geolocations_to_exclude = set(pro_object.geolocation.exclude)

        if len(pro_object.geolocation.only_use) > 0:
            full_geo_list = set(["EU", "AS", "NA", "SA", "AF", "OC", "AN"])
            self.geolocations_to_exclude = full_geo_list.difference(set(pro_object.geolocation.only_use))

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
            self.best_effort_privacy_subsets = self.decreasing_lists(pro_object.privacy.best_effort)

        # Initially set the best effort requirement sets to the biggest subset in the list of sets
        self.best_effort_security_requirements = self.best_effort_security_subsets[0]
        self.best_effort_privacy_requirements = self.best_effort_privacy_subsets[0]







    def best_effort_security_constraints_are_not_yet_reduced_to_the_empty_set(self) -> bool:
        return len(self.best_effort_security_subsets) > 1

    def best_effort_privacy_constraints_are_not_yet_reduced_to_the_empty_set(self) -> bool:
        return len(self.best_effort_privacy_subsets) > 1

    def reduce_best_effort_security_constraints(self):
        if self.best_effort_security_constraints_are_not_yet_reduced_to_the_empty_set():
            self.best_effort_security_subsets.pop(0)
            self.best_effort_security_requirements = self.best_effort_security_subsets[0]

    def reduce_best_effort_privacy_constraints(self):
        if self.best_effort_privacy_constraints_are_not_yet_reduced_to_the_empty_set():
            self.best_effort_privacy_subsets.pop(0)
            self.best_effort_privacy_requirements = self.best_effort_privacy_subsets[0]

    def as_has_to_be_removed(self, nio_object, mode, print_mode) -> bool:
        drop: bool = False
        strict = mode == "strict"
        verbose = print_mode == "verbose"

        security_requirements = []
        privacy_requirements = []
        security_requirements.extend(self.strict_security_requirements)
        privacy_requirements.extend(self.strict_privacy_requirements)

        if not(strict):
            security_requirements.extend(list(self.best_effort_security_requirements))
            privacy_requirements.extend(list(self.best_effort_privacy_requirements))


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
                if verbose:
                    print(geolocation, "is in", self.geolocations_to_exclude, "while it should be excluded")
                break

        # security_requirements.clear()
        # privacy_requirements.clear()

        return drop