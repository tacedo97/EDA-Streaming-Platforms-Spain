#Importamos los paquetes necesarios
import requests
import pandas as pd
import numpy as np
import os
import math

def get_products_tmdb(movie_tv, id_provider, header):
    '''
    Inputs:
        - movie_tv --> "movie" o "tv" en función de si queremos extraer el listado de películas o de series de TMDB
        - id_provider --> El ID de la plataforma de streaming de la que queremos obtener las películas/series de TMDB
        - header --> Header que contiene una clave con laque poder realizar peticiones en la API de TMDB

    Output:
    Dataframe con las películas/series de la plataforma de streaming con ID='id_provider' en la región de España
    '''    
    url_products = "https://api.themoviedb.org/3/discover/"+ movie_tv + "?with_watch_providers=" + str(id_provider)+ "&watch_region=ES" #URL del endpoint
    res_url_products = requests.get(url_products, headers=header) #Petición a la bbdd para la obtención de las películas/series de la plataforma introducida como input en España
    platform_products = res_url_products.json()["results"] #JSON con la información de las películas/series de la plataforma indicada en España
    pages = res_url_products.json()["total_pages"]

    for i in range(2, pages+1): #Tenemos que hacer una petición por hoja para conseguir todas las películas/series. Empezamos en la 2 porque la página 1 es la que hemos obtenido en la petición previa
        url = url_products + "&page=" +str(i)
        res_url = requests.get(url,headers=header)
        platform_products = pd.concat([pd.DataFrame(platform_products), pd.DataFrame(res_url.json()["results"])], ignore_index=True)
    return platform_products