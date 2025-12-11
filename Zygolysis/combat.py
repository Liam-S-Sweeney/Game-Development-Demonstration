import character_table as ct
import personality_stat_tracker as pst
import stat_calc as sc
import character_creator as cc
# import items as items
import tkinter as tk
from tkinter import ttk, messagebox
from background import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import random
import os
import re

os.remove('combat.db')

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
    'hand_slot_1','hand_slot_2','hand_slot_3','hand_slot_4',
    # Accessories
    'hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
    'ring','necklace','bracelet','eye_piece','mask','implant','gadget',
    # Status Effects
    'status_effects',
    # Stress
    'stress_level',
    # Relationships
    'individual_relationships', 'faction_relationships',

    'randomize_stats'
]

# COMBAT DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMBAT_DB_PATH = os.path.join(BASE_DIR,'combat.db')
COMBAT_CONN = connect(COMBAT_DB_PATH)
COMBAT_CURSOR = COMBAT_CONN.cursor()
# CHARACTERS DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_DB_PATH = os.path.join(BASE_DIR,'characters.db')
CHARACTERS_CONN = connect(CHARACTERS_DB_PATH)
CHARACTERS_CURSOR = CHARACTERS_CONN.cursor()

# ITEMS DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_DB_PATH = os.path.join(BASE_DIR,'items.db')
ITEMS_CONN = connect(ITEMS_DB_PATH)
ITEMS_CURSOR = ITEMS_CONN.cursor()

def load_character_data():
    global CHARACTER_DATA
    try:
        df = pd.read_sql('SELECT * FROM combat', COMBAT_CONN)
        CHARACTER_DATA = df.to_dict(orient='list')
    except Exception as e:
        print("Initializing empty database:", e)

        # Initialize structure
        CHARACTER_DATA = {column: [] for column in expected_column_order}

        # Create characters table with characters expected columns
        column_defs = ', '.join([f'"{col}" TEXT' for col in expected_column_order])
        COMBAT_CURSOR.execute(f"CREATE TABLE IF NOT EXISTS combat ({column_defs})")
        COMBAT_CONN.commit()

load_character_data()
# print(CHARACTER_DATA)

def add_character(character):

    CHARACTERS_CURSOR.execute("SELECT * FROM characters where name = ?",(character,))
    rows = CHARACTERS_CURSOR.fetchall()

    CHARACTERS_CURSOR.execute("PRAGMA table_info(characters)")
    columns = [col[1] for col in CHARACTERS_CURSOR.execute("PRAGMA table_info(characters)")]
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?'] * len(columns))
    insert_sql = f"INSERT INTO combat ({columns_str}) VALUES ({placeholders})"

    for row in rows:
        COMBAT_CURSOR.execute(insert_sql,row)

    COMBAT_CONN.commit()
    # CHARACTERS_CONN.close()
    # COMBAT_CONN.close()

# ITEMS DATA FRAME
items_df = pd.read_sql_query(f"SELECT * FROM items", ITEMS_CONN)
# ITEMS_CONN.close()

def delete_character(name):
    COMBAT_CURSOR.execute(f"DELETE FROM combat WHERE name = ?",(name,))
    COMBAT_CONN.commit()
    print(f"Deleted character: {name}")


can_move = True 

# MAKE A COMBAT DATABASE AND TAKE STATS CHARACTER INNIT AND MULTIPLY BASED ON EXHAUSTION

inventory_list = [
    'inventory'
]

equipment_list = [
    'helmet','visor','gorget','coif','arming_cap', # gorget for neck and throat, coif for additional protection of cranium+neck, arming_cap for comfort+cranium,
    'gambeson','haubergeon','breastplate','backplate','plackart', # gambeson for whole torso (base layer fabric), haubergeon for whole torso (second layer mail), plackart for abdominal plate
    'r_pauldron','l_pauldron','r_spaulder','l_spaulder','upper_gousset','r_vambrace','l_vambrace','r_gauntlet','l_gauntlet', # pauldron for shoulders, spaulder for upper arm, vambrace for forearm, Gousset for flexible joints that dont allow for rigid protection
    'chausses','culet','mail_skirt','codpiece','lower_gousset','r_tasset','l_tasset','r_poleyn','l_poleyn','r_greave','l_greave','r_sabaton','l_sabaton', # chausses for whole legs, culet for lwoer back and buttocks, tasset fore upper legs, grieves for lower legs, poleyn for the knees, sabatons for feet
]

