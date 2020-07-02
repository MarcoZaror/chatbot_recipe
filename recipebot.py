# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:44:28 2020

@author: Marco
"""
import json
from sacremoses import MosesTokenizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class recipebot:
    def __init__(self):
        self.recetas = {}
        self.recetas_emb = {}
        self.w_emb = {}
        self.word2id = {}
        self.query = {} #query or customer information
        self.query['vegan'] = 0
        self.query['vegetarian'] = 0
        self.query['gluten'] = 0
        self.query['lactosa'] = 0
        
    def init_bot(self, path_rec, path_rec_emb, path_w_emb, path_w2i):
        with open(path_rec, 'r') as fp:
            self.recetas = json.load(fp)
        with open(path_w2i, 'r') as fp:
            self.word2id = json.load(fp)
        self.w_emb = np.load(path_w_emb, allow_pickle=True).item()
        self.recetas_emb = np.load(path_rec_emb, allow_pickle=True).item()
    
    def get_veg(self, phrase):
        # get if customer is vegan or vegetarian
        mt = MosesTokenizer(lang='sp')
        phrase_lower = phrase.lower()
        phrase_lower = mt.tokenize(phrase_lower, escape=False)

        if ' '.join(phrase_lower).find('vegan') > 0:
            self.query['vegan'] = 1
        elif ' '.join(phrase_lower).find('vegetarian') > 0:
            self.query['vegetarian'] = 1
    
    def get_glu(self, phrase):
        # get if customer doesnt like gluten
        if phrase.lower().find('si') >= 0:
            self.query['gluten'] = 1
    
    def get_lact(self, phrase):
        # get if customer doesnt like lactose
        if phrase.lower().find('si') >= 0:
            self.query['lactosa'] = 1
            
    def get_recipes(self, phrase): 
        mt = MosesTokenizer(lang='sp')
        phrase_lower = phrase.lower()
        phrase_lower = mt.tokenize(phrase_lower, escape=False)
        # Compute embedding of the phrase
        w = 0.000000001
        emb = np.zeros(100) 
        for word in phrase_lower:
            if word in self.w_emb:
                emb += self.w_emb[word]
                w += 1
        phrase_emb = emb/w
        sims = []
        
        # Check if person is vegan or vegetarian and get idx of recipes matching
        matchings_veg = []
        #recetas_filt = {}
        #j = 0
        if self.query['vegan'] == 1:
            for i, receta in self.recetas.items():
                if receta['vega'] == 1:
                    matchings_veg.append(int(i))
                    #recetas_filt[j] = receta
                    #j += 1
        elif self.query['vegetarian'] == 1:
            for i, receta in self.recetas.items():
                if receta['veg'] == 1:
                    matchings_veg.append(int(i))
                    #recetas_filt[j] = receta
                    #j += 1
        else:
            #recetas_filt = self.recetas
            matchings_veg = [i for i in range(1,len(self.recetas))]
        
        # Check if person doesn't eat gluten
        matchings_glu = []
        if self.query['gluten'] == 1:
            for i, receta in self.recetas.items():
                if receta['s_glu'] == 1:
                    matchings_glu.append(int(i))
        else:
            matchings_glu = [i for i in range(1,len(self.recetas))]
        
        # Get a general matching
        matchings = [value for value in matchings_veg if value in matchings_glu]
        # Check similarity between phrase and all the other recipes
        for i in range(1, (len(self.recetas)+1)):
            if i in matchings:
                sims.append(cosine_similarity(self.recetas_emb[i].reshape(1,-1), phrase_emb.reshape(1,-1))[0])
        results = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:5]
        print('He encontrado estas recetas!')
        for i in results:
            print(str(self.recetas[str(matchings[i])]['tit']) + '\n')
            #print(str(self.recetas[str(i+1)]['tit']) + '\n')
            #print(str(self.recetas[str(i+1)]['desc']) + '\n') 
    

        