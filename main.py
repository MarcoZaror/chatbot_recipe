# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:58:36 2020

@author: Marco
"""
from recipebot import recipebot
import os

def main():
    bot = recipebot()
    
    path_rec = os.getcwd()+'\\recetas.json'
    path_w2i = os.getcwd()+'\\w2i.json'
    path_rec_emb = os.getcwd()+'\\recetas_emb.npy'
    path_w_emb = os.getcwd()+'\\w_emb.npy'
    
    bot.init_bot(path_rec, path_rec_emb, path_w_emb, path_w2i)
    print('Hola, soy receta-bot!')
    print('Para comenzar, cuentame un poco de ti..')
    print('Eres vegetariana(o) o vegana(o)?')
    rpta_veg = input()
    bot.get_veg(rpta_veg)
    print('Perfecto! Lo tendre en consideracion')
    print('Eres alergico o alergica al gluten?')
    rpta_glu = input()
    bot.get_glu(rpta_glu)
    print('Genial.. estoy listo para recomendarte recetas!')
    print('Que te gustaria cocinar hoy?')
    preg = input()
    bot.get_recipes(preg)
    #print(bot.query['vegan'])
    #bot.get_veg('soy vegano')
    #print(bot.query['vegan'])
    #print(bot.query['gluten'])
    #bot.get_glu('si')
    #print(bot.query['gluten'])
    #bot.get_recipes('quiero cocinar comida india')

if __name__ == '__main__':
    main()

