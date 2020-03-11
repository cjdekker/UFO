
import folium
from folium import plugins
from IPython.display import HTML, display




def map_all_clusters(df_us,year =''):
    data = df_us.iloc[0:, :]
    data.head()

    # let's start again with a clean copy of the map of San Francisco
    us_map = folium.Map(location=[43.5, -100], zoom_start=5)

    # instantiate a mark cluster object for the incidents in the dataframe
    incidents = plugins.MarkerCluster().add_to(us_map)

    # loop through the dataframe and add each data point to the mark cluster
    for lat, lng, in zip(data.latitude, data['longitude ']):
        folium.Marker(
            location=[lat, lng],
            icon=None,

            #         popup=label,
        ).add_to(incidents)

    # add incidents to map
    us_map.add_child(incidents)

    display(us_map)
    us_map.save("us_map_all_clusters_%s.html"%year)
