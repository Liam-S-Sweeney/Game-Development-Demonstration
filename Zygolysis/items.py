from lore import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os
# os.remove('items.db')

expected_column_order = ['name','weight','rarity','description','stack_size','unique_traits','components','value','level',
            
    'wield',
        'bludgeoning_dmg','piercing_dmg','slashing_dmg','attack_speed','attack_range','energy_cost','block','wield_strength_check','wield_durability','one_or_two_handed',
    'armor',

        'cranium_coverage',                                            
        'eye_coverage',                         
        'nose_coverage',                     
        'wield_durability',                   
        'neck_coverage',                     
        'throat_coverage',                     

        # UPPER TORSO               
        'pec_coverage',                                 
        'rib_coverage',                   
        'sternum_coverage',                     
        'heart_coverage',                                       
        'lung_coverage',                  
        'diaphragm_coverage',                  
        'thoracic_viscera_coverage',     
        'liver_coverage',                     

        # LOWER TORSO
        'abdomen_coverage', 
        'abdominal_viscera_coverage',
        'spleen_coverage',
        'groin_coverage',        

        # BACK
        'spine_coverage',                        
        'upper_back_coverage', 
        'lower_back_coverage',
        'kidney_coverage',                 

        # LEGS     
        'glute_coverage',          
        'quad_coverage',      
        'hamstring_coverage',             
        'knee_coverage',                               
        'shin_coverage',                   
        'calf_coverage',         
        'foot_coverage',   

        # ARMS   
        'shoulder_coverage',      
        'armpit_coverage',               
        'upper_arm_coverage',                 
        'elbow_coverage',                          
        'forearm_coverage',     
        'hand_coverage',

        'mobility_modifier','bludgeoning_res','piercing_res','slashing_res','armor_strength_check','armor_durability','armor_equip_type',
    'accessories',
        'accessories_equip_type', # clothing and wearables
    'consumables',
        'buffs','debuffs','duration','cooldown','nutritional_value',
    'ammo',
        'ammo_bludgeoning_dmg','ammo_piercing_dmg','ammo_slashing_dmg','area_of_effect',
    'materials',
        # necessary for crafting
    'special',
        # necessary for plot
    'currency',
        # used just for money
    'misc',
        # all other items   
]

rarity_scale_list = ['shoddy','average','superior','exceptional','flawless']
one_or_two_handed_list = [1,2]
armor_equip_type_list = ['helmet','face','gorget','coif','arming_cap', # gorget for neck and throat, coif for additional protection of cranium+neck, arming_cap for comfort+cranium,
                    'gambeson','haubergeon','breastplate','backplate','abdominal_plate', # gambeson for whole torso (base layer fabric), haubergeon for whole torso (second layer mail)
                    'pauldrons','spaulders','upper_gousset','vambraces','gauntlets', # pauldrons for shoulders, spaulders for upper arm, vambrace for forearm, 
                    'chausses','culet','mail_skirt','codpiece','tassets','kneecups','greaves','sabatons','lower_gusset'] 
                    # chausses for whole legs, culet for upper glute, codpiece for groin, tasset for upper legs, grieves for lower legs, sabatons for feet
accessories_equip_type_list = ['hat','upper_face','lower_face','scarf','jacket','shirt','bottoms','belt','socks','undergarment','shoes',
                        'ring','necklace','bracelet','eye_piece','mask','implant','gadget']

# ITEM_DB_PATH = r'C:\Users\15086\Desktop\Zygolysis\items.db'
# item_conn = connect(ITEM_DB_PATH)
# item_cursor = item_conn.cursor()

def load_character_data():
    global ITEM_DATA
    global ITEM_CONN
    global ITEM_CURSOR

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ITEMS_DB_PATH = os.path.join(BASE_DIR,'items.db')
    ITEM_CONN = connect(ITEMS_DB_PATH)
    ITEM_CURSOR = ITEM_CONN.cursor()
    

    try:
        df = pd.read_sql('SELECT * FROM items', ITEM_CONN)
        ITEM_DATA = df.to_dict(orient='list')
    except Exception as e:
        print('Initializing empty database:', e)

        ITEM_DATA = {column: [] for column in expected_column_order}

        columns_def = ', '.join(f'"{col}" TEXT' for col in expected_column_order)
        ITEM_CURSOR.execute(f"CREATE TABLE IF NOT EXISTS items ({columns_def})")
        ITEM_CONN.commit()
    return ITEM_CONN, ITEM_CURSOR

