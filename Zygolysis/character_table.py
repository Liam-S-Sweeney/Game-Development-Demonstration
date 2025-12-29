from lore import *
from stats import *
from sqlite3 import *
from pprint import *
import pandas as pd
import os
# os.remove('characters.db')

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

    'randomize_stats',
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHARACTERS_DB_PATH = os.path.join(BASE_DIR,'characters.db')
CHARACTERS_CONN = connect(CHARACTERS_DB_PATH)
CHARACTERS_CURSOR = CHARACTERS_CONN.cursor()

def load_character_data():
    global CHARACTER_DATA
    try:
        df = pd.read_sql('SELECT * FROM characters', CHARACTERS_CONN)
        CHARACTER_DATA = df.to_dict(orient='list')
    except Exception as e:
        print("Initializing empty database:", e)

        # Initialize structure
        CHARACTER_DATA = {column: [] for column in expected_column_order}

        # Create characters table with all expected columns
        column_defs = ', '.join([f'"{col}" TEXT' for col in expected_column_order])
        CHARACTERS_CURSOR.execute(f"CREATE TABLE IF NOT EXISTS characters ({column_defs})")
        CHARACTERS_CONN.commit()

load_character_data()

def save_character_to_db():
        df = pd.DataFrame({key: [CHARACTER_DATA[key][-1]] for key in CHARACTER_DATA})
        df.to_sql('characters', CHARACTERS_CONN, if_exists='append',index=False)


def inherit_primary_traits(character_data):
    inheritance_map = {
        # 'strength': [1],
        'brawn': 'strength',
            'might': 'brawn',
            'skeletal_muscle_mass': 'brawn', 
            'explosiveness': 'brawn', 
            'carrying_capacity': 'brawn',
            'block_chance': 'brawn',
        'stamina': 'strength',
            'muscular_endurance': 'stamina',
            'grip': 'stamina',
            'gross_motor_control': 'stamina',

    # 'agility': [1], 
        'dodge': 'agility',
            'reflexes': 'dodge',
            'hit_avoidance_chance': 'dodge', 
            'stealth': 'dodge',
        'mobility': 'agility',
            'balance': 'mobility', 
            'speed': 'mobility', 
            'flexibility': 'mobility', 
            'acrobatics': 'mobility',
        'precision': 'agility',
            'fine_motor_control': 'precision',
            'aim': 'precision',
            'targeting': 'precision',
            'parry': 'precision',

    # 'vitality': [1],
        'resilience': 'vitality',
            'pain_tolerance': 'resilience',
            'durability': 'resilience',
            'dmg_absorbtion': 'resilience',
        'vigor': 'vitality',
            'recovery_rate': 'vigor',
            'intervention_receptivity': 'vigor',
            'resistance': 'vigor',
            
    # 'cognition': [1],
        'memory': 'cognition', 
            'information_retention': 'memory',
        'logic': 'cognition',
            'reasoning': 'logic',
        'fluency': 'cognition',
            'processing_speed': 'fluency',

    # 'sagacity': [1],
        'perception': 'sagacity',
            'situational_awareness': 'perception',
            'sensory_sensitivity': 'perception',
        'intuition': 'sagacity',
            'instincts': 'intuition',
            'o_interpersonal_insigt': 'intuition',
            's_intrapersonal_insight': 'intuition',
        'composure': 'sagacity',
            'stress_modulation': 'composure',
            'emotional_stability': 'composure',

    # 'influence': [1], 
        'charm': 'influence', 
        'intimidation': 'influence',
        'seduction': 'influence',
        'deception': 'influence',
    }

    # Only update the last entry (most recent character)
    for sub, main in inheritance_map.items():
        if character_data[sub][-1] in [1, '', ' ', 'NA']:
            character_data[sub][-1] = character_data[main][-1]


