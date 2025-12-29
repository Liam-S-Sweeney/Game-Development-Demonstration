import character_table as ct
import personality_stat_tracker as pst
import stat_calc as sc
import character_creator as cc
import tkinter as tk
from tkinter import ttk, messagebox
from background import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import random
import os
# os.remove('player_characters.db')

expected_column_order = [
    'name', 'sex', 'faction', 'gods', 'mortal_type', 'mortal_subtype','level',

    'strength', 
        'brawn',
            'might', 
            'skeletal_muscle_mass', 
            'explosiveness', 
            'carrying_capacity',
            'block_chance',
        'stamina', 
            'muscular_endurance', 
            'grip',
            'gross_motor_control',

    'agility', 
        'dodge', 
            'reflexes', 
            'hit_avoidance_chance', 
            'stealth',
        'mobility', 
            'balance', 
            'speed', 
            'flexibility', 
            'acrobatics',
        'precision',
            'fine_motor_control',
            'aim',
            'targeting',
            'parry',

    'vitality', 
        'resilience', 
            'pain_tolerance',
            'durability',
            'dmg_absorbtion',
        'vigor',
            'recovery_rate',
            'intervention_receptivity',
            'resistance',
            
    'cognition', 
        'memory', 
            'information_retention',
        'logic', 
            'reasoning',
        'fluency',
            'processing_speed',

    'sagacity', 
        'perception', 
            'situational_awareness',
            'sensory_sensitivity',
        'intuition', 
            'instincts',
            'o_interpersonal_insigt',
            's_intrapersonal_insight',
        'composure',
            'stress_modulation',
            'emotional_stability',

    'influence', 
        'charm', 
        'intimidation', 
        'seduction', 
        'deception',

    'openness',
    'conscientiousness',
    'extraversion',
    'agreeableness',
    'neuroticism',

    # Inventory
    'inventory',
    # Equipment
    'helmet','visor','gorget','coif','arming_cap', # gorget for neck and throat, coif for additional protection of cranium+neck, arming_cap for comfort+cranium,
    'gambeson','haubergeon','breastplate','backplate','plackart', # gambeson for whole torso (base layer fabric), haubergeon for whole torso (second layer mail), plackart for abdominal plate
    'r_pauldron','l_pauldron','r_spaulder','l_spaulder','upper_gousset','r_vambrace','l_vambrace','r_gauntlet','l_gauntlet', # pauldron for shoulders, spaulder for upper arm, vambrace for forearm, Gousset for flexible joints that dont allow for rigid protection
    'chausses','culet','mail_skirt','codpiece','lower_gousset','r_tasset','l_tasset','r_poleyn','l_poleyn','r_greave','l_greave','r_sabaton','l_sabaton', # chausses for whole legs, culet for lwoer back and buttocks, tasset fore upper legs, grieves for lower legs, poleyn for the knees, sabatons for feet
    # Hand Slots
    '1_hand','2_hand','3_hand','4_hand',
    # Accessories
    'hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
    'ring','necklace','bracelet','eye_piece','mask','implant','gadget',
    # Status Effects
    'status_effects',
    # Stress
    'stress_level',
    # Relationships
    'individual_relationships', 'faction_relationships',

    'randomize_stats',
]

# Nutritional Needs
# 'kcal_daily_needs', 'protein_daily_needs' # 1kg * 15kcal / 2g protein
# Experience

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PC_DB_PATH = os.path.join(BASE_DIR,'player_characters.db')
PC_CONN = connect(PC_DB_PATH)
PC_CURSOR = PC_CONN.cursor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_DB_PATH = os.path.join(BASE_DIR,'characters.db')
CHARACTERS_CONN = connect(CHARACTERS_DB_PATH)
CHARACTERS_CURSOR = CHARACTERS_CONN.cursor()

def load_character_data():
    global CHARACTER_DATA
    try:
        df = pd.read_sql('SELECT * FROM player_characters', PC_CONN)
        CHARACTER_DATA = df.to_dict(orient='list')
    except Exception as e:
        print("Initializing empty database:", e)

        # Initialize structure
        CHARACTER_DATA = {column: [] for column in expected_column_order}

        # Create characters table with all expected columns
        column_defs = ', '.join([f'"{col}" TEXT' for col in expected_column_order])
        PC_CURSOR.execute(f"CREATE TABLE IF NOT EXISTS player_characters ({column_defs})")
        PC_CONN.commit()

load_character_data()

def add_player_character(character):

    CHARACTERS_CURSOR.execute("SELECT * FROM characters where name = ?",(character,))
    rows = CHARACTERS_CURSOR.fetchall()

    CHARACTERS_CURSOR.execute("PRAGMA table_info(characters)")
    columns = [col[1] for col in CHARACTERS_CURSOR.execute("PRAGMA table_info(characters)")]
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?'] * len(columns))
    insert_sql = f"INSERT INTO player_characters ({columns_str}) VALUES ({placeholders})"

    for row in rows:
        PC_CURSOR.execute(insert_sql,row)

    PC_CONN.commit()
    CHARACTERS_CONN.close()
    PC_CONN.close()
    
add_player_character('test')

def delete_character(name,faction):
    PC_CURSOR.execute("DELETE FROM characters WHERE name = ? AND faction = ?",
                   (name, faction))
    PC_CONN.commit()
    print(f"Deleted character: {name} from {faction}")