hand_slots_list = [
    'hand_slot_1','hand_slot_2','hand_slot_3','hand_slot_4',
]

accessories_list = [
    'hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
    'ring','necklace','bracelet','eye_piece','mask','implant','gadget',
]

status_effects_list = [
    'status_effects',
]

stress_list = [
    'stress_level',
]

relationships_list = [
    'individual_relationships', 'faction_relationships',
    ]

def hp(character):
    hp_dict = cc.Character(character).__getattribute__('durability')
    return hp_dict
def sex(character):
    sex = cc.Character(character).__getattribute__('sex')
    return sex
def inventory(character):
    inventory_dict = {}
    for item in inventory_list:
        inventory_list[item] = cc.Character(character).__getattribute__(item)
    return inventory_dict
def equipment(character):
    equipment_dict = {}
    for item in equipment_list:
        equipment_dict[item] = cc.Character(character).__getattribute__(item)
    return equipment_dict
def hand_slots(character):
    hand_slots_dict = {}
    for item in hand_slots_list:
        hand_slots_dict[item] = cc.Character(character).__getattribute__(item)
    return hand_slots_dict
def accessories(character):
    accessories_dict = {}
    for item in accessories_list:
        accessories_dict[item] = cc.Character(character).__getattribute__(item)
    return accessories_dict
def status_effects(character):
    status_effects_dict = {}
    for item in status_effects_list:
        status_effects_dict[item] = cc.Character(character).__getattribute__(item)
    return status_effects_dict
def stress(character):
    stress_dict = {}
    for item in stress_list:
        stress_dict[item] = cc.Character(character).__getattribute__(item)
    return stress_dict
def relationships(character):
    relationships_dict = {}
    for item in relationships_list:
        relationships_dict[item] = cc.Character(character).__getattribute__(item)
    return relationships_dict

# print(hp('test'))

# print(hp('test'))
# print(equipment('test'))

# combat_fatigue('test')

def equiped_gear(character):
    ITEMS_CURSOR.execute('SELECT * FROM items')
    column_names = [description[0] for description in ITEMS_CURSOR.description]
    
    active_gear_df = pd.DataFrame(columns=column_names)

    for key, value in equipment(character).items():
        if value and value.strip():  # skip None, "", " "
            name = re.split(r'[",]', value)[1]
            e_type = re.split(r'[",]', value)[4]

            # find matching row in items_df
            match = items_df[items_df['name'] == name]
            if not match.empty:
                # append to active_gear_df
                active_gear_df = pd.concat([active_gear_df, match], ignore_index=True)

    return active_gear_df

# usage
df = equiped_gear('test')
rarity = df['rarity']
print(rarity)

def punch(attacker):
    might_dict = cc.Character(attacker).__getattribute__('might')
    sex = cc.Character(attacker).__getattribute__('sex')
    for key,val in might_dict.items():
        if key == f"{sex}_punch":
            return val
        
def kick(attacker):
    might_dict = cc.Character(attacker).__getattribute__('might')
    sex = cc.Character(attacker).__getattribute__('sex')
    for key,val in might_dict.items():
        if key == f"{sex}_kick":
            return val

        