load_character_data()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ITEMS_DB_PATH = os.path.join(BASE_DIR,'items.db')
# ITEM_CONN = connect(ITEMS_DB_PATH)
# ITEM_CURSOR = ITEM_CONN.cursor()

def save_item_to_db():
    df = pd.DataFrame({key: [ITEM_DATA[key][-1]] for key in ITEM_DATA})
    df.to_sql('items', ITEM_CONN, if_exists='append',index=False)

def new_item(name, weight, rarity, description, stack_size, unique_traits, components, value, level,
wield,
    bludgeoning_dmg, piercing_dmg, slashing_dmg, attack_speed, attack_range, energy_cost, block, wield_strength_check, wield_durability, one_or_two_handed,
armor,

    cranium_coverage,                                            
    eye_coverage,                         
    nose_coverage,                     
    jaw_coverage,                   
    neck_coverage,                     
    throat_coverage,                     

    # UPPER TORSO               
    pec_coverage,                                 
    rib_coverage,                   
    sternum_coverage,                     
    heart_coverage,                                       
    lung_coverage,                  
    diaphragm_coverage,                  
    thoracic_viscera_coverage,     
    liver_coverage,                     

    # LOWER TORSO
    abdomen_coverage, 
    abdominal_viscera_coverage,
    spleen_coverage,
    groin_coverage,        

    # BACK
    spine_coverage,                        
    upper_back_coverage, 
    lower_back_coverage,
    kidney_coverage,                 

    # LEGS     
    glute_coverage,          
    quad_coverage,      
    hamstring_coverage,             
    knee_coverage,                               
    shin_coverage,                   
    calf_coverage,         
    foot_coverage,   

    # ARMS   
    shoulder_coverage,      
    armpit_coverage,               
    upper_arm_coverage,                 
    elbow_coverage,                          
    forearm_coverage,     
    hand_coverage,
    mobility_modifier, bludgeoning_res, piercing_res, slashing_res, armor_strength_check, armor_durability,armor_equip_type,

accessories,
    accessories_equip_type,
consumables,
    buffs, debuffs, duration, cooldown, nutritional_value,
ammo,
    ammo_bludgeoning_dmg, ammo_piercing_dmg, ammo_slashing_dmg, area_of_effect,
materials,
    # necessary for crafting
special,
    # necessary for plot
currency,
misc):
    
    all_args = [name, weight, rarity, description, stack_size, unique_traits, components, value, level,
wield,
    bludgeoning_dmg, piercing_dmg, slashing_dmg, attack_speed, attack_range, energy_cost, block, wield_strength_check, wield_durability, one_or_two_handed,
armor,
    cranium_coverage,                                            
    eye_coverage,                         
    nose_coverage,                     
    jaw_coverage,                   
    neck_coverage,                     
    throat_coverage,                     

    # UPPER TORSO               
    pec_coverage,                                 
    rib_coverage,                   
    sternum_coverage,                     
    heart_coverage,                                       
    lung_coverage,                  
    diaphragm_coverage,                  
    thoracic_viscera_coverage,     
    liver_coverage,                     

    # LOWER TORSO
    abdomen_coverage, 
    abdominal_viscera_coverage,
    spleen_coverage,
    groin_coverage,        

    # BACK
    spine_coverage,                        
    upper_back_coverage, 
    lower_back_coverage,
    kidney_coverage,                 

    # LEGS     
    glute_coverage,          
    quad_coverage,      
    hamstring_coverage,             
    knee_coverage,                               
    shin_coverage,                   
    calf_coverage,         
    foot_coverage,   

    # ARMS   
    shoulder_coverage,      
    armpit_coverage,               
    upper_arm_coverage,                 
    elbow_coverage,                          
    forearm_coverage,     
    hand_coverage,

    mobility_modifier, bludgeoning_res, piercing_res, slashing_res, armor_strength_check, armor_durability,armor_equip_type,
accessories,
    accessories_equip_type,
consumables,
    buffs, debuffs, duration, cooldown, nutritional_value,
ammo,
    ammo_bludgeoning_dmg, ammo_piercing_dmg, ammo_slashing_dmg, area_of_effect,
materials,
    # necessary for crafting
special,
    # necessary for plot
currency,
misc]
    args_and_attributes = list(zip(expected_column_order,all_args))


    existing_items = list(zip(ITEM_DATA['name'],ITEM_DATA['rarity'],ITEM_DATA['components'],ITEM_DATA['unique_traits']))

    if (name.strip(), rarity.strip(), components.strip(), unique_traits.strip()) not in [(n.strip(),r.strip(),c.strip(),u.strip()) for n,r,c,u in existing_items]:
        [[ITEM_DATA[f'{attribute[0]}'].append(attribute[1])] for attribute in args_and_attributes]
        save_item_to_db()
        print(f"{name} successfully added")
    else:
        print(f"{name} already exists")

