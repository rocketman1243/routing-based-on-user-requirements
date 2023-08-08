import get_country_from_latlon


# Read in country to lat/lon file
country_to_latlon = {}
latlon_file = open("additional_data/country_to_latlon.csv")
nothing_file = open("dlc3_input_nothing.csv", "w")
no_country_file = open("dlc3_input_nocountry.csv", "w")
output = open("asn_data/dlc2_cleaned.csv", "w")

for line in latlon_file:
    els = line.split(",")
    country = str(els[0])[1:3]
    lat = els[2]
    lon = els[3]

    country_to_latlon[country] = {
        "lat": lat,
        "lon": lon
    }

latlon_file.close()

complete_info = {}
no_country = {}
no_latlon = {}
nothing = set()

dlc2file = open("dlc2_output.csv", "r")
for line in dlc2file:

    items = line.split(",")

    asn = items[0]
    country = items[1]
    lat = items[2]
    lon = items[3]

    if lat == '0' and (lon == '0\n' or lon == '0') and len(country) == 0:
        nothing_file.write(f"{asn}\n")

    elif len(country) == 0:
        no_country[asn] = {
            "lat": items[2],
            "lon": items[3]
        }

    elif lat == '0' and (lon == '0\n' or lon == '0') and len(country) > 0:
        no_latlon[asn] = country

    else:
        output.write(line)

# FILL IN LAT LON FROM FILE
for asn in no_latlon:
    country = no_latlon[asn]
    if country not in country_to_latlon:
        nothing.add(asn)

    complete_info[asn] = {
        "country": country,
        "lat": country_to_latlon[country]["lat"],
        "lon": country_to_latlon[country]["lon"][:-1]
    }

# FILL IN COUNTRY FROM LAT LON
cc = get_country_from_latlon.CountryChecker('additional_data/borders/borders.shp')

for asn in no_country:
    lat = float(no_country[asn]["lat"])
    lon = float(no_country[asn]["lon"])

    country = cc.getCountry(get_country_from_latlon.Point(lat, lon))
    if country is None:
        no_country_file.write(f"{asn},{lat},{lon}\n")
        continue
    
    country_iso = country.iso


    complete_info[asn] = {
        "country": country_iso,
        "lat": lat,
        "lon": lon
    }

for asn in complete_info:
    output.write(f'{asn},{complete_info[asn]["country"]},{complete_info[asn]["lat"]},{complete_info[asn]["lon"]}\n')
output.close()

for asn in nothing:
    nothing_file.write(f"{asn}\n")

nothing_file.close()
no_country_file.close()