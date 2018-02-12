def country_location(country):
    """
    str -> lst
    Return the location of country
    """
    import geopy
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(timeout=10)
    location = geolocator.geocode(country)
    print("location found")
    print(location.latitude, location.longitude)
    return [location.latitude, location.longitude]

def main():
    import folium
    map = folium.Map(tiles = "cartodbdark_matter")
    lst_countries = [["India", "flags/India.jpeg"],["USA", "flags/USA.jpeg"],
                    ["France", "flags/France.jpeg"],["Japan", "flags/Japan.jpeg"],
                    ["Iran", "flags/Iran.jpeg"],["Italy", "flags/Italy.jpeg"],
                    ["Germany", "flags/Germany.jpeg"],["UK", "flags/UK.jpeg"],
                    ["Canada", "flags/Canada.jpeg"],["South Korea", "flags/SK.jpeg"]]
    layer_4 = folium.FeatureGroup(name="Top 10 of all times")
    for element in lst_countries:
        icon_img = folium.features.CustomIcon(element[1], icon_size=(15, 10))
        layer_4.add_child(folium.Marker(location=country_location(element[0]),
                                                popup=element[0],
                                                icon=icon_img))
        print("!!!")
    map.add_child(layer_4)
    map.add_child(folium.LayerControl())
    map.save("Map123.html")
    print("SAVED")


main()