def delete_item(name,rarity,components,unique_traits):
    ITEM_CURSOR.execute("DELETE FROM items WHERE name = ? AND rarity = ? AND components = ? AND unique_traits = ?",
                        (name,rarity,components,unique_traits))
    ITEM_CONN.commit()
    print(f"Deleted item: {name} ({rarity} made from {components}) | Unique = {unique_traits}")

def edit_item(name:str, rarity:str, components:str, unique_traits:str, updates:dict):
    set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values()) + [name,rarity,components,unique_traits]
    sql = f"UPDATE items SET {set_clause} WHERE name = ? AND rarity = ? AND components = ? AND unique_traits = ?",
    ITEM_CURSOR.execute(sql,values)
    ITEM_CONN.commit()

new_item(name='sharp_stick', weight=1, rarity='common', description='it is a sharp stick', stack_size=1, unique_traits='normal', components='stick', value=1,level=1,
wield=1,
    bludgeoning_dmg=1, piercing_dmg=1, slashing_dmg=1, attack_speed=1, attack_range=1, energy_cost=1, block=1, wield_strength_check=1, wield_durability=1, one_or_two_handed=1,
armor=None,

    cranium_coverage=None,                                            
    eye_coverage=None,                         
    nose_coverage=None,                     
    jaw_coverage=None,                   
    neck_coverage=None,                     
    throat_coverage=None,                     

    # UPPER TORSO               
    pec_coverage=None,                                 
    rib_coverage=None,                   
    sternum_coverage=None,                     
    heart_coverage=None,                                       
    lung_coverage=None,                  
    diaphragm_coverage=None,                  
    thoracic_viscera_coverage=None,     
    liver_coverage=None,                     

    # LOWER TORSO
    abdomen_coverage=None, 
    abdominal_viscera_coverage=None,
    spleen_coverage=None,
    groin_coverage=None,        

    # BACK
    spine_coverage=None,                        
    upper_back_coverage=None, 
    lower_back_coverage=None,
    kidney_coverage=None,                 

    # LEGS     
    glute_coverage=None,          
    quad_coverage=None,      
    hamstring_coverage=None,             
    knee_coverage=None,                               
    shin_coverage=None,                   
    calf_coverage=None,         
    foot_coverage=None,   

    # ARMS   
    shoulder_coverage=None,      
    armpit_coverage=None,               
    upper_arm_coverage=None,                 
    elbow_coverage=None,                          
    forearm_coverage=None,     
    hand_coverage=None,
    
    mobility_modifier=None, bludgeoning_res=None, piercing_res=None, slashing_res=None, armor_strength_check=None, armor_durability=None, armor_equip_type=None,
    accessories=False,
        accessories_equip_type=False,
    consumables=False,
        buffs=None, debuffs=None, duration=None, cooldown=None, nutritional_value=None,
    ammo=False,
        ammo_bludgeoning_dmg=None, ammo_piercing_dmg=None, ammo_slashing_dmg=None, area_of_effect=None,
    materials=False,
        # necessary for crafting
    special=False,
        # necessary for plot
    currency=False,
    misc=False
)


primary_attributes = ['name','weight','rarity','description','stack_size','unique_traits','components','value','level',          
                      'type',
]

all_types = ['wield','armor','accessories','consumables','ammo','materials','special','currency','misc',]


