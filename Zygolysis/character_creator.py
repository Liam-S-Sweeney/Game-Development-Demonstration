import character_table as ct
import personality_stat_tracker as pst
import stat_calc as sc
import tkinter as tk
from tkinter import ttk, messagebox
from background import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import random
import statistics as stat
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTER_DB_PATH = os.path.join(BASE_DIR,'characters.db')
conn = connect(CHARACTER_DB_PATH)
cursor = conn.cursor()

def load_character_data():
    global CHARACTER_DATA
    try:
        df = pd.read_sql('SELECT * FROM characters', conn)
        CHARACTER_DATA = df.to_dict(orient='list')
        print('df accessed.')
    except Exception as e:
        print("Initializing empty database:", e)
        return

load_character_data()

# print(CHARACTER_DATA.items())

class Character():
# print(CHARACTER_DATA)
    def __init__(self,name):
        def db_to_cs(name):
            for position_index,n in enumerate(CHARACTER_DATA['name']):
                if n == name:
                    index_db = position_index        

            all_fields = {
                'strength': {
                    'brawn':[
                        'might', 
                        'skeletal_muscle_mass', 
                        'explosiveness', 
                        'carrying_capacity',
                        'block_chance',],
                    'stamina':[
                        'muscular_endurance', 
                        'grip',
                        'gross_motor_control',]
                        },
                'agility': {
                    'dodge': [
                        'reflexes', 
                        'hit_avoidance_chance', 
                        'stealth',],
                    'mobility':[
                        'balance', 
                        'speed', 
                        'flexibility', 
                        'acrobatics',],
                    'precision':[
                        'fine_motor_control',
                        'aim',
                        'targeting',
                        'parry',]},
                'vitality': {
                    'resilience': [
                        'pain_tolerance',
                        'durability',
                        'dmg_absorbtion',],
                    'vigor':[
                        'recovery_rate',
                        'intervention_receptivity',
                        'resistance',]},
                'cognition': { 
                    'memory':[
                        'information_retention',],
                    'logic':['logic', 
                        'reasoning'],
                    'fluency':[
                        'processing_speed',]},
                'sagacity': {
                    'perception': [
                        'situational_awareness',
                        'sensory_sensitivity'],
                    'intuition': [
                        'instincts',
                        'o_interpersonal_insigt',
                        's_intrapersonal_insight'],
                    'composure':[
                        'stress_modulation',
                        'emotional_stability',]},
                'influence': {
                    'charm': ['charm'],
                    'intimidation': ['intimidation'],
                    'seduction': ['seduction'],
                    'deception': ['deception'],},}
                                                                    

            personality = ['openness',
            'conscientiousness',
            'extraversion',
            'agreeableness',
            'neuroticism',]
            global character_db_stats
            try:
                if CHARACTER_DATA['randomize_stats'][index_db] == '1':

                    strength_subscale_vals = []
                    agility_subscale_vals = []
                    vitality_subscale_vals = []
                    cognition_subscale_vals = []
                    sagacity_subscale_vals = []
                    influence_subscale_vals = []

                    for field,subfield in all_fields.items():
                        for subfield_name,trait in subfield.items():
                            # print(f"{field} -> {subfield_name}")
                            # print(f"field = {field} | subfield_name = {subfield_name}")
                            vary_or_same = random.randint(0,4)

                            base = int(CHARACTER_DATA[subfield_name][index_db])
                            # print(f"Base = {base}")

                            rand_stat_modifier = 0

                            if vary_or_same > 1:
                                rand_percent = random.randint(0,100)
                                if rand_percent < 14:
                                    rand_stat_modifier = -3
                                elif rand_percent > 14 and rand_percent < 31:
                                    rand_stat_modifier = -2
                                elif rand_percent > 31 and rand_percent < 50:
                                    rand_stat_modifier = -1
                                elif rand_percent > 50 and rand_percent < 69:
                                    rand_stat_modifier = 1
                                elif rand_percent > 69 and rand_percent < 86:
                                    rand_stat_modifier = 2
                                elif rand_percent > 86:
                                    rand_stat_modifier = 3
                            elif vary_or_same < 1:
                                rand_stat_modifier = 0

                            modified_stat = (base + rand_stat_modifier)
                            # print(modified_stat)
                            for trait in subfield[subfield_name]:
                                CHARACTER_DATA[trait][index_db] = str(modified_stat)

                            if modified_stat >= 1:
                                CHARACTER_DATA[subfield_name][index_db] = str(modified_stat)
                                if field == 'strength':
                                    strength_subscale_vals.append(modified_stat)
                                elif field == 'agility':
                                    agility_subscale_vals.append(modified_stat)
                                elif field == 'vitality':
                                    vitality_subscale_vals.append(modified_stat)
                                elif field == 'cognition':
                                    cognition_subscale_vals.append(modified_stat)
                                elif field == 'sagacity':
                                    sagacity_subscale_vals.append(modified_stat)
                                elif field == 'influence':
                                    influence_subscale_vals.append(modified_stat)
                            else:
                                CHARACTER_DATA[subfield_name][index_db] = '1'
                                if field == 'strength':
                                    strength_subscale_vals.append(modified_stat)
                                elif field == 'agility':
                                    agility_subscale_vals.append(modified_stat)
                                elif field == 'vitality':
                                    vitality_subscale_vals.append(modified_stat)
                                elif field == 'cognition':
                                    cognition_subscale_vals.append(modified_stat)
                                elif field == 'sagacity':
                                    sagacity_subscale_vals.append(modified_stat)
                                elif field == 'influence':
                                    influence_subscale_vals.append(modified_stat)
                            # print(agility_subscale_vals) 
                for field in all_fields.keys():
                    if field == 'strength':
                        avg = round(stat.mean(strength_subscale_vals))
                        if avg < 1:
                            avg = 1
                        CHARACTER_DATA[field][index_db] = str(avg)
                    elif field == 'agility':
                        avg = round(stat.mean(agility_subscale_vals))
                        if avg < 1:
                            avg = 1
                    elif field == 'vitality':
                        avg = round(stat.mean(vitality_subscale_vals))
                        if avg < 1:
                            avg = 1
                    elif field == 'cognition':
                        avg = round(stat.mean(cognition_subscale_vals))
                        if avg < 1:
                            avg = 1
                    elif field == 'sagacity':
                        avg = round(stat.mean(sagacity_subscale_vals))
                        if avg < 1:
                            avg = 1
                    elif field == 'influence':
                        avg = round(stat.mean(influence_subscale_vals))
                        if avg < 1:
                            avg = 1
                    CHARACTER_DATA[field][index_db] = str(avg)
            
                for field in personality:
                    rand_percent = random.randint(0,100)
                    base = int(CHARACTER_DATA[field][index_db])
                    CHARACTER_DATA[field][index_db] = str(rand_percent)

                
                character_db_stats = {}
                for field,val in CHARACTER_DATA.items():
                    character_db_stats[field] = val[index_db]
            except:
                
                character_db_stats = {}
                for field,val in CHARACTER_DATA.items():
                    character_db_stats[field] = val[index_db]
            
            # print(character_db_stats)

    # db_to_cs('Dummy')

        db_to_cs(name)
        global character_in_game_stats

        character_in_game_stats = {}
        for field,val in character_db_stats.items():
            if field in ['name', 'faction', 'gods', 'mortal_type', 'mortal_subtype',
                         # Inventory
                        'inventory',
                        # Equipment
                        'helmet','visor','gorget','coif','arming_cap', # gorget for neck and throat, coif for additional protection of cranium+neck, arming_cap for comfort+cranium,
                        'gambeson','haubergeon','breastplate','backplate','plackart', # gambeson for whole torso (base layer fabric), haubergeon for whole torso (second layer mail), plackart for abdominal plate
                        'r_pauldron','l_pauldron','r_spaulder','l_spaulder','upper_gousset','r_vambrace','l_vambrace','r_gauntlet','l_gauntlet', # pauldron for shoulders, spaulder for upper arm, vambrace for forearm, Gousset for flexible joints that dont allow for rigid protection
                        'chausses','culet','mail_skirt','codpiece','lower_gousset','r_tasset','l_tasset','r_poleyn','l_poleyn','r_greave','l_greave','r_sabaton','l_sabaton', # chausses for whole legs, culet for lwoer back and buttocks, tasset fore upper legs, grieves for lower legs, poleyn for the knees, sabatons for feet
    
                        # Hand Slots
                        'hand_slot_1','hand_slot_2','hand_slot_3','hand_slot_4',

                        # Accessories
                        'hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
                        'ring','necklace','bracelet','eye_piece','mask','implant','gadget',

                        # Status Effects
                        'status_effects',

                        # Stress
                        'stress_level',

                        # Relationships
                        'individual_relationships', 'faction_relationships',]:
                character_in_game_stats[field] = val
                
            elif field == 'sex':
                character_in_game_stats[field] = val.lower()

            elif field in ['strength', 'brawn','stamina', 
                        'agility', 'dodge', 'mobility', 'precision',
                        'vitality', 'resilience', 'vigor',
                        'cognition', 'memory', 'logic', 'fluency',
                        'sagacity', 'perception', 'intuition', 'composure',
                        'influence', 'charm', 'intimidation', 'seduction', 'deception',
                        'openness','conscientiousness','extraversion','agreeableness','neuroticism']:
                character_in_game_stats[field] = int(val)

            elif field in ['might', 'skeletal_muscle_mass', 'explosiveness', 'carrying_capacity','block_chance',]:
                df = getattr(sc.Brawn(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['muscular_endurance', 'grip', 'gross_motor_control',]:
                df = getattr(sc.Stamina(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['reflexes', 'hit_avoidance_chance','stealth']:
                df = getattr(sc.Dodge(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
            
            elif field in ['balance', 'speed', 'flexibility','acrobatics']:
                df = getattr(sc.Mobility(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['fine_motor_control', 'aim', 'targeting','parry',]:
                df = getattr(sc.Precision(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['pain_tolerance', 'durability', 'dmg_absorbtion']:
                df = getattr(sc.Resilience(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
            
            elif field in ['recovery_rate', 'intervention_receptivity', 'resistance']:
                df = getattr(sc.Vigor(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                
            elif field in ['information_retention']:
                df = getattr(sc.Memory(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['reasoning']:
                df = getattr(sc.Logic(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['processing_speed']:
                df = getattr(sc.Fluency(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['situational_awareness','sensory_sensitivity',]:
                df = getattr(sc.Perception(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
            
            elif field in ['instincts','o_interpersonal_insight','s_intrapersonal_insight']:
                df = getattr(sc.Intuition(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['stress_modulation','emotional_stability']:
                df = getattr(sc.Composure(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats

            elif field in ['charm','seduction','deception','intimidation']:
                df = getattr(sc.Influence(),f"{field}_df")
                ws_df = df.iloc[int(val)]
                if character_in_game_stats['sex'] == 'male':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" not in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
                elif character_in_game_stats['sex'] == 'female':
                    substats = {}
                    for k,v in ws_df.items():
                        if "female" in k:
                            substats[k] = v
                    character_in_game_stats[field] = substats
        for key,value in character_in_game_stats.items():
            setattr(self,key, value)
            # print(f'{key} --> {value}\n')
        

# print(vars(Character('god')))
# print(Character('random_test'))
# print(vars(Character('test')))


# character = 'test'
# x = Character('test').__getattribute__('durability')[f"{Character('test').__getattribute__('sex')}_cranium"]  
# print(x)
# print(Character('test').__getattribute__('sex'))
# TAKE THE DB VAL THEN WHEN YOU MAKE A CHARACTER, 
# TAKES THESE DB VAL AND APPLY TO ATTRIBUTE FILTER FROM SC TO OBJECT

