
from ufo_data_preprocess import data_preprocess
from ufo_map_cluster import map_all_clusters
import ufo_data_analysis as an


df_us = data_preprocess('ufo-sightings/scrubbed.csv')
an.data_wordcloud(df_us)
an.data_wordcloud(df_us,city='tinley park')
an.show_freq_by_shape(df_us)
an.show_freq_by_city(df_us)
an.show_freq_by_date(df_us)


df_us_2004 = df_us[df_us['year'] == '2004']
map_all_clusters(df_us)
map_all_clusters(df_us,year='2004')