class ItemCreatorGUI:
    def __init__(self,root):
        self.root = root
        root.title("Item Creator")
        entry_var = tk.StringVar()

        canvas = tk.Canvas(root)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side='right', fill='y')

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))


        
        self.vars = {}
        self.entries = {}

        def to_lower(*args):
            current = entry_var.get()
            lower = current.lower()
            if current != lower:
                entry_var.set(lower)
        entry_var.trace_add('write', to_lower)

        for i,field in enumerate(primary_attributes):
            label = tk.Label(self.scrollable_frame, text=field.capitalize())
            label.grid(row=i, column=0, sticky='e', padx=5, pady=2)

            var = tk.StringVar()
            self.vars[field] = var
            entry = ttk.Entry(self.scrollable_frame, textvariable=var)
            self.entries[field] = entry

            name_entry = ttk.Entry(self.scrollable_frame,textvariable=tk.StringVar())
            weight_entry = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
            rarity_entry = ttk.Combobox(self.scrollable_frame,values=rarity_scale_list, state='readonly')
            description_entry = ttk.Entry(self.scrollable_frame,textvariable=tk.StringVar())
            stack_size_entry = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
            unique_traits_entry = ttk.Entry(self.scrollable_frame,textvariable=tk.StringVar())
            components_entry = ttk.Entry(self.scrollable_frame,textvariable=tk.StringVar())
            value_entry = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
            level_entry = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)

            type_entry = ttk.Combobox(self.scrollable_frame,values=all_types,
                                                    state='readonly')
            type_entry.bind("<<ComboboxSelected>>", self.expand_stats)

            if field == "name":
                name_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['name'] = name_entry
            elif field == 'weight':
                weight_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['weight'] = weight_entry
            elif field == 'rarity':
                rarity_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['rarity'] = rarity_entry
            elif field == 'description':
                description_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['description'] = description_entry
            elif field == 'stack_size':
                stack_size_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['stack_size'] = stack_size_entry
            elif field == 'unique_traits':
                unique_traits_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['unique_traits'] = unique_traits_entry
            elif field == 'components':
                components_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['components'] = components_entry
            elif field == 'value':
                value_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['value'] = value_entry
            elif field == 'type':
                type_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['type'] = type_entry
            elif field == 'level':
                level_entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries['level'] = level_entry

        submit_btn = tk.Button(self.scrollable_frame, text='Save Item', command=self.save_item)
        submit_btn.grid(row=len(primary_attributes), column=0, columnspan=2, pady=2)

    def expand_stats(self, event=None):
        def delete_extra_rows():
            children = self.scrollable_frame.winfo_children()
            # max_row = max(int(widget.grid_info().get('row', -1)) for widget in children)

            for widget in children:
                info = widget.grid_info()
                row = int(info.get('row', -1))
                if row > 10:
                    widget.grid_forget()
        delete_extra_rows()
        selected_type = self.entries['type'].get()

        if selected_type == 'wield':
            delete_extra_rows()
            for type in all_types:
                if type != 'wield':
                    self.entries[type] = tk.IntVar(value=0)
            weapon_fields = ['bludgeoning_dmg','piercing_dmg','slashing_dmg','attack_speed','attack_range','energy_cost',
                            'block','wield_strength_check','wield_durability','one_or_two_handed']
            for i,label_text in enumerate(weapon_fields):
                ttk.Label(self.scrollable_frame, text=label_text.title()).grid(row=1+len(primary_attributes)+i, column=0)
                if label_text != 'one_or_two_handed':
                    spin = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
                    spin.grid(row=1+len(primary_attributes)+i, column=1)
                    self.entries[label_text] = spin
                elif label_text == 'one_or_two_handed':
                    combo = ttk.Combobox(self.scrollable_frame,values=one_or_two_handed_list)
                    combo.grid(row=1+len(primary_attributes)+i, column=1)
                    self.entries[label_text] = combo

            self.entries['wield'] = tk.IntVar(value=1)
                
        elif selected_type == 'armor':
            delete_extra_rows()
            for type in all_types:
                if type != 'armor':
                    self.entries[type] = tk.IntVar(value=0)
            armor_fields = [
        'cranium_coverage',                                            
        'eye_coverage',                         
        'nose_coverage',                     
        'jaw_coverage',                   
        'neck_coverage',                     
        'throat_coverage',                     

        # UPPER TORSO               
        'pec_coverage',                                 
        'rib_coverage',                   
        'sternum_coverage',                     
        'heart_coverage',                                       
        'lung_coverage',                  
        'diaphragm_coverage',                  
        'thoracic_viscera_coverage',     
        'liver_coverage',                     

        # LOWER TORSO
        'abdomen_coverage', 
        'abdominal_viscera_coverage',
        'spleen_coverage',
        'groin_coverage',        

        # BACK
        'spine_coverage',                        
        'upper_back_coverage', 
        'lower_back_coverage',
        'kidney_coverage',                 

        # LEGS     
        'glute_coverage',          
        'quad_coverage',      
        'hamstring_coverage',             
        'knee_coverage',                               
        'shin_coverage',                   
        'calf_coverage',         
        'foot_coverage',   

        # ARMS   
        'shoulder_coverage',      
        'armpit_coverage',               
        'upper_arm_coverage',                 
        'elbow_coverage',                          
        'forearm_coverage',     
        'hand_coverage',

        'mobility_modifier','bludgeoning_res','piercing_res','slashing_res','armor_strength_check','armor_durability','armor_equip_type']
            for i,label_text in enumerate(armor_fields):
                ttk.Label(self.scrollable_frame, text=label_text.title()).grid(row=1+len(primary_attributes)+i, column=0)
                if label_text != 'armor_equip_type':
                    spin = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
                    spin.grid(row=1+len(primary_attributes)+i, column=1)
                    self.entries[label_text] = spin
                if label_text == 'armor_equip_type':
                    combo = ttk.Combobox(self.scrollable_frame,values=armor_equip_type_list)
                    combo.grid(row=1+len(primary_attributes)+i, column=1)
                    self.entries[label_text] = combo
            self.entries['armor'] = tk.IntVar(value=1)
        
        elif selected_type == 'consumables':
            delete_extra_rows()
            for type in all_types:
                if type != 'consumables':
                    self.entries[type] = tk.IntVar(value=0)
            weapon_fields = ['buffs','debuffs','duration','cooldown','nutritional_value',]
            for i,label_text in enumerate(weapon_fields):
                ttk.Label(self.scrollable_frame, text=label_text.title()).grid(row=1+len(primary_attributes)+i, column=0)
                spin = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
                spin.grid(row=1+len(primary_attributes)+i, column=1)
                self.entries[label_text] = spin
            self.entries['consumable'] = tk.IntVar(value=1)
   
        elif selected_type == 'ammo':
            delete_extra_rows()
            for type in all_types:
                if type != 'ammo':
                    self.entries[type] = tk.IntVar(value=0)
            weapon_fields = ['ammo_bludgeoning_dmg','ammo_piercing_dmg','ammo_slashing_dmg','area_of_effect',]
            for i,label_text in enumerate(weapon_fields):
                ttk.Label(self.scrollable_frame, text=label_text.title()).grid(row=1+len(primary_attributes)+i, column=0)
                spin = ttk.Spinbox(self.scrollable_frame,from_=1,to=1000)
                spin.grid(row=1+len(primary_attributes)+i, column=1)
                self.entries[label_text] = spin
            self.entries['ammo'] = tk.IntVar(value=1)

        elif selected_type == 'accessories':
            delete_extra_rows()
            for type in all_types:
                if type != 'accessories':
                    self.entries[type] = tk.IntVar(value=0)
            weapon_fields = ['accessories_equip_type',]
            for i,label_text in enumerate(weapon_fields):
                ttk.Label(self.scrollable_frame, text=label_text.title()).grid(row=1+len(primary_attributes)+i, column=0)
                combo = ttk.Combobox(self.scrollable_frame,values=accessories_equip_type_list)
                combo.grid(row=1+len(primary_attributes)+i, column=1)
                self.entries[label_text] = combo
            self.entries['accessories'] = tk.IntVar(value=1)

        elif selected_type == 'materials':
            delete_extra_rows()
            for type in all_types:
                if type != 'materials':
                    self.entries[type] = tk.IntVar(value=0)
            self.entries['materials'] = tk.IntVar(value=1)

        elif selected_type == 'special':
            delete_extra_rows()
            for type in all_types:
                if type != 'special':
                    self.entries[type] = tk.IntVar(value=0)
            self.entries['special'] = tk.IntVar(value=1)

        elif selected_type == 'currency':
            delete_extra_rows()
            for type in all_types:
                if type != 'currency':
                    self.entries[type] = tk.IntVar(value=0)
            self.entries['currency'] = tk.IntVar(value=1)

        elif selected_type == 'misc':
            delete_extra_rows()
            for type in all_types:
                if type != 'misc':
                    self.entries[type] = tk.IntVar(value=0)
            self.entries['misc'] = tk.IntVar(value=1)

        else:
            delete_extra_rows()

        
    def save_item(self):
        data = {}

        for field in expected_column_order:
            try:
                val = self.entries[field].get()
                data[field] = val
                if data[field] == None:
                    messagebox.showerror("Error", f"{field} is required to make an item.")
                    return
            except:
                data[field] = None
        
        try:
            placeholders = ', '.join('?' * len(data))
            columns = ', '.join(data.keys())
            sql = f"INSERT INTO items ({columns}) VALUES ({placeholders})"
            ITEM_CURSOR.execute(sql,list(data.values()))
            ITEM_CONN.commit()
            messagebox.showinfo("Save Successful", f'{data["name"]} was successfully added.')
        except Exception as e:
            messagebox.showerror("Database Error",str(e))


root = tk.Tk()
app = ItemCreatorGUI(root)
root.mainloop()
                

















