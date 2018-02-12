def read_file(year):
    """
    None -> lst
    Return the lst with lines from file
    """
    lst = []
    with open("locations.list") as f:
        for line in f:
            test = line.strip().split('\t')
            if "("+year+")" in test[0]:
                lst.append(test)
    return lst


def get_location(element):
    """
    lst -> None
    Fills the dictionary with element coordinates
    """
    import geopy
    from geopy.geocoders import Nominatim
    global country_dict
    geolocator = Nominatim(timeout=10)
    if "(" != element[-1][0]:
        key = element[-1].split(",")[-1].strip()
        print(key)
        try:
            country_dict[key] = country_dict[key]+1
        except:
            country_dict[key] = 1

        if element[-1] not in lc_dict.keys():
            location = geolocator.geocode(element[-1])
            if location:
                lc_dict[element[-1]] = [element[0],location.latitude, location.longitude, 1]
        else:
            lc_dict[element[-1]][-1] +=1
    else:
        key = element[-2].split(",")[-1]
        print("Loading...")
        try:
            country_dict[key] = country_dict[key] + 1
        except:
            country_dict[key] = 1
        if element[-2] not in lc_dict.keys():
            location = geolocator.geocode(element[-2])
            if location:
                lc_dict[element[-2]] = [element[0], location.latitude, location.longitude, 1]
        else:
            lc_dict[element[-2]][-1] +=1


def country_location(country):
    """
    str -> lst
    Return the location of country
    """
    import geopy
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(timeout=10)
    location = geolocator.geocode(country)
    return [location.latitude, location.longitude]


def get_map(lc_dict):
    """
    dict -> None
    Creates and saves the map to file
    """
    import folium
    map = folium.Map(tiles = "cartodbdark_matter")
    layer_2 = folium.FeatureGroup(name="Top 5 this year")
    icon_img = folium.features.CustomIcon("flags/mark.png", icon_size=(100, 70))
    for key, i in zip(country_dict.keys(), [0,1,2,3,4]):
        layer_2.add_child(folium.Marker(location=[country_location(key)],
                                                popup=key,
                                                icon=icon_img))

    #Add markers for places where movies were filmed
    layer_1 = folium.FeatureGroup(name="Places")
    for key in lc_dict.keys():
        layer_1.add_child(folium.Marker(location=[lc_dict[key][1], lc_dict[key][2]],
                                                popup=str(lc_dict[key][0]).replace("'", "*"),
                                                icon=folium.Icon()))
    #Add markers for top 10 movie places
    layer_2 = folium.FeatureGroup(name="Top 10 of all times")
    lst_countries = [["India", "flags/India.jpeg"],["USA", "flags/USA.jpeg"],
                    ["France", "flags/France.jpeg"],["Japan", "flags/Japan.jpeg"],
                    ["Iran", "flags/Iran.jpeg"],["Italy", "flags/Italy.jpeg"],
                    ["Germany", "flags/Germany.jpeg"],["UK", "flags/UK.jpeg"],
                    ["Canada", "flags/Canada.jpeg"],["South Korea", "flags/SK.jpeg"]]
    for element in lst_countries:
        icon_img = folium.features.CustomIcon(element[1], icon_size=(15, 10))
        layer_2.add_child(folium.Marker(location=country_location(element[0]),
                                                popup=element[0],
                                                icon=icon_img))
    map.add_child(layer_1)
    map.add_child(layer_2)
    map.add_child(folium.LayerControl())
    map.save("Map.html")

#get year from user
year = str(input("Enter a year: "))
#dictionary of locations
lc_dict = {}
#dictionary with counry as key and number of films as value
country_dict = {}
#for element in list of lines from file
for element in read_file(year):
    #get location and "save" it to lc_dict
    get_location(element)
#get and save map to file "Map.html"
get_map(lc_dict)
