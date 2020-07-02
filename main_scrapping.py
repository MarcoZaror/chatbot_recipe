# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 20:19:27 2020

@author: Marco
"""

from Data import Data
from Scrapping import Scrapping
import os
import requests

def main():
    #Need to create a dictionary at the beginning (just for the first time)
    #path = os.getcwd()+'\\recetas.json'#'C:/Users/Marco/Documents/MSc/Tesis/content.json'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    seeds = [
    'https://www.recetasgratis.net/Recetas-de-Aperitivos-tapas-listado_receta-1_1.html',
    'https://www.recetasgratis.net/Recetas-de-Aves-caza-listado_receta-11_1.html',
    'https://www.recetasgratis.net/Recetas-de-Cocteles-bebida-listado_receta-15_1.html',
    'https://www.recetasgratis.net/Recetas-de-Ensaladas-listado_receta-4_1.html',
    'https://www.recetasgratis.net/Recetas-de-Huevos-lacteos-listado_receta-18_1.html',
    'https://www.recetasgratis.net/Recetas-de-Mariscos-listado_receta-13_1.html',
    'https://www.recetasgratis.net/Recetas-de-Pasta-listado_receta-5_1.html',
    'https://www.recetasgratis.net/Recetas-de-Postres-listado_receta-17_1.html',
    'https://www.recetasgratis.net/Recetas-de-Sopa-listado_receta-6_1.html',
    'https://www.recetasgratis.net/Recetas-de-Arroces-cereales-listado_receta-9_1.html',
    'https://www.recetasgratis.net/Recetas-de-Carne-listado_receta-10_1.html',
    'https://www.recetasgratis.net/Recetas-de-Guisos-Potage-listado_receta-19_1.html',
    'https://www.recetasgratis.net/Recetas-de-Legumbres-listado_receta-8_1.html',
    'https://www.recetasgratis.net/Recetas-de-Pan-bolleria-listado_receta-16_1.html',
    'https://www.recetasgratis.net/Recetas-de-Pescado-listado_receta-12_1.html',
    'https://www.recetasgratis.net/Recetas-de-Salsas-guarniciones-listado_receta-14_1.html',
    'https://www.recetasgratis.net/Recetas-de-Verduras-listado_receta-7_1.html']
    ct = Data()
    #recetas = ct.load_content(path)
    recetas = {}
    key = len(recetas) + 1
       
    sc = Scrapping(headers, seeds)
    links = sc.look_for_links()
    for link in links:
        try:
            recetas = sc.grab_content(link[0], recetas, key, link[1])
            key += 1
        except requests.ConnectionError:
            continue
    ct.recetas = recetas
    ct.get_only_complete() # Get only complete recipes
    ct.clean_getvocab() # clean text and compute word2id and id2word
    ct.get_embeddings() # Compute embeddings for the recipes
    
    path_rec = os.getcwd()+'\\recetas.json'
    path_w2i = os.getcwd()+'\\w2i.json'
    path_i2w = os.getcwd()+'\\i2w.json'
    path_rec_emb = os.getcwd()+'\\recetas_emb.npy'
    path_w_emb = os.getcwd()+'\\w_emb.npy'
    
    ct.write_content(path_rec, path_w2i, path_i2w, path_rec_emb, path_w_emb)
        
if __name__ == '__main__':
    main()

# typical query 
#q = []
#for i in range(1, len(recetas)):
#    if recetas[i]['pais'] > 0:
#        q.append(recetas[i])
  