def new_character(name, sex, faction, gods, mortal_type, mortal_subtype, level,
                strength, brawn, might, skeletal_muscle_mass, explosiveness, carrying_capacity, block_chance,
                stamina, muscular_endurance, grip, gross_motor_control,
                agility, dodge, reflexes, hit_avoidance_chance, stealth,
                mobility, balance, speed, flexibility, acrobatics,
                precision, fine_motor_control, aim, targeting, parry,
                vitality, resilience, pain_tolerance, durability, dmg_absorbtion,
                vigor, recovery_rate, intervention_receptivity, resistance,
                cognition, memory, information_retention, logic, reasoning,
                fluency, processing_speed,
                sagacity, perception, situational_awareness, sensory_sensitivity,
                intuition, instincts, o_interpersonal_insigt, s_intrapersonal_insight,
                composure, stress_modulation, emotional_stability,
                influence, Charm, Intimidation, Seduction, Deception,
                openness, conscientiousness, extraversion, agreeableness, neuroticism,
                inventory, 
                helmet, visor, gorget, coif, arming_cap, 
                gambeson, haubergeon, breastplate, backplate, plackart, 
                r_pauldron, l_pauldron, r_spaulder, l_spaulder, upper_gousset, r_vambrace, l_vambrace, r_gauntlet, l_gauntlet, 
                chausses, culet, mail_skirt, codpiece, lower_gousset, r_tasset, l_tasset, r_poleyn, l_poleyn, r_greave, l_greave, r_sabaton, l_sabaton,

                # Hand Slots
                hand_slot_1,hand_slot_2,hand_slot_3,hand_slot_4,
                # Accessories
                hat,upper_face,lower_face,scarf,jacket,shirt,bottoms,belt,socks,undergarment,shoes,
                ring,necklace,bracelet,eye_piece,mask,implant,gadget,
                # Status Effects
                status_effects,
                # Stress
                stress_level,
                # Relationships
                individual_relationships,faction_relationships,
                randomize_stats):

    existing_pairs = list(zip(CHARACTER_DATA['name'], CHARACTER_DATA['faction']))

    if (name.strip(), faction.strip()) not in [(n.strip(), f.strip()) for n, f in existing_pairs]:
        CHARACTER_DATA['name'].append(name)
        CHARACTER_DATA['sex'].append(sex)
        CHARACTER_DATA['faction'].append(faction)
        CHARACTER_DATA['gods'].append(gods)
        CHARACTER_DATA['mortal_type'].append(mortal_type)
        CHARACTER_DATA['mortal_subtype'].append(mortal_subtype)
        CHARACTER_DATA['level'].append(level)

        CHARACTER_DATA['strength'].append(strength)
        CHARACTER_DATA['brawn'].append(brawn)
        CHARACTER_DATA['might'].append(might)
        CHARACTER_DATA['skeletal_muscle_mass'].append(skeletal_muscle_mass)
        CHARACTER_DATA['explosiveness'].append(explosiveness)
        CHARACTER_DATA['carrying_capacity'].append(carrying_capacity)
        CHARACTER_DATA['block_chance'].append(block_chance)
        CHARACTER_DATA['stamina'].append(stamina)
        CHARACTER_DATA['muscular_endurance'].append(muscular_endurance)
        CHARACTER_DATA['grip'].append(grip)
        CHARACTER_DATA['gross_motor_control'].append(gross_motor_control)

        CHARACTER_DATA['agility'].append(agility)
        CHARACTER_DATA['dodge'].append(dodge)
        CHARACTER_DATA['reflexes'].append(reflexes)
        CHARACTER_DATA['hit_avoidance_chance'].append(hit_avoidance_chance)
        CHARACTER_DATA['stealth'].append(stealth)
        CHARACTER_DATA['mobility'].append(mobility)
        CHARACTER_DATA['balance'].append(balance)
        CHARACTER_DATA['speed'].append(speed)
        CHARACTER_DATA['flexibility'].append(flexibility)
        CHARACTER_DATA['acrobatics'].append(acrobatics)
        CHARACTER_DATA['precision'].append(precision)
        CHARACTER_DATA['fine_motor_control'].append(fine_motor_control)
        CHARACTER_DATA['aim'].append(aim)
        CHARACTER_DATA['targeting'].append(targeting)
        CHARACTER_DATA['parry'].append(parry)

        CHARACTER_DATA['vitality'].append(vitality)
        CHARACTER_DATA['resilience'].append(resilience)
        CHARACTER_DATA['pain_tolerance'].append(pain_tolerance)
        CHARACTER_DATA['durability'].append(durability)
        CHARACTER_DATA['dmg_absorbtion'].append(dmg_absorbtion)
        CHARACTER_DATA['vigor'].append(vigor)
        CHARACTER_DATA['recovery_rate'].append(recovery_rate)
        CHARACTER_DATA['intervention_receptivity'].append(intervention_receptivity)
        CHARACTER_DATA['resistance'].append(resistance)

        CHARACTER_DATA['cognition'].append(cognition)
        CHARACTER_DATA['memory'].append(memory)
        CHARACTER_DATA['information_retention'].append(information_retention)
        CHARACTER_DATA['logic'].append(logic)
        CHARACTER_DATA['reasoning'].append(reasoning)
        CHARACTER_DATA['fluency'].append(fluency)
        CHARACTER_DATA['processing_speed'].append(processing_speed)

        CHARACTER_DATA['sagacity'].append(sagacity)
        CHARACTER_DATA['perception'].append(perception)
        CHARACTER_DATA['situational_awareness'].append(situational_awareness)
        CHARACTER_DATA['sensory_sensitivity'].append(sensory_sensitivity)
        CHARACTER_DATA['intuition'].append(intuition)
        CHARACTER_DATA['instincts'].append(instincts)
        CHARACTER_DATA['o_interpersonal_insigt'].append(o_interpersonal_insigt)
        CHARACTER_DATA['s_intrapersonal_insight'].append(s_intrapersonal_insight)
        CHARACTER_DATA['composure'].append(composure)
        CHARACTER_DATA['stress_modulation'].append(stress_modulation)
        CHARACTER_DATA['emotional_stability'].append(emotional_stability)

        CHARACTER_DATA['influence'].append(influence)
        CHARACTER_DATA['charm'].append(Charm)
        CHARACTER_DATA['intimidation'].append(Intimidation)
        CHARACTER_DATA['seduction'].append(Seduction)
        CHARACTER_DATA['deception'].append(Deception)

        CHARACTER_DATA['openness'].append(openness)
        CHARACTER_DATA['conscientiousness'].append(conscientiousness)
        CHARACTER_DATA['extraversion'].append(extraversion)
        CHARACTER_DATA['agreeableness'].append(agreeableness)
        CHARACTER_DATA['neuroticism'].append(neuroticism)

        CHARACTER_DATA['inventory'].append(inventory)
        CHARACTER_DATA['helmet'].append(helmet)
        CHARACTER_DATA['visor'].append(visor)
        CHARACTER_DATA['gorget'].append(gorget)
        CHARACTER_DATA['coif'].append(coif)
        CHARACTER_DATA['arming_cap'].append(arming_cap)
        CHARACTER_DATA['gambeson'].append(gambeson)
        CHARACTER_DATA['haubergeon'].append(haubergeon)
        CHARACTER_DATA['breastplate'].append(breastplate)
        CHARACTER_DATA['backplate'].append(backplate)
        CHARACTER_DATA['plackart'].append(plackart)
        CHARACTER_DATA['r_pauldron'].append(r_pauldron)
        CHARACTER_DATA['l_pauldron'].append(l_pauldron)
        CHARACTER_DATA['r_spaulder'].append(r_spaulder)
        CHARACTER_DATA['l_spaulder'].append(l_spaulder)
        CHARACTER_DATA['upper_gousset'].append(upper_gousset)
        CHARACTER_DATA['r_vambrace'].append(r_vambrace)
        CHARACTER_DATA['l_vambrace'].append(l_vambrace)
        CHARACTER_DATA['r_gauntlet'].append(r_gauntlet)
        CHARACTER_DATA['l_gauntlet'].append(l_gauntlet)
        CHARACTER_DATA['chausses'].append(chausses) 
        CHARACTER_DATA['culet'].append(culet)
        CHARACTER_DATA['mail_skirt'].append(mail_skirt)
        CHARACTER_DATA['codpiece'].append(codpiece)
        CHARACTER_DATA['lower_gousset'].append(lower_gousset)
        CHARACTER_DATA['r_tasset'].append(r_tasset)
        CHARACTER_DATA['l_tasset'].append(l_tasset)
        CHARACTER_DATA['r_poleyn'].append(r_poleyn)
        CHARACTER_DATA['l_poleyn'].append(l_poleyn)
        CHARACTER_DATA['r_greave'].append(r_greave)
        CHARACTER_DATA['l_greave'].append(l_greave)
        CHARACTER_DATA['r_sabaton'].append(r_sabaton)
        CHARACTER_DATA['l_sabaton'].append(l_sabaton)
        CHARACTER_DATA['hand_slot_1'].append(hand_slot_1)
        CHARACTER_DATA['hand_slot_2'].append(hand_slot_2)
        CHARACTER_DATA['hand_slot_3'].append(hand_slot_3)
        CHARACTER_DATA['hand_slot_4'].append(hand_slot_4)
        CHARACTER_DATA['hat'].append(hat)
        CHARACTER_DATA['upper_face'].append(upper_face)
        CHARACTER_DATA['lower_face'].append(lower_face)
        CHARACTER_DATA['scarf'].append(scarf)
        CHARACTER_DATA['jacket'].append(jacket)
        CHARACTER_DATA['shirt'].append(shirt)
        CHARACTER_DATA['bottoms'].append(bottoms)
        CHARACTER_DATA['belt'].append(belt)
        CHARACTER_DATA['socks'].append(socks)
        CHARACTER_DATA['undergarment'].append(undergarment)
        CHARACTER_DATA['shoes'].append(shoes)
        CHARACTER_DATA['ring'].append(ring)
        CHARACTER_DATA['necklace'].append(necklace)
        CHARACTER_DATA['bracelet'].append(bracelet)
        CHARACTER_DATA['eye_piece'].append(eye_piece)
        CHARACTER_DATA['mask'].append(mask)
        CHARACTER_DATA['implant'].append(implant)
        CHARACTER_DATA['gadget'].append(gadget)

        CHARACTER_DATA['status_effects'].append(status_effects)
        CHARACTER_DATA['stress_level'].append(stress_level)

        CHARACTER_DATA['individual_relationships'].append(individual_relationships)
        CHARACTER_DATA['faction_relationships'].append(faction_relationships)


        CHARACTER_DATA['randomize_stats'].append(randomize_stats)

        inherit_primary_traits(CHARACTER_DATA)
        save_character_to_db()
        print(f"{name} successfully added")
    else:
        print(f"{name} already exists")
        