def bludgeon(attacker):
    might_modifier = punch(attacker)

    all_wieldables = []
    for hand in range(4):
        hand_count = hand+1
        # print(hand_count)
        equiped_in_hand = cc.Character(attacker).__getattribute__(f'hand_slot_{hand_count}')
        wielded_name = equiped_in_hand.split(' | ')[0]
        all_wieldables.append(wielded_name)
        # print(all_wieldables)
        # print(items_df)
    def hand_selection(): 
        hand_used = input("Which hand would you like to bludgeon with?\n\n 1 | 2 | 3 | 4\n\n")
        if int(hand_used) == 1:
            for i,item in enumerate(items_df['name']):
                # print(item)
                if all_wieldables[0] in item:
                    # print(f'{item} is in row {i}')
                    bludgeoning_dmg = int(items_df.loc[i, "bludgeoning_dmg"])
                    total_dmg = bludgeoning_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 2:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[1] in item:
                    # print(f'{item} is in row {i}')
                    bludgeoning_dmg = int(items_df.loc[i, "bludgeoning_dmg"])
                    total_dmg = bludgeoning_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 3:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[2] in item:
                    # print(f'{item} is in row {i}')
                    bludgeoning_dmg = int(items_df.loc[i, "bludgeoning_dmg"])
                    total_dmg = bludgeoning_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 4:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[3] in item:
                    # print(f'{item} is in row {i}')
                    bludgeoning_dmg = int(items_df.loc[i, "bludgeoning_dmg"])
                    total_dmg = bludgeoning_dmg + might_modifier
                    return total_dmg
        else:
            print("None found")
            hand_selection()
    dmg = hand_selection()
    return dmg

def pierce(attacker):
    might_modifier = punch(attacker)

    all_wieldables = []
    for hand in range(4):
        hand_count = hand+1
        # print(hand_count)
        equiped_in_hand = cc.Character(attacker).__getattribute__(f'hand_slot_{hand_count}')
        wielded_name = equiped_in_hand.split(' | ')[0]
        all_wieldables.append(wielded_name)
        # print(all_wieldables)
        # print(items_df)
    def hand_selection(): 
        hand_used = input("Which hand would you like to pierce with?\n\n 1 | 2 | 3 | 4\n\n")
        if int(hand_used) == 1:
            for i,item in enumerate(items_df['name']):
                # print(item)
                if all_wieldables[0] in item:
                    # print(f'{item} is in row {i}')
                    piercing_dmg = int(items_df.loc[i, "piercing_dmg"])
                    total_dmg = piercing_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 2:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[1] in item:
                    # print(f'{item} is in row {i}')
                    piercing_dmg = int(items_df.loc[i, "piercing_dmg"])
                    total_dmg = piercing_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 3:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[2] in item:
                    # print(f'{item} is in row {i}')
                    piercing_dmg = int(items_df.loc[i, "piercing_dmg"])
                    total_dmg = piercing_dmg + might_modifier
                    return total_dmg
        elif int(hand_used) == 4:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[3] in item:
                    # print(f'{item} is in row {i}')
                    piercing_dmg = int(items_df.loc[i, "piercing_dmg"])
                    total_dmg = piercing_dmg + might_modifier
                    # print(f"{piercing_dmg} + {might_modifier}")
                    # print(total_dmg)
                    return total_dmg
        else:
            print("None found")
    dmg = hand_selection()
    return dmg

