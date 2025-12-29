import character_table as ct
import tkinter as tk
from tkinter import ttk, messagebox
from background import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import json
import os

# Connect to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTER_DB_PATH = os.path.join(BASE_DIR,'characters.db')
conn = connect(CHARACTER_DB_PATH)
cursor = conn.cursor()

def load_character_data():
    global CHARACTER_DATA
    try:
        df = pd.read_sql('SELECT * FROM characters', conn)
        CHARACTER_DATA = df.to_dict(orient='list')
        print('characters df accessed.')
    except Exception as e:
        print("Initializing empty database:", e)
        return

load_character_data()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_DB_PATH = os.path.join(BASE_DIR,'items.db')
items_conn = connect(ITEMS_DB_PATH)
items_cursor = items_conn.cursor()

def load_item_data():
    global ITEM_DATA
    try:
        df = pd.read_sql('SELECT * FROM items', items_conn)
        ITEM_DATA = df.to_dict(orient='list')
        print('items df accessed.')
    except:
        print("Initializing empty database:")
        return

load_item_data()

# Define core stat main_demographics
main_demographics = [
    "name", "sex", "faction", "gods", "mortal_type", "mortal_subtype",'level',

    'strength', 
    'agility', 
    'vitality', 
    'cognition', 
    'sagacity', 
    'influence', 
    
    'openness',
    'conscientiousness',
    'extraversion',
    'agreeableness',
    'neuroticism',

    'randomize_stats'
]

inventory_options = ['inventory',]

wield_options = ['slot_1','slot_2','slot_3','slot_4',]

equipment_options = [
    # Equipment
    'helmet','visor','gorget','coif','arming_cap', # gorget for neck and throat, coif for additional protection of cranium+neck, arming_cap for comfort+cranium,
    'gambeson','haubergeon','breastplate','backplate','plackart', # gambeson for whole torso (base layer fabric), haubergeon for whole torso (second layer mail), plackart for abdominal plate
    'r_pauldron','l_pauldron','r_spaulder','l_spaulder','upper_gousset','r_vambrace','l_vambrace','r_gauntlet','l_gauntlet', # pauldron for shoulders, spaulder for upper arm, vambrace for forearm, Gousset for flexible joints that dont allow for rigid protection
    'chausses','culet','mail_skirt','codpiece','lower_gousset','r_tasset','l_tasset','r_poleyn','l_poleyn','r_greave','l_greave','r_sabaton','l_sabaton', # chausses for whole legs, culet for lwoer back and buttocks, tasset fore upper legs, grieves for lower legs, poleyn for the knees, sabatons for feet
]

accessories_options = [
    'hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
    'ring','necklace','bracelet','eye_piece','mask','implant','gadget',
]

class CharacterCreatorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Character Creator")
        global entry_var
        entry_var = tk.StringVar()

        self.entries = {}
        self.widgets = []

        self.main_page()

    def main_page(self):
        entry_var = tk.StringVar()
        entry_var.trace_add('write', lambda *args: entry_var.set(entry_var.get().lower()))
        
        # Layout
        for i, field in enumerate(main_demographics):
            label = tk.Label(root, text=field.capitalize())
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            self.widgets.append(label)

            name_entry = ttk.Combobox(root,textvariable=entry_var)
            sex_entry = ttk.Combobox(root, values=SEX, state='readonly')
            faction_entry = ttk.Combobox(root, values=FACTIONS, state='readonly')
            gods_entry = ttk.Combobox(root, values=GODS, state='readonly')

            mortal_type_entry = ttk.Combobox(root, values=list(MORTALS_DICTIONARY.keys()), state='readonly')
            mortal_type_entry.bind("<<ComboboxSelected>>", self.update_subtypes)

            mortal_subtype_entry = ttk.Combobox(root, state='disabled')

            level_entry= tk.Spinbox(root,from_=1,to=1000)

            attributes_var = tk.IntVar(value=10)
            strength_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)
            agility_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)
            vitality_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)
            cognition_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)
            sagacity_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)
            influence_entry = tk.Spinbox(root,to=40,textvariable=attributes_var)

            personality_var = tk.IntVar(value=50)
            openness_entry = tk.Spinbox(root,to=100,textvariable=personality_var)
            conscientiousness_entry = tk.Spinbox(root,to=100,textvariable=personality_var)
            extraversion_entry = tk.Spinbox(root,to=100,textvariable=personality_var)
            agreeableness_entry = tk.Spinbox(root,to=100,textvariable=personality_var)
            neuroticism_entry = tk.Spinbox(root,to=100,textvariable=personality_var)

            randomize_var = tk.IntVar()
            randomize_stats_entry = tk.Checkbutton(root,variable=randomize_var)
            

            if field == "name":
                name_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['name'] = name_entry
                self.widgets.append(name_entry)
            elif field == 'sex':
                sex_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['sex'] = sex_entry
                self.widgets.append(sex_entry)
            elif field == "faction":
                faction_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['faction'] = faction_entry
                self.widgets.append(faction_entry)
            elif field == "gods":
                gods_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['gods'] = gods_entry
                self.widgets.append(gods_entry)

            elif field == "mortal_type":
                mortal_type_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['mortal_type'] = mortal_type_entry
                self.widgets.append(mortal_type_entry)
            elif field == "mortal_subtype":
                mortal_subtype_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['mortal_subtype'] = mortal_subtype_entry
                self.widgets.append(mortal_subtype_entry)
                
            elif field == "level":
                level_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['level'] = level_entry
                self.widgets.append(level_entry)

            elif field == "strength":
                strength_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['strength'] = strength_entry
                self.widgets.append(strength_entry)
            elif field == "agility":
                agility_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['agility'] = agility_entry
                self.widgets.append(agility_entry)
            elif field == "vitality":
                vitality_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['vitality'] = vitality_entry
                self.widgets.append(vitality_entry)
            elif field == "cognition":
                cognition_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['cognition'] = cognition_entry
                self.widgets.append(cognition_entry)
            elif field == "sagacity":
                sagacity_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['sagacity'] = sagacity_entry
                self.widgets.append(sagacity_entry)
            elif field == "influence":
                influence_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['influence'] = influence_entry
                self.widgets.append(influence_entry)

            elif field == "openness":
                openness_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['openness'] = openness_entry
                self.widgets.append(openness_entry)
            elif field == "conscientiousness":
                conscientiousness_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['conscientiousness'] = conscientiousness_entry
                self.widgets.append(conscientiousness_entry)
            elif field == "extraversion":
                extraversion_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['extraversion'] = extraversion_entry
                self.widgets.append(extraversion_entry)
            elif field == "agreeableness":
                agreeableness_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['agreeableness'] = agreeableness_entry
                self.widgets.append(agreeableness_entry)
            elif field == "neuroticism":
                neuroticism_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['neuroticism'] = neuroticism_entry
                self.widgets.append(neuroticism_entry)

            elif field == "randomize_stats":
                randomize_stats_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries['randomize_stats'] = randomize_var
                self.widgets.append(randomize_stats_entry)

        submit_main_btn = tk.Button(root, text="Save Stats | Next Page", command=self.save_character_stats)
        submit_main_btn.grid(row=len(main_demographics)+2, column=0, columnspan=4, pady=10)
        self.widgets.append(submit_main_btn)  

    
    def wield_page(self):
        entry_var = tk.StringVar()
        entry_var.trace_add('write', self.to_lower)

        handed_label = tk.Label(root, text="Select up to 4 wielded items")
        handed_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.widgets.append(handed_label)

        global on_level_wield
        on_level_wield = []

        for position_index, item_level in enumerate(ITEM_DATA['level']):
            if item_level <= active_character['level'] and str(ITEM_DATA['wield'][position_index]) == '1':
                on_level_wield.append((ITEM_DATA['name'][position_index], ITEM_DATA['one_or_two_handed'][position_index]))
                
        self.wielded_items = {}
        for i in range(4):
            label = tk.Label(root, text=f'Hand Slot {i + 1}')
            label.grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
            self.widgets.append(label)

            item_values = []
            for item,hand in on_level_wield:
                item_values.append(f'{item} | {hand} handed')

            print(item_values)
            if label.cget("text") == 'Hand Slot 1':
                hand_slot_entry = ttk.Combobox(root, values=item_values, state='readonly')
                hand_slot_entry.grid(row=i+1, column=1, sticky="e", padx=5, pady=5)
                self.wielded_items[f'hand_slot_{i + 1}'] = hand_slot_entry
                self.widgets.append(hand_slot_entry)
                hand_slot_entry.bind("<<ComboboxSelected>>", self.update_hands)
            elif label.cget("text") == 'Hand Slot 3':
                hand_slot_entry = ttk.Combobox(root, values=item_values, state='readonly')
                hand_slot_entry.grid(row=i+1, column=1, sticky="e", padx=5, pady=5)
                self.wielded_items[f'hand_slot_{i + 1}'] = hand_slot_entry
                self.widgets.append(hand_slot_entry)
                hand_slot_entry.bind("<<ComboboxSelected>>", self.update_hands)
            else:
                hand_slot_entry = ttk.Combobox(root, state='disabled')
                hand_slot_entry.grid(row=i+1, column=1, sticky="e", padx=5, pady=5)
                self.wielded_items[f'hand_slot_{i + 1}'] = hand_slot_entry
                self.widgets.append(hand_slot_entry)
                
        submit_wield_page = tk.Button(root, text="Save Wieldables | Next Page", command=self.save_wieldables)
        submit_wield_page.grid(row=6, column=0, columnspan=4, pady=10)
        self.widgets.append(submit_wield_page)  

    def equipment_page(self):
            equip_label = tk.Label(root, text="Select equipment that this character will wear")
            equip_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            self.widgets.append(equip_label)

            self.on_level_equip = []

            for position_index, item_level in enumerate(ITEM_DATA['level']):
                if item_level <= active_character['level'] and str(ITEM_DATA['armor'][position_index]) == '1':
                    self.on_level_equip.append((ITEM_DATA['name'][position_index], ITEM_DATA['armor_equip_type'][position_index]))

            self.equipped_gear = []
            self.equipment_vars = []

            for i, item in enumerate(self.on_level_equip):
                name, equip_type = item
                frame = tk.Frame(self.root)
                frame.grid(row=i+1, column=0, columnspan=2, sticky='w')


                label = tk.Label(frame, text=f"{name} | ({equip_type})")
                label.pack(side='left')

                var = tk.IntVar()
                checkbutton = tk.Checkbutton(
                    frame, variable=var,
                    command=lambda idx=i: self.update_equipped(idx)
                )
                checkbutton.pack(side='right')

                self.equipment_vars.append((var, name, equip_type))
                self.widgets.extend([frame, label, checkbutton])

            submit_wield_page = tk.Button(root, text="Save Equipped Gear | Next Page", command=self.save_equipped)
            submit_wield_page.grid(row=len(self.on_level_equip)+2, column=0, columnspan=4, pady=10)
            self.widgets.append(submit_wield_page)  