def delete_character(name,faction):
    CHARACTERS_CURSOR.execute("DELETE FROM characters WHERE name = ? AND faction = ?",
                   (name, faction))
    CHARACTERS_CONN.commit()
    print(f"Deleted character: {name} from {faction}")


def edit_character(name:str, faction:str, updates:dict):
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [name,faction]

        sql = f"UPDATE characters SET {set_clause} WHERE name = ? AND faction = ?"
        CHARACTERS_CURSOR.execute(sql,values)
        CHARACTERS_CONN.commit()

new_character(name='dummy', sex='dummy', faction='dummy', gods='dummy', mortal_type='dummy', mortal_subtype='dummy', level=1,
                strength=1, 
                    brawn=1,
                        might=1, 
                        skeletal_muscle_mass=1, 
                        explosiveness=1, 
                        carrying_capacity=1,
                        block_chance=1,
                    stamina=1, 
                        muscular_endurance=1, 
                        grip=1,
                        gross_motor_control=1,
                agility=1, 
                    dodge=1, 
                        reflexes=1, 
                        hit_avoidance_chance=1, 
                        stealth=1,
                    mobility=1, 
                        balance=1, 
                        speed=1, 
                        flexibility=1, 
                        acrobatics=1,
                    precision=1,
                        fine_motor_control=1,
                        aim=1,
                        targeting=1,
                        parry=1,
                vitality=1, 
                    resilience=1, 
                        pain_tolerance=1,
                        durability=1,
                        dmg_absorbtion=1,
                    vigor=1,
                        recovery_rate=1,
                        intervention_receptivity=1,
                        resistance=1,
                cognition=1, 
                    memory=1, 
                        information_retention=1,
                    logic=1, 
                        reasoning=1,
                    fluency=1,
                        processing_speed=1,
                sagacity=1, 
                    perception=1, 
                        situational_awareness=1,
                        sensory_sensitivity=1,
                    intuition=1, 
                        instincts=1,
                        o_interpersonal_insigt=1,
                        s_intrapersonal_insight=1,
                    composure=1,
                        stress_modulation=1,
                        emotional_stability=1,
                influence=1, 
                    Charm=1, 
                    Intimidation=1,
                    Seduction=1, 
                    Deception=1,
                openness=1,
                conscientiousness=1,
                extraversion=1,
                agreeableness=1,
                neuroticism=1,

                inventory=None, 
                #armor
                helmet=None, visor=None, gorget=None, coif=None, arming_cap=None, 
                gambeson=None, haubergeon=None, breastplate=None, backplate=None, plackart=None, 
                r_pauldron=None, l_pauldron=None, r_spaulder=None, l_spaulder=None, upper_gousset=None, r_vambrace=None, l_vambrace=None, r_gauntlet=None, l_gauntlet=None, 
                chausses=None, culet=None, mail_skirt=None, codpiece=None, lower_gousset=None, r_tasset=None, l_tasset=None, r_poleyn=None, l_poleyn=None, r_greave=None, l_greave=None, r_sabaton=None, l_sabaton=None,
                # Hand Slots
                hand_slot_1=None,hand_slot_2=None,hand_slot_3=None,hand_slot_4=None,
                # Accessories
                hat=None,upper_face=None,lower_face=None,scarf=None,jacket=None,shirt=None,bottoms=None,belt=None,socks=None,undergarment=None,shoes=None,
                ring=None,necklace=None,bracelet=None,eye_piece=None,mask=None,implant=None,gadget=None,
                # Status Effects
                status_effects=None,
                # Stress
                stress_level=None,
                # Relationships
                individual_relationships=None,faction_relationships=None,

                randomize_stats=0
)

df = pd.read_sql("SELECT * FROM characters", CHARACTERS_CONN)

print(df)