def slash(attacker):
    might_modifier = punch(attacker)

    all_wieldables = []
    for hand in range(4):
        hand_count = hand+1
        # print(hand_count)
        equiped_in_hand = cc.Character(attacker).__getattribute__(f'hand_slot_{hand_count}')
        wielded_name = equiped_in_hand.split(' | ')[0]
        all_wieldables.append(wielded_name)
        # print(all_wieldables)
        # print(items_df)

    def hand_selection(): 
        hand_used = input("Which hand would you like to slash with?\n\n 1 | 2 | 3 | 4\n\n")
        if int(hand_used) == 1:
            for i,item in enumerate(items_df['name']):
                # print(item)
                if all_wieldables[0] in item:
                    # print(f'{item} is in row {i}')
                    slashing_dmg = int(items_df.loc[i, "slashing_dmg"])
                    total_dmg = slashing_dmg + might_modifier
                    # print(f'{total_dmg} dmg dealt')
                    return total_dmg
        elif int(hand_used) == 2:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[1] in item:
                    # print(f'{item} is in row {i}')
                    slashing_dmg = int(items_df.loc[i, "slashing_dmg"])
                    total_dmg = slashing_dmg + might_modifier
                    # print(f'{total_dmg} dmg dealt')
                    return total_dmg
        elif int(hand_used) == 3:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[2] in item:
                    # print(f'{item} is in row {i}')
                    slashing_dmg = int(items_df.loc[i, "slashing_dmg"])
                    total_dmg = slashing_dmg + might_modifier
                    # print(f'{total_dmg} dmg dealt')
                    return total_dmg
        elif int(hand_used) == 4:
            for i,item in enumerate(items_df['name']):
                if all_wieldables[3] in item:
                    # print(f'{item} is in row {i}')
                    slashing_dmg = int(items_df.loc[i, "slashing_dmg"])
                    total_dmg = slashing_dmg + might_modifier
                    # print(f"{slashing_dmg} + {might_modifier}")
                    # print(f'{total_dmg} dmg dealt')
                    # print(type(total_dmg))
                    # print(total_dmg)
                    return total_dmg
        else:
            print("None found")
            hand_selection()
    dmg = hand_selection()
    # print(dmg)
    # print(type(dmg))
    return dmg
    

    
# bludgeon('test')
# print(pierce('test'))
# answer = slash('test')
# print(slash('test'))
# print(answer)
# test = slash('test')
# print(test)
# print(test)

melee_strikes = {
    'punch': (punch,2),
    'kick': (kick,5),
    'bludgeon': (bludgeon,7),
    'pierce': (pierce,3),
    'slash': (slash, 4),
}

def hit(attacker,strike,defender,limb):
    global CHARACTER_DATA
    global combat_characters_active_stats

    dmg_abosorbtion = cc.Character(defender).__getattribute__("dmg_absorbtion")[f'{sex(defender)}_{limb}']

    for key,val in combat_characters_active_stats.items():
        # print(key,val)
        if defender in key:
            for target_limb,hp in val.items():
                # print(target_limb,hp)
                if limb in target_limb.lower():
                    limb_hp = hp
                    affected_limb = target_limb
                    affected_key = key
                    # print(f"Limb is {limb}, limb hp is {limb_hp}")
    if strike.lower() in melee_strikes:
        if strike in ['punch','kick']:
            dmg = melee_strikes[strike.lower()]
            new_limb_hp = limb_hp + dmg_abosorbtion - dmg[0](attacker)
            if new_limb_hp > limb_hp:
                new_limb_hp = limb_hp
            
            print(f'{cc.Character(defender).__getattribute__("name").title()} was hit with {strike} in the {limb} by {cc.Character(attacker).__getattribute__("name").title()}'
                f' for {dmg[0](attacker)} damage! \n\n'
                f'{limb_hp} ({dmg_abosorbtion}) - {dmg[0](attacker)} --> {new_limb_hp}')
        else:
            strike_type = melee_strikes[strike.lower()]
            dmg = strike_type[0](attacker)
            new_limb_hp = limb_hp + dmg_abosorbtion - dmg
            if new_limb_hp > limb_hp:
                new_limb_hp = limb_hp
            
            print(f'{cc.Character(defender).__getattribute__("name").title()} was hit with {strike} in the {limb} by {cc.Character(attacker).__getattribute__("name").title()}'
                f' for {dmg} damage! \n\n'
                f'{limb_hp}hp ({dmg_abosorbtion}abs) - {dmg}hp --> {new_limb_hp}hp')
        
        if new_limb_hp <= 0:
            if limb in ['cranium','throat','ribs','sternum']:
                print(f'{defender} has been killed!')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            elif limb in ['abdomen','back','glute','quad','hamstring','knee','shin','calve','foot']:
                print('decreased mobility')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            elif limb in ['pec','armpit','shoulder','upper_arm','elbow','forearm','hand']:
                print('decreased motor skills')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            elif limb == 'eyes':
                print('blind')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            elif limb == 'spine':
                print('paralyzed')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            else:
                print(f'{limb} destroyed')
                combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
        elif new_limb_hp > 0:
            combat_characters_active_stats[affected_key][affected_limb] = new_limb_hp
            # additional debuffs depending on percentage of dmg here

# hit('op','slash','weak','quads_r')

def static_melee_aim(attacker,strike,defender,limb):
    global combat_characters_active_stats
    attacker = cc.Character(attacker).__getattribute__('name')
    defender = cc.Character(defender).__getattribute__('name')

    for key in combat_characters_active_stats.keys():
        if attacker in key:
            attacker_key = key
            # print(attacker_key)
        if defender in key:
            defender_key = key
    
    attacker_fatigue_modifier = combat_characters_active_stats[attacker_key]['fatigue_level'][1]
    defender_fatigue_modifier = combat_characters_active_stats[defender_key]['fatigue_level'][1]

    melee_accuracy_val = cc.Character(attacker).__getattribute__('aim')[f'{sex(attacker)}_melee_accuracy'] * attacker_fatigue_modifier
    percent_roll = random.randint(0,100)
    if can_move == True:
        if melee_accuracy_val * (100/cc.Character(attacker).__getattribute__('aim')[f'{sex(attacker)}_hand_eye_coord']) > percent_roll:
            percent_roll = random.randint(0,100)
            # if combat_characters_active_stats[attacker_key]
            if (cc.Character(defender).__getattribute__('parry')[f'{sex(defender)}']* defender_fatigue_modifier) > percent_roll:
                print(f'⚔️ PARRY⚔️')
            else:
                percent_roll = random.randint(0,100)
                if (cc.Character(defender).__getattribute__('hit_avoidance_chance')[f'{sex(defender)}']* defender_fatigue_modifier) > percent_roll:
                    print('💨DODGE💨')
                else:
                    percent_roll = random.randint(0,100)
                    if (cc.Character(defender).__getattribute__('block_chance')[f'{sex(defender)}']* defender_fatigue_modifier) > percent_roll:
                        print('🛡️ BLOCK🛡️')
                    else:
                        hit(attacker,strike,defender,limb)
        else:
            print('🛟 MISS🛟')
    else: 
        print('Too tired to make more moves')

combat_characters_active_stats = {}

