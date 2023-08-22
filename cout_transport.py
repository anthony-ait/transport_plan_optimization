#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anthony
"""
#Algorithme permettant de calculer les coûts à l'aide du PRK et des coordonnées GPS des sites

import numpy as np
import pandas as pd
import gmaps
import googlemaps

API_KEY = 'AIzaSyCEI4l7A8UwIf5vrZWnxsTFReR17M8sjas'
gmaps.configure(api_key=API_KEY)
googlemaps = googlemaps.Client(key=API_KEY)

# Fonction pour calculer la distance entre 2 points
def distance_calculator(_df):
    
    _distance_result = np.zeros((len(_df),len(_df)))
    _df['latitude-longitude'] = '0'
    for i in range(len(_df)):
        _df['latitude-longitude'].iloc[i] = str(_df.latitude[i]) + ',' + str(_df.longitude[i])
    print(_df)
    for i in range(len(_df)):
        for j in range(len(_df)):
            
            # calculate distance of all pairs
            _google_maps_api_result = googlemaps.directions(_df['latitude-longitude'].iloc[i],
                                                            _df['latitude-longitude'].iloc[j],
                                                            mode = 'driving')
            # append distance to result list
            _distance_result[i][j] = _google_maps_api_result[0]['legs'][0]['distance']['value']
    
    return _distance_result



#on met les distances vdr-pfc à zéro si on se place dans les arrivées
def adaptation_arrivee(df):
    for i in range(len(df)):
        distance[0][i]=0
        
        
#on met les distances vdr-pfc à zéro si on se place dans les arrivées
def adaptation_depart(df):
    for i in range(len(df)):
        distance[i][0]=0        
        
        
        
        
        
print("Calculateur de coût transport")
print("Dans quel sens souhaitez-vous calculer le coût ?")
print("1. Départ")
print("2. Arrivée")
continuer=True
while continuer:
    choix=input("Veuillez indiquer le numéro choisi :")
    if choix in ("1","2"):
        if choix=="1":
            continuer=False
            df = pd.read_csv ('/Users/anthony/spyder-py3/Plan_de_transport/Coord_PFC_DEPART.csv',
                              sep=';',
                              )
            customer_count = len(df)
            distance = distance_calculator(df)
            print(distance)
            adaptation_arrivee(df)
            distance = (distance/1000)*1.1845
            Dist=pd.DataFrame(distance)
            Dist.to_csv("cout_transport_depart.csv")

        if choix=="2":
            continuer=False
            df = pd.read_csv ('/Users/anthony/spyder-py3/Plan_de_transport/Coord_PFC_ARRIVEE.csv',
                              sep=';',
                              )
            customer_count = len(df)
            distance = distance_calculator(df)
            adaptation_depart(df)
            distance = (distance/1000)*1.1845
            Dist=pd.DataFrame(distance)
            Dist.to_csv("cout_transport_arrivee.csv")

    else:
        print("Commande incorrecte")


    








