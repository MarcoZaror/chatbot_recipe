# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 20:08:14 2020

@author: Marco
"""

import json
import os
from sacremoses import MosesTokenizer
import numpy as np

class Data:
    def __init__(self):
        self.recetas = {}
        self.word2id = {}
        self.id2word = {}
        self.recetas_emb = {}
        self.w_emb = {} # pretrained word embeddings for word only in text
    
    def load_content(self, path):
        if os.path.exists(path):
            with open(path, 'r') as fp:
                self.recetas = json.load(fp)
        else:
            self.recetas = {}
        return self.recetas
    
    def write_content(self, path_rec, path_w2i, path_i2w, path_rec_emb, path_w_emb):
        with open(path_rec, 'w') as fp:
            json.dump(self.recetas, fp)
        with open(path_w2i, 'w') as fp:
            json.dump(self.word2id, fp)
        with open(path_i2w, 'w') as fp:
            json.dump(self.id2word, fp)
        np.save(path_rec_emb, self.recetas_emb)
        np.save(path_w_emb, self.w_emb)

    def get_only_complete(self):
        complete = 0
        incomplete = 0
        recetas2 = {}
        ind = 1
        for i in self.recetas.keys():
            check = self.recetas[i]
            if (check['link'] != '') and (check['tit'] != '') and (check['desc'] != '') and (check['com'] != '') and (check['dur'] != '') and (check['dif'] != '') and (check['prop'] != '') and (check['ing'] != ''):
                complete += 1
                recetas2[ind] = self.recetas[i]
                ind +=1
            else:
                incomplete += 1
        print('{} % of complete recipes'.format(complete/(complete+incomplete)))
        self.recetas = recetas2
    
    def clean_getvocab(self):
        raw_text = []
        for i in range(1,len(self.recetas)):
            desc = self.recetas[i]['tit'] + self.recetas[i]['cat'] + self.recetas[i]['desc'] 
            desc = desc.replace('.',' ')
            desc = desc.replace(',',' ')
            desc = desc.replace('(',' ')
            desc = desc.replace(')',' ')
            desc = desc.split()
            for word in desc:
                raw_text.append(word.strip())
            if self.recetas[i]['pais'] != 0: # Add country to the text
                raw_text.append(self.recetas[i]['pais'])
                
        raw_text = [w.lower() for w in raw_text]
        raw_text = ' '.join(raw_text)
        
        mt = MosesTokenizer(lang='sp')
        raw_text_tok = mt.tokenize(raw_text, escape=False)
        # make word2id and id2word
        i = 0
        for word in raw_text_tok:
            if word not in self.word2id:
                self.word2id[word] = i
                i += 1
        self.id2word = {w: k for k, w in self.word2id.items()}
    
    def get_embeddings(self):
        # Load embeddings
        self.w_emb = {}
        with open('embeddings-m-model.vec', 'r', encoding='utf-8') as fp:
            for line in fp.readlines()[1:]:
                word = line.split()[0]
                if word in self.word2id:
                    emb = np.array(line.strip('\n').split()[1:]).astype(np.float32)
                    self.w_emb[word] = emb 
        # Compute recipe embeddings
        mt = MosesTokenizer(lang='sp')
        for i in range(1,(len(self.recetas)+1)):
            desc = mt.tokenize(self.recetas[i]['tit'] + ' ' + self.recetas[i]['cat'] + ' ' +  str(self.recetas[i]['pais']) , escape=False)
            desc = [w.lower() for w in desc]
            # Compute embedding for the sentence
            w = 0.000000001
            emb = np.zeros(100) 
            for word in desc:
                if word in self.w_emb:
                    emb += self.w_emb[word]
                    w += 1
            self.recetas_emb[i] = emb/w
