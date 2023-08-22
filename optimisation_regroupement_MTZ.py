#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 18:33:01 2022

@author: anthony
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anthony
"""
import numpy as np
import pandas as pd
import pulp
import matplotlib.pyplot as plt
import time	
				
tic = time.perf_counter() # Start Time

#import du fichier contenant les données des PFC
df = pd.read_csv ('/Users/anthony/spyder-py3/test.csv',
                  sep=';',
                  )

#Nombre de PFC ('0' est VDR) 
customer_count = len(df)


#Capacité du véhicule
vehicle_capacity = 4800

#Liste contenant les départs des liaisons
liaison=[]

#Calculer le nombre de colis de chaque PFC
def demand(nb_colis_national):
    df['nb_colis']=df.weight*nb_colis_national #calcul avec la clé de répartition
    df['nb_colis']=df['nb_colis'].astype(int) #convertit en entier
    print(df)
    
#nb_colis_journalier=int(input("Quel est le nombre de colis journalier ?"))
nb_colis_journalier = 45000

demand(nb_colis_journalier)

#Génération de la matrice des coûts
df2 = pd.read_csv('/Users/anthony/spyder-py3/Plan_de_transport/cout_transport.csv',delimiter=",",index_col=0)
distance=df2.to_numpy(dtype=int) 


#permet de déterminer les camions qui partiront plein d'un site et d'avoir la df à jour
cout_total=0
for PFC in df.index:
    if df.loc[PFC,'nb_colis']>vehicle_capacity:
        nb_liaison=df.loc[PFC,'nb_colis']//vehicle_capacity
        for i in range(nb_liaison):
            df.at[PFC,'nb_colis']-=vehicle_capacity
            liaison.append(df.loc[PFC,'name'])#retourne le nom correspondant au nombre de colis
            cout_total+=distance[df.index[PFC]][0]


# Solver avec pulp et gurobi

    
    #Définition du problème
problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

    #Définition des variables de décision
x = [[pulp.LpVariable("x%s_%s"%(i,j), cat="Binary") for j in range(customer_count)] for i in range(customer_count)]
u = [pulp.LpVariable("u%s"%(i)) for i in range(customer_count)]

    #Fonction objectif
problem += pulp.lpSum(distance[i][j] * x[i][j]
                      for j in range(customer_count) 
                      for i in range (customer_count))

    #Contraintes
    #Une visite par véhicule par PFC
for i in range(1, customer_count):
    problem += pulp.lpSum(x[i][j] for j in range(customer_count)) ==1

for i in range(1, customer_count):
    problem += pulp.lpSum(x[j][i] for j in range(customer_count)) ==1                      

for i in range(customer_count):
    for j in range(1, customer_count):
        problem += u[j]>=u[i]+df.nb_colis[j]-vehicle_capacity*(1-x[i][j])

for i in range(1, customer_count):
    problem += df.nb_colis[i]<=u[i]<=vehicle_capacity

problem+=u[0]==0

for i in range(1,customer_count):
    problem+=u[i]>=0
    


solver = pulp.GUROBI()
problem.setSolver(solver)
problem.solver.buildSolverModel(problem)   
    
    #Affiche nombre de véhicule et coût
if problem.solve() == 1:
    print('Moving Distance:', pulp.value(problem.objective))

cout_total+=pulp.value(problem.objective)        




#Affichage avec matplotlib

#Carte de France
plt.figure(figsize=(8,8))
xf = np.array([2, -5, -2, 8,8,2])
yf = np.array([51,47, 43, 43,49,51])

plt.plot(xf, yf)
for i in range(customer_count):    
    if i == 0:
        plt.scatter(df.longitude[i], df.latitude[i], c='green', s=200)
        plt.text(df.longitude[i], df.latitude[i], "depot", fontsize=12)
    else:
        plt.scatter(df.longitude[i], df.latitude[i], c='orange', s=200)
        plt.text(df.longitude[i], df.latitude[i], str(df.name[i]), fontsize=12)
color_list=['red','blue','yellow','pink']
color=0

for i in range(customer_count):
    for j in range(customer_count):
        if i != j and pulp.value(x[i][j]) == 1:
            plt.plot([df.longitude[i], df.longitude[j]], [df.latitude[i], df.latitude[j]], c=color_list[color%3])
            color+=1
            if i==0:
                liaison.append(df.name[j])




plt.show()

print(liaison)
print('Cout total=',cout_total)



toc = time.perf_counter() # End Time
print(f"Build finished in {(toc - tic)/60:0.0f} minutes {(toc - tic)%60:0.0f} seconds")

































