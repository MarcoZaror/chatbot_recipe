# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 20:09:37 2020

@author: Marco
"""

import requests
from bs4 import BeautifulSoup

class Scrapping:
    def __init__(self, headers, seeds):
        self.headers = headers
        self.seeds = seeds
        
    def look_for_links(self):
        link_total = []
        for seed in self.seeds:
            init = seed.find('-de-')
            end = seed.find('-listado')
            category = seed[init+4:end]
            for i in range(1,20):
                seed = seed[:-6] + str(i) + seed[-5:]
                request = requests.get(seed)
                if request.status_code != 200:
                    continue
                r = requests.get(seed, headers = self.headers)
                a = r.text
                soup = BeautifulSoup(a, "lxml")
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                for l in links:
                    link_total.append((l,category))
        # Clean links (get only the ones with recipes)
        match = 'https://www.recetasgratis.net/receta-'            
        links_recetas = []
        for l in link_total:
            if (l[0][:37] == match):
                links_recetas.append(l)
       
        links_recetas = set(links_recetas)
        links_recetas = list(links_recetas)
        return links_recetas
    
    def grab_content(self, link, recetas, ind,category):
        # Initial configurations
        r = requests.get(link, headers = self.headers)#, verify=False)
        a = r.text
        soup = BeautifulSoup(a, "lxml")
        
        # get title
        tit = ''
        title = soup.findAll("h1", {"class": "titulo titulo--articulo"})
        for o in title:
            tit = o.text.strip()
        
        # Get text
        desc = ''
        description = soup.findAll("div", {"class": "intro"})
        for o in description:
            desc = o.text.strip()
        
        # Get people
        com = ''
        people = soup.findAll("span", {"class": "property comensales"})
        for o in people:
            com = o.text.strip()
        
        # Get duration
        dur = ''
        duration = soup.findAll("span", {"class": "property duracion"})
        for o in duration:
            dur = o.text.strip()
        
        # Get difficulty
        dif = ''
        difficulty = soup.findAll("span", {"class": "property dificultad"})
        for o in difficulty:
            dif = o.text.strip()
        
        # Caracteristicas adicionales
        prop = ''
        extras = soup.findAll("div", {"class": "properties inline"})
        for o in extras:
            prop = o.text.strip()

        vegetarianos = 0
        if prop.find('vegetarianos') > 1:
            vegetarianos = 1
        veganos = 0
        if prop.find('veganos') > 1:
            veganos = 1
        sin_az = 0
        if prop.find('sin azúcar') > 1:
            sin_az = 1
        sin_glu = 0
        if prop.find('sin gluten') > 1:
            sin_glu = 1
        sin_lac = 0
        if prop.find('sin lactosa') > 1:
            sin_lac = 1
        sin_sal = 0
        if prop.find('sin sal') > 1:
            sin_sal = 1
        picante = 0
        if prop.find('Nada picante') > 1:
            picante = 1
        elif prop.find('Poco picante') > 1:
            picante = 2
        elif prop.find('Picante') > 1:
            picante = 3
        elif prop.find('Muy picante') > 1:
            picante = 4
            
        paises = [('italianas','italia'),('españolas','españa'),
                  ('venezolanas','venezuela'), ('argentinas','argentina'),
                  ('colombianas','colombia'),('japonesas','japon'),
                 ('Francia','Francia'),('peruanas','peru'),
                 ('chilenas','chile'),('chinas','china'),
                 ('Estados Unidos','estados unidos'),('indias','india'),
                 ('Cuba','cuba'),('Alemania','alemania')]
        p = 0
        for pais in paises:
            if prop.find(pais[0]) > 1:
                p = pais[1]

        # Get ingredients
        ing = []
        i=1
        ingredients = soup.findAll("label", {"for": "ingrediente-{}".format(1)})
        for o in ingredients:
            ing.append(o.text.strip())
        while len(ingredients) > 0:
        #for i in range(10):
            i+=1
            ingredients = soup.findAll("label", {"for": "ingrediente-{}".format(i)})
            for o in ingredients:
                ing.append(o.text.strip())
        
        recetas[ind] = {}
        recetas[ind]['cat'] = category
        recetas[ind]['link'] = link
        recetas[ind]['tit'] = tit
        recetas[ind]['desc'] = desc
        recetas[ind]['com'] = com
        recetas[ind]['dur'] = dur
        recetas[ind]['dif'] = dif
        recetas[ind]['prop'] = prop
        recetas[ind]['veg'] = vegetarianos
        recetas[ind]['vega'] = veganos
        recetas[ind]['s_az'] = sin_az
        recetas[ind]['s_la'] = sin_lac
        recetas[ind]['s_glu'] = sin_glu
        recetas[ind]['s_sal'] = sin_sal
        recetas[ind]['pic'] = picante
        recetas[ind]['pais'] = p
        recetas[ind]['ing'] = ing
        
        return recetas