####################

    def update_subtypes(self, event):
        selected_type = self.entries['mortal_type'].get()
        subtype_box_2 = self.entries['mortal_subtype']
        options = MORTALS_DICTIONARY.get(selected_type, [])
        subtype_box_2.config(values=options, state="readonly")
        subtype_box_2.set('')

    def update_hands(self, event):
        for hand_slot,value in self.wielded_items.items():
            value = value.get()
            if hand_slot == "hand_slot_1":
                if "1 handed" in value:
                    subtype_box_2 = self.wielded_items['hand_slot_2']

                    one_hand_options = []
                    for item,hand in on_level_wield:
                        if hand == '1':
                            one_hand_options.append(f'{item} | {hand} handed')

                    subtype_box_2.config(values=one_hand_options, state="readonly")
                elif "1 handed" not in value:
                    subtype_box_2 = self.wielded_items['hand_slot_2']
                    subtype_box_2.config(state="disabled")
                    subtype_box_2.set('')
            elif hand_slot == "hand_slot_3":
                if "1 handed" in value:
                    subtype_box_4 = self.wielded_items['hand_slot_4']

                    one_hand_options = []
                    for item,hand in on_level_wield:
                        if hand == '1':
                            one_hand_options.append(f'{item} | {hand} handed')

                    subtype_box_4.config(values=one_hand_options, state="readonly")
                    subtype_box_4.set('')
                elif "1 handed" not in value:
                    subtype_box_4 = self.wielded_items['hand_slot_4']
                    subtype_box_4.config(state="disabled")
                    

    def update_equipped(self, idx):
        var, name, equip_type = self.equipment_vars[idx]

        if var.get() == 1:  
            for _, etype in self.equipped_gear:
                if etype == equip_type:
                    var.set(0)  
                    messagebox.showwarning("Already Equipped", f"The '{equip_type}' spot is already equipped.")
                    return
            self.equipped_gear.append((name, equip_type))

        else:  # Unchecking
            self.equipped_gear = [(n, t) for n, t in self.equipped_gear if n != name]



    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        
    def to_lower(self,*args):
        current = entry_var.get()
        lower = current.lower()
        if current != lower:
            entry_var.set(lower) 

    def save_character_stats(self):
        data = {}

        for field in main_demographics:
            val = self.entries[field].get()
            if field in ['strength', 'agility', 'vitality', 'cognition', 'sagacity', 'influence',
                        'openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism',]:
                try:                     
                    data[field] = int(val)
                    if field == 'strength':
                        data['Brawn'] = int(val)
                        data['might'] = int(val)
                        data['skeletal_muscle_mass'] = int(val)
                        data['explosiveness'] = int(val)
                        data['carrying_capacity'] = int(val)
                        data['block_chance'] = int(val)
                        data['Stamina'] = int(val)
                        data['muscular_endurance'] = int(val)
                        data['grip'] = int(val)
                        data['gross_motor_control'] = int(val)

                    elif field == 'agility':
                        data['dodge'] = int(val)
                        data['reflexes'] = int(val)
                        data['hit_avoidance_chance'] = int(val)
                        data['stealth'] = int(val)
                        data['mobility'] = int(val)
                        data['balance'] = int(val)
                        data['speed'] = int(val)
                        data['flexibility'] = int(val)
                        data['acrobatics'] = int(val)
                        data['precision'] = int(val)
                        data['fine_motor_control'] = int(val)
                        data['aim'] = int(val)
                        data['targeting'] = int(val)
                        data['parry'] = int(val)

                    elif field == 'vitality':
                        data['resilience'] = int(val)
                        data['pain_tolerance'] = int(val)
                        data['durability'] = int(val)
                        data['dmg_absorbtion'] = int(val)
                        data['vigor'] = int(val)
                        data['recovery_rate'] = int(val)
                        data['intervention_receptivity'] = int(val)
                        data['resistance'] = int(val)

                    elif field == 'cognition':
                        data['memory'] = int(val)
                        data['information_retention'] = int(val)
                        data['logic'] = int(val)
                        data['reasoning'] = int(val)
                        data['fluency'] = int(val)
                        data['processing_speed'] = int(val)

                    elif field == 'sagacity':
                        data['perception'] = int(val)
                        data['situational_awareness'] = int(val)
                        data['sensory_sensitivity'] = int(val)
                        data['intuition'] = int(val)
                        data['instincts'] = int(val)
                        data['o_interpersonal_insigt'] = int(val)
                        data['s_intrapersonal_insight'] = int(val)
                        data['composure'] = int(val)
                        data['stress_modulation'] = int(val)
                        data['emotional_stability'] = int(val)

                    elif field == 'influence':
                        data['charm'] = int(val)
                        data['intimidation'] = int(val)
                        data['seduction'] = int(val)
                        data['deception'] = int(val)

                    elif field == 'randomize_stats':
                        data['randomize_stats'] = int(val)
                except:
                    data[field] = 0
            else:
                data[field] = val


        if not data["name"] or not data["sex"] or not data["faction"] or not data["gods"] or not data["mortal_type"] or not data["mortal_subtype"]:
            messagebox.showerror("Error", "name, sex, faction, god, and mortal_types/subtypes are required to make a character.")
            return

        try:
            placeholders = ', '.join('?' * len(data))
            columns = ', '.join(data.keys())
            sql = f'INSERT INTO characters ({columns}) VALUES ({placeholders})'
            cursor.execute(sql, list(data.values()))
            conn.commit()
            messagebox.showinfo("Saved", f"{data['name'].title()}'s main stats were saved to character.db")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        global active_character 
        active_character = {}
        for key,field in data.items():
            active_character[key] = field

        self.clear_widgets()
        self.wield_page()

    def save_wieldables(self):
        wieldable_inventory = {}
        for hand,item in self.wielded_items.items():
            wieldable_inventory[hand] = item.get()
        try:
            global character_name
            character_name = active_character['name'] 
            hand_list = []
            item_list = []
            for hand,item in wieldable_inventory.items():
                hand_list.append(hand)
                item_list.append(item)
            set_clause = ', '.join(f"{col} = ?" for col in hand_list)
            sql = f'UPDATE characters SET {set_clause} WHERE name = ?'
            cursor.execute(sql, item_list + [character_name])
            conn.commit()
            messagebox.showinfo("Saved", "Wieldables were saved to character.db")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        self.clear_widgets()
        self.equipment_page()

    def save_equipped(self):
        try:
            for item in self.equipped_gear:
                # global character_name
                name,equip_type = item
                equip_json = json.dumps(item)
                character_name = active_character['name'] 
                sql = f'UPDATE characters SET {equip_type} = ? WHERE name = ?'
                cursor.execute(sql, (equip_json, character_name))
            conn.commit()
            messagebox.showinfo("Saved", "Equipped Gear was saved to character.db")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        self.clear_widgets()
        self.main_page()

# Launch the GUI
root = tk.Tk()
app = CharacterCreatorGUI(root)
root.mainloop()


