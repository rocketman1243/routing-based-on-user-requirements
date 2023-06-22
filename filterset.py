class Filterset():
    def __init__(self, security_requirements, privacy_requirements, geolocations_to_exclude):
        this.security_requirements = security_requirements
        this.privacy_requirements = privacy_requirements
        this.geolocations_to_exclude = geolocations_to_exclude

    def this_as_has_to_be_removed(nio_object) -> bool:
        drop: bool = False

        # check security: The required security requirements have to be a subset of the security
        # requirements of the AS to have this AS handle our path. If this is NOT the case, we
        # drop this AS from our graph. Same for privacy...
        if not(set(this.security_requirements).issubset(set(nio_object.security))):
            drop = True
        if not(set(this.privacy_requirements).issubset(set(nio_object.privacy))):
            drop = True

        # Check whether the geolocation(s) of this AS fall in the list of geolocations that we
        # want to EXCLUDE. If so, we drop this AS
        for geolocation in nio_object.geolocation:
            if geolocation in this.geolocations_to_exclude:
                drop = True
                break