def combat(*args):
    [[delete_character(character)] for character in args]

    [[add_character(character)] for character in args]
    load_character_data()

    # print(CHARACTER_DATA)
    for num,character in enumerate(args):
        key = f'{num}_{character}'
        if key not in combat_characters_active_stats:
            combat_characters_active_stats[key] = {}
            for part,hp_val in hp(character).items():
                combat_characters_active_stats[key][part] = hp_val
            # combat_characters_active_stats[key] = inventory(character)
            for etype,armor_name in equipment(character).items():
                combat_characters_active_stats[key][etype] = armor_name
            # combat_characters_active_stats[key] = hand_slots(character)
            # combat_characters_active_stats[key] = accessories(character)
            # combat_characters_active_stats[key] = status_effects(character)
            # combat_characters_active_stats[key] = stress(character)
            # combat_characters_active_stats[key] = relationships(character)
            combat_characters_active_stats[key]['total_fatigue'] = 0
            combat_characters_active_stats[key]['fatigue_level'] = ("no",1)

    # print(combat_characters_active_stats)

    combat_continues = True
    while combat_continues == True:
        for key in combat_characters_active_stats.keys():
            attacker = key.split("_",1)[1]
            total_fatigue = combat_characters_active_stats[key]['total_fatigue']
            combat_characters_active_stats[key]['possible_moves'] = 5
            possible_moves = combat_characters_active_stats[key]['possible_moves']

            
            print(f"\n{attacker.title()}'s turn!\n"
                f"Total Fatigue = {total_fatigue}")
            
            while possible_moves > 0:
                choice = input('\nMove (m) or rest (spacebar)?\n\nENTER HERE | ')
                if choice == ' ':
                    rest = round(total_fatigue - 0.2 * cc.Character(attacker).__getattribute__('muscular_endurance')[f'{sex(attacker)}'])
                    if rest < 0:
                        total_fatigue = 0
                    else:
                        total_fatigue = rest
                    print(total_fatigue)

                else:
                    defender = input(f"\nWhat enemy would you like to target?\n").lower()
                    if defender not in CHARACTER_DATA['name']:
                        try_again = False
                        while try_again == False:
                            defender = input(f"\nNo combatant caleld {defender} found!\n\n"
                                            f"What enemy would you like to target?\n").lower()
                            if defender not in CHARACTER_DATA['name']:
                                continue
                            else:
                                try_again = True

                    strike = input("\nWhat strike would you like to use?\n").lower()
                    if strike not in melee_strikes.keys():
                        try_again = False
                        while try_again == False:
                            strike = input(f"\nNo strike called {strike} found!\n\n"
                                            f"What strike would you like to use?\n").lower()
                            if strike not in melee_strikes.keys():
                                continue
                            else:
                                try_again = True
                                
                    list_of_limbs = []
                    [[list_of_limbs.append((limb.split(f"{sex(defender)}_"))[1])] for limb in hp(defender).keys()]
                    # [[list_of_limbs.append(limb)] for limb in hp(defender).keys()]
                    print(list_of_limbs)

                    limb = input(f"\nWhat limb would you like to target?\n").lower()
                    if limb not in list_of_limbs:
                        try_again = False
                        while try_again == False:
                            limb = input(f"\nNo limb caleld {limb} found!\n\n"
                                            f"What limb would you like to target?\n").lower()
                            if limb not in list_of_limbs:
                                continue
                            else:
                                try_again = True


                    # print(attacker)
                    static_melee_aim(attacker,strike,defender,limb)
                    if strike.lower() in melee_strikes:
                        added_fatigue = melee_strikes[strike.lower()][1]
                        total_fatigue = total_fatigue + added_fatigue
                combat_characters_active_stats[key]['total_fatigue'] = total_fatigue
                muscular_endurance = cc.Character(attacker).__getattribute__('muscular_endurance')[f'{sex(attacker)}']
                if total_fatigue >= muscular_endurance:
                    print('Exhausted')
                    combat_characters_active_stats[key]['fatigue_level'] = ('exhausted', 0.5)
                    possible_moves = possible_moves - 5
                elif total_fatigue >= 0.8 * muscular_endurance:
                    print('Critical Fatigue')
                    combat_characters_active_stats[key]['fatigue_level'] = ('critical',0.6)
                    possible_moves = possible_moves - 4
                elif total_fatigue >= 0.6 * muscular_endurance:
                    print('High Fatigue')
                    combat_characters_active_stats[key]['fatigue_level'] = ('high',0.7)
                    possible_moves = possible_moves - 3 
                elif total_fatigue >= 0.4 * muscular_endurance:
                    print('Medium Fatigue')
                    combat_characters_active_stats[key]['fatigue_level'] = ('medium',0.8)
                    possible_moves = possible_moves - 2
                elif total_fatigue >= 0.2 * muscular_endurance:
                    print('Low Fatigue')
                    combat_characters_active_stats[key]['fatigue_level'] = ('low',0.9)
                    possible_moves = possible_moves - 1
                elif total_fatigue < 0.2 * muscular_endurance:
                    print('No Fatigue')
                    combat_characters_active_stats[key]['fatigue_level'] = ('no',1)
                print(f'{total_fatigue} fatigue')
                possible_moves = possible_moves - 1

                    
        next_round = input('\nContinue? Y or N\n')
        if next_round.lower() == 'n':
            combat_continues = False
    [[delete_character(character)] for character in args]

combat("op",'weak')

# print(static_melee_aim())

### ADD Damge Over Time, ENERGY/FATIGUE, ARMOR + EQUIPMENT, RANGED, and ACTIVE

# MAKE IT SO THAT DIFFERENT ATTACKS TAKE UP A DIFFERENT NUMBER OF FATIGUE / MOVES
# ENABLE AUTOREST TO CERTAIN FATIGUE THRESHOLDS

