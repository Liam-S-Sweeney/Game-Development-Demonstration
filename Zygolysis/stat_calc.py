import pandas as pd

def raw_to_z(raw,average,sd):
    z = (raw-average)/sd
    return(round(z))
def z_to_raw(z,average,sd):
    raw = z * sd + average
    return(round(raw))

def z_to_ws(z):
    ws = 3*z+10
    return(round(ws))
def ws_to_z(ws):
    z=(ws-10)/3
    return(round(z))

def raw_to_ws(raw,average,sd):
    z = (raw-average)/sd
    ws = 3*z+10
    return(round(ws))
def ws_to_raw(ws,average,sd):
    z = (ws-10)/3
    raw = z * sd + average
    return(round(raw))

# def nutritional_needs(weight):
#         return(1kg * 15kcal / 2g protein)

# ds = data_setup
def ds_main_categories(dictionary):
        df_dict = {}

        for gender, (avg,sd) in dictionary.items():
            key = gender
            df_dict[key] = [ws_to_raw(ss,avg,sd) for ss in range(41)]
        df = pd.DataFrame(df_dict)
        return df
def ds_sub_categories(dictionary):
        df_dict = {}

        for gender, activities in dictionary.items():
             for activity, (avg,sd) in activities.items():
                  key = f"{gender}_{activity}"
                  df_dict[key] = [ws_to_raw(ss,avg,sd) for ss in range(41)]
        df = pd.DataFrame(df_dict)
        return df

#####

# Strength
class Brawn: 
    def __init__(self):
        self.might_df = self.might_data # KiloNewtons of unarmed attack
        self.skeletal_muscle_mass_df = self.skeletal_muscle_mass_data # Weight(kg)
        self.explosiveness_df = self.explosiveness_data # m/s, m 
        self.carrying_capacity_df = self.carrying_capacity_data # kg
        self.block_chance_df = self.block_chance_data # % chance to block attack if dodge/parry fails

    might_standards = {
    'male': { # AVG : punches = 8 , kicks = 24
        'punch': (10, 5.67),                             # ~ 1000 N Avg, untrained = 800-1200N, amateur =2400-2600N (2500N), professional = 3000-4100N(3550N), world_reocrd = 5000-6000N (5500N)
        'kick': (30, 11.5),                              # ~12000 N max
    },
    'female': {
        'punch': (6, 2.92),                              # ~ 650 N Avg, max = 3000N
        'kick': (18, 6),                               # 
    }}
    might_data = ds_sub_categories(might_standards)


    skeletal_muscle_mass = {
        'male': (32.6,5.2),
        'female': (20.9,3.6)
    }
    skeletal_muscle_mass_data = ds_main_categories(skeletal_muscle_mass)

    explosiveness_standards = {
        'male':  {
            'sprint': (9.67, 0.39), #m/s
            'long_jump': (7.8, 0.8) #m
        },
        'female': {
            'sprint': (8.79, 0.46),
            'long_jump': (6.5, 0.7)
        }
    }
    explosiveness_data = ds_sub_categories(explosiveness_standards)

    carrying_capacity = {
        'male': (35, 5),
        'female': (25, 5),
    }
    carrying_capacity_data = ds_main_categories(carrying_capacity)

    block_chance = {
        'male': (45,8),
        'female': (45,8)
    }
    block_chance_data = ds_main_categories(block_chance)
#####
class Stamina:
    def __init__(self):
        self.muscular_endurance_df = self.muscular_endurance_data # time (s) in combat before fatigue
        self.grip_df = self.grip_data # kg of grip strength
        self.gross_motor_control_df = self.gross_motor_control_data # fitness reps (push, pull, legs, core)

    muscular_endurance = {
            'male': (20,10),
            'female': (20,10),
        }
    muscular_endurance_data = ds_main_categories(muscular_endurance)

    def fatigue_threshold(self, gender, ss, duration):
        if ss < 0 or ss > 35:
            print(f"{ss} out of range (0-34)")
            return
        threshold = self.muscular_endurance_df[gender][ss]
        # print(threshold)
        if duration >= threshold:
            print(f"Success — performance matches or exceeds ({threshold}), no change")
        else:
            print(f"Success — performance matches or exceeds SS, no change")
    
    grip = {
            'male': (46,9),
            'female': (28,5),
        }
    grip_data = ds_main_categories(grip)

    gross_motor_control = {
            'male': {
                'push': (115, 15),
                'pull': (110, 15),
                'legs': (105, 15),
                'core': (102, 15),
            },
            'female': {
                'push': (85, 15),
                'pull': (90, 15),
                'legs': (95, 15),
                'core': (98, 15),
            },
        }
    gross_motor_control_data = ds_sub_categories(gross_motor_control)

#############################################################################

# Agility

class Dodge:
    def __init__(self):
        self.reflexes_df = self.reflexes_data # rt
        self.hit_avoidance_chance_df = self.hit_avoidance_chance_data # % dodge/parry
        self.stealth_df = self.stealth_data # % chance to remain hidden
    
    reflexes = {
        'male': (103,15),
        'female': (97,15)
    }
    reflexes_data = ds_main_categories(reflexes)

    hit_avoidance_chance = {
        'male': (20,8),
        'female': (20,8)
    }
    hit_avoidance_chance_data = ds_main_categories(hit_avoidance_chance)

    stealth = {
         'male':{
             'total_visability': (1,2), # out in the open
             'high_visability': (20,10), # light cover
             'moderate_visability': (45,15), # medium cover
             'low_visability': (70,10), # strong cover
             'no_visability': (90,5), # perfect cover
         },
         'female':{
             'total_visability': (2,2), # out in the open
             'high_visability': (30,10), # light cover
             'moderate_visability': (60,15), # medium cover
             'low_visability': (80,10), # strong cover
             'no_visability': (95,5), # perfect cover
         },
    }
    stealth_data = ds_sub_categories(stealth)
#####
class Mobility:
    def __init__(self):
        self.balance_df = self.balance_data # standard score balance
        self.speed_df = self.speed_data # walking speed (m/s)
        self.flexibility_df = self.flexibility_data # standard score flexibility
        self.acrobatics_df = self.acrobatics_data # standard score acrobatics
    
    balance = {
         'male': {
              'static' : (100,15),
              'dynamic': (100,15),
              'reactive': (40,8), # % chance to not fall if shoved
         },
         'female': {
              'static' : (105,15),
              'dynamic': (103,15),
              'reactive': (30,8), # % chance to not fall if shoved
         }
    }
    balance_data = ds_sub_categories(balance)

    speed = {
        'male': (1.37,0.12),
        'female': (1.26,0.12)
    }
    speed_data = ds_main_categories(speed)

    flexibility = {
        'male': (90,15),
        'female': (110,15)
    }
    flexibility_data = ds_main_categories(flexibility)

    acrobatics = {
         'male': {
              'grace' : (90,15),
              'rotation': (100,15),
              'power': (110,15),
         },
         'female': {
              'grace' : (110,15),
              'rotation': (100,15),
              'power': (90,15),
         }
    }
    acrobatics_data = ds_sub_categories(acrobatics)
#####
class Precision:
    def __init__(self):
        self.fine_motor_control_df = self.fine_motor_control_data # standard score fmc
        self.aim_df = self.aim_data # refer below, standard score
        self.targeting_df = self.targeting_data # % ability to target individual limbs
        self.parry_df = self.parry_data # % chance to parry blows with an equiped weapon
# AIM IS MULTI-DIMENSIONAL
    # Agility (motor execution)
    # Perception (target acquisition)
    # Sagacity/Composure (performance under stress)
    # Logic/Fluency (timing and anticipation)

    fine_motor_control = {
        'male': {
            'dexterity_manipulation' : (95,15), 
            'tool_utilization': (100,15),
            'writing_drawing': (95,15),
        },
        'female': {
            'dexterity_manipulation' : (105,15),
            'tool_utilization': (105,15),
            'writing_drawing': (110,15),
        },
     }
    fine_motor_control_data = ds_sub_categories(fine_motor_control)

    aim = {
        'male': {
            'hand_eye_coord': (100,8), # Modified Ability to quickly aim at static targets (static H-E_C)
            'consistent_tracking': (75,8), # Modified Ability to aim at targets in consistent motion (continuous H-E_C)
            'inconsistent_tracking': (50,8), # Modified Ability to aim at targets in inconsistent motion (continuous H-E_C)
            'fire_rate': (5,1), # SHOTS PER MINUTE (60sec) - rate of fire for non-automatics 
            'draw_speed': (100,15), # rate of weapon draw
            'melee_accuracy': (70,10), # % of melee strikes that will hit
            'melee_targeting': (100,15), # ability to aim melee strikes at specific limbs
            'ranged_accuracy': (60,12), # % of ranged strikes that will hit
            'ranged_targeting': (100,15), # ability to aim range strikes at specific limbs
        },
        'female': {
            'hand_eye_coord': (100,8), # Ability to quickly aim at static targets (static H-E_C)
            'consistent_tracking': (70,8), # Modified Ability to aim at targets in consistent motion (continuous H-E_C)
            'inconsistent_tracking': (45,8), # Modified Ability to aim at targets in inconsistent motion (continuous H-E_C)
            'fire_rate': (5,1), # SHOTS PER MINUTE (60sec) - rate of fire for non-automatics            
            'draw_speed': (100,15), # rate of weapon draw
            'melee_accuracy': (70,10), # % of melee strikes that will hit
            'melee_targeting': (100,15), # ability to aim melee strikes at specific limbs
            'ranged_accuracy': (60,12), # % of ranged strikes that will hit
            'ranged_targeting': (100,15), # ability to aim range strikes at specific limbs
        },
     }
    aim_data = ds_sub_categories(aim)

    targeting = {
        'male': {
            # HEAD
            'cranium': (30, 10),         
            'eye_r': (12, 6),         
            'eye_l': (12, 6),          
            'nose': (22, 8),          
            'jaw': (25, 8),           
            'neck': (28, 8),         
            'throat': (20, 6),      

            # UPPER TORSO
            'pec_r': (50, 10),
            'pec_l': (50, 10),
            'rib_r': (65, 10),  
            'rib_l': (65, 10),        
            'sternum': (55, 8),     
            'heart': (15, 6), 
            'lung_r': (25, 6),
            'lung_l': (25, 6),
            'diaphragm': (30,8),
            'thoracic_viscera': (40, 8),
            'liver': (20,4),

            # LOWER TORSO
            'abdomen': (60, 9),      
            'abdominal_viscera': (30, 8),
            'spleen': (15,6),
            'groin': (20, 6),         

            # BACK
            'spine': (25, 6),         
            'upper_back': (65, 10), 
            'lower_back': (55, 8),   
            'kidney_r': (15, 6),
            'kidney_l': (15, 6),          

            # LEGS
            'glute_r': (40, 8),        
            'glute_l': (40, 8),       
            'quad_r': (50, 8),       
            'quad_l': (50, 8),       
            'hamstring_r': (45,8),
            'hamstring_l': (45,8),
            'knee_r': (38, 8),         
            'knee_l': (38, 8),         
            'shin_r': (30,8),
            'shin_l': (30,8),
            'calf_r': (30, 8),        
            'calf_l': (30, 8),        
            'foot_r': (15, 8),       
            'foot_l': (15, 8),    
            
            # ARMS
            'shoulder_r': (45, 8),    
            'shoulder_l': (45, 8),  
            'armpit_r': (12, 6),      
            'armpit_l': (12, 6),           
            'upper_arm_r': (40, 8),     
            'upper_arm_l': (40, 8),     
            'elbow_r': (25, 6),   
            'elbow_l': (25, 6),      
            'forearm_r': (30, 8),   
            'forearm_l': (30, 8),     
            'hand_r': (15, 6),
            'hand_l': (15, 6),

        },
        'female': {
            # HEAD
            'cranium': (30, 10),         
            'eye_r': (12, 6),         
            'eye_l': (12, 6),          
            'nose': (22, 8),          
            'jaw': (25, 8),           
            'neck': (28, 8),         
            'throat': (20, 6),      

            # UPPER TORSO
            'pec_r': (50, 10),
            'pec_l': (50, 10),
            'rib_r': (65, 10),  
            'rib_l': (65, 10),        
            'sternum': (55, 8),     
            'heart': (15, 6), 
            'lung_r': (25, 6),
            'lung_l': (25, 6),
            'diaphragm': (30,8),
            'thoracic_viscera': (40, 8),
            'liver': (20,4),

            # LOWER TORSO
            'abdomen': (60, 9),      
            'abdominal_viscera': (30, 8),
            'spleen': (15,6),
            'groin': (20, 6),         

            # BACK
            'spine': (25, 6),         
            'upper_back': (65, 10), 
            'lower_back': (55, 8),       
            'kidney_r': (15, 6),
            'kidney_l': (15, 6),            

            # LEGS
            'glute_r': (40, 8),        
            'glute_l': (40, 8),       
            'quad_r': (50, 8),       
            'quad_l': (50, 8),       
            'hamstring_r': (45,8),
            'hamstring_l': (45,8),
            'knee_r': (38, 8),         
            'knee_l': (38, 8),         
            'shin_r': (30,8),
            'shin_l': (30,8),
            'calf_r': (30, 8),        
            'calf_l': (30, 8),        
            'foot_r': (15, 8),       
            'foot_l': (15, 8),    
            
            # ARMS
            'shoulder_r': (45, 8),    
            'shoulder_l': (45, 8),  
            'armpit_r': (12, 6),      
            'armpit_l': (12, 6),           
            'upper_arm_r': (40, 8),     
            'upper_arm_l': (40, 8),     
            'elbow_r': (25, 6),   
            'elbow_l': (25, 6),      
            'forearm_r': (30, 8),   
            'forearm_l': (30, 8),     
            'hand_r': (15, 6),
            'hand_l': (15, 6),

        },
    }
    targeting_data = ds_sub_categories(targeting)

    parry = {
        'male': (10,4),
        'female': (10,4)
    }
    parry_data = ds_main_categories(parry)
#############################################################################

# Vitality

class Resilience:
    def __init__(self):
        self.pain_tolerance_df = self.pain_tolerance_data # % damage debuff resistance; Acute - immediate battle debuff, chronic - permanent debuff until healed fully
        self.durability_df = self.durability_data # unarmored limb hp
        self.dmg_absorbtion_df = self.dmg_absorbtion_data # numeric baseline dmg absorbtion by limb

    pain_tolerance = {
        'male': {
            'acute': (10.5,10),
            'chronic': (10.0,10),
        },
        'female': {
            'acute': (10.0,10),
            'chronic': (10.75,10),
        },
    }
    pain_tolerance_data = ds_sub_categories(pain_tolerance)
    
    durability = {
        'male': {# AVG : punches = 8 , kicks = 24
            # HEAD
            'cranium': (24, 8),                     # Hard       
            'eye_r': (6, 2),                         
            'eye_l': (6, 2),                         
            'nose': (16, 4.8),                       
            'jaw': (24, 8),                          
            'neck': (16, 4.8),                       
            'throat': (12, 2),                       

            # UPPER TORSO
            'pec_r': (24, 8),                       
            'pec_l': (24, 8),                       
            'rib_r': (16, 4.8),                     # Hard
            'rib_l': (16, 4.8),                     # Hard
            'sternum': (32, 8),                     # Hard
            'heart': (8, 2.4),                      
            'lung_r': (16, 4.8),                    
            'lung_l': (16, 4.8),                    
            'diaphragm': (16,4.8),                  
            'thoracic_viscera': (24, 8),            
            'liver': (8, 2.4),                      

            # LOWER TORSO
            'abdomen': (72, 24),      
            'abdominal_viscera': (16, 3),
            'spleen': (8, 4.8),
            'groin': (32, 10),         

            # BACK
            'spine': (24, 8),                       # Hard        
            'upper_back': (72, 24), 
            'lower_back': (48, 16), 
            'kidney_r': (8, 2.4),
            'kidney_l': (8, 2.4),                  

            # LEGS
            'glute_r': (120, 24),        
            'glute_l': (120, 24),       
            'quad_r': (120, 24),       
            'quad_l': (120, 24),       
            'hamstring_r': (96, 24),
            'hamstring_l': (96, 24),
            'knee_r': (72, 24),                    # Hard
            'knee_l': (72, 24),                    # Hard
            'shin_r': (36, 20),                    # Hard
            'shin_l': (36, 20),                    # Hard
            'calf_r': (72, 24),        
            'calf_l': (72, 24),        
            'foot_r': (48, 16),       
            'foot_l': (48, 16),    
            
            # ARMS
            'shoulder_r': (24, 8),    
            'shoulder_l': (24, 8),  
            'armpit_r': (20, 6),      
            'armpit_l': (20, 6),           
            'upper_arm_r': (24, 8),     
            'upper_arm_l': (24, 8),     
            'elbow_r': (16, 4.8),                   # Hard
            'elbow_l': (16, 4.8),                   # Hard
            'forearm_r': (24, 8),                   
            'forearm_l': (24, 8),     
            'hand_r': (16, 4.8),
            'hand_l': (16, 4.8),

        },

        'female': {# AVG : punches = 8 , kicks = 24
            # HEAD
            'cranium': (19.2, 6.4),                   # Hard       
            'eye_r': (6, 2),                         
            'eye_l': (6, 2),                         
            'nose': (12.8, 3.8),                       
            'jaw': (19.2, 6.4),                          
            'neck': (12.8, 3.8),                       
            'throat': (9.6, 1.6),                       

            # UPPER TORSO
            'pec_r': (19.2, 6.4),                       
            'pec_l': (19.2, 6.4),                       
            'rib_r': (12.8, 3.8),                     # Hard
            'rib_l': (12.8, 3.8),                     # Hard
            'sternum': (25.6, 6.4),                   # Hard
            'heart': (7.2, 2.2),                      
            'lung_r': (14.4, 7.2),                    
            'lung_l': (14.4, 7.2),                    
            'diaphragm': (12.8, 3.8),                  
            'thoracic_viscera': (19.2, 6.4),            
            'liver': (7.2, 2.2),                      

            # LOWER TORSO
            'abdomen': (72, 24),      
            'abdominal_viscera': (12.8, 3.8),
            'spleen': (7.2, 2.2),
            'groin': (32, 10),         

            # BACK
            'spine': (19.2, 6.4),                     # Hard        
            'upper_back': (57.6, 19.2), 
            'lower_back': (38.4, 12.8), 
            'kidney_r': (7.2, 2.2),
            'kidney_l': (7.2, 2.2),                  

            # LEGS
            'glute_r': (108, 21.6),        
            'glute_l': (108, 21.6),       
            'quad_r': (108, 21.6),       
            'quad_l': (108, 21.6),       
            'hamstring_r': (86.4, 21.6),
            'hamstring_l': (86.4, 21.6),
            'knee_r': (64.8, 21.6),                  # Hard
            'knee_l': (64.8, 21.6),                  # Hard
            'shin_r': (32.4, 16.2),                  # Hard
            'shin_l': (32.4, 16.2),                  # Hard
            'calf_r': (64.8, 21.6),        
            'calf_l': (64.8, 21.6),        
            'foot_r': (43.2, 14.4),       
            'foot_l': (43.2, 14.4),    
            
            # ARMS
            'shoulder_r': (19.2, 6.4),    
            'shoulder_l': (19.2, 6.4),  
            'armpit_r': (16, 4.8),      
            'armpit_l': (16, 4.8),           
            'upper_arm_r': (19.2, 6.4),     
            'upper_arm_l': (19.2, 6.4),     
            'elbow_r': (12.8, 3.8),                   # Hard
            'elbow_l': (12.8, 3.8),                   # Hard
            'forearm_r': (19.2, 6.4),                   
            'forearm_l': (19.2, 6.42),     
            'hand_r': (12.8, 3.8),
            'hand_l': (12.8, 3.8),

        },
    }
    durability_data = ds_sub_categories(durability)

    dmg_absorbtion = {
        'male': {# AVG : punches = 8 , kicks = 24
            # HEAD
            'cranium': (0, 1.2),                     # Hard       
            'eye_r': (0, 0),                         
            'eye_l': (0, 0.4),                         
            'nose': (0, 0.8),                       
            'jaw': (0, 0.8),                          
            'neck': (0, 0.4),                       
            'throat': (0, 0.2),                       

            # UPPER TORSO
            'pec_r': (0, 0.9),                       
            'pec_l': (0, 0.9),                       
            'rib_r': (0, 0.8),                      # Hard
            'rib_l': (0, 0.8),                      # Hard
            'sternum': (0, 1.2),                    # Hard
            'heart': (0, 0),                      
            'lung_r': (0, 0.2),                    
            'lung_l': (0, 0.2),                    
            'diaphragm': (0, 0.3),                  
            'thoracic_viscera': (0, 0.1),            
            'liver': (0, 0.3),                      

            # LOWER TORSO
            'abdomen': (0, 0.8),      
            'abdominal_viscera': (0, 0.1),
            'spleen': (0, 0.3),
            'groin': (0, 0.2),         

            # BACK
            'spine': (0, 1.2),                      # Hard        
            'upper_back': (0, 1.0), 
            'lower_back': (0, 1.0), 
            'kidney_r': (0, 0.3),
            'kidney_l': (0, 0.3),                  

            # LEGS
            'glute_r': (0, 1.0),        
            'glute_l': (0, 1.0),       
            'quad_r': (0, 1.0),       
            'quad_l': (0, 1.0),       
            'hamstring_r': (0, 0.8),
            'hamstring_l': (0, 0.8),
            'knee_r': (0, 0.6),                    # Hard
            'knee_l': (0, 0.6),                    # Hard
            'shin_r': (0, 0.6),                    # Hard
            'shin_l': (0, 0.6),                    # Hard
            'calf_r': (0, 0.8),        
            'calf_l': (0, 0.8),        
            'foot_r': (0, 0.4),       
            'foot_l': (0, 0.4),    
            
            # ARMS
            'shoulder_r': (0, 0.8),    
            'shoulder_l': (0, 0.8),  
            'armpit_r': (0, 0.4),      
            'armpit_l': (0, 0.4),           
            'upper_arm_r': (0, 0.8),     
            'upper_arm_l': (0, 0.8),     
            'elbow_r': (0, 0.3),                   # Hard
            'elbow_l': (0, 0.3),                   # Hard
            'forearm_r': (0, 0.6),                   
            'forearm_l': (0, 0.6),     
            'hand_r': (0, 0.3),
            'hand_l': (0, 0.3),

        },
        'female': {# AVG : punches = 8 , kicks = 24
            # HEAD
            'cranium': (0, 1.08),                     # Hard       
            'eye_r': (0, 0),                         
            'eye_l': (0, 0.36),                         
            'nose': (0, 0.72),                       
            'jaw': (0, 0.72),                          
            'neck': (0, 0.36),                       
            'throat': (0, 0.18),                       

            # UPPER TORSO
            'pec_r': (0, 0.81),                       
            'pec_l': (0, 0.81),                       
            'rib_r': (0, 0.72),                      # Hard
            'rib_l': (0, 0.72),                      # Hard
            'sternum': (0, 1.08),                    # Hard
            'heart': (0, 0),                      
            'lung_r': (0, 0.18),                    
            'lung_l': (0, 0.18),                    
            'diaphragm': (0, 0.27),                  
            'thoracic_viscera': (0, 0.09),            
            'liver': (0, 0.27),                      

            # LOWER TORSO
            'abdomen': (0, 0.72),      
            'abdominal_viscera': (0, 0.09),
            'spleen': (0, 0.27),
            'groin': (0, 0.18),         

            # BACK
            'spine': (0, 1.08),                      # Hard        
            'upper_back': (0, 0.81), 
            'lower_back': (0, 0.81), 
            'kidney_r': (0, 0.27),
            'kidney_l': (0, 0.27),                  

            # LEGS
            'glute_r': (0, 0.81),        
            'glute_l': (0, 0.81),       
            'quad_r': (0, 0.81),       
            'quad_l': (0, 0.81),       
            'hamstring_r': (0, 0.72),
            'hamstring_l': (0, 0.72),
            'knee_r': (0, 0.54),                    # Hard
            'knee_l': (0, 0.54),                    # Hard
            'shin_r': (0, 0.54),                    # Hard
            'shin_l': (0, 0.54),                    # Hard
            'calf_r': (0, 0.72),        
            'calf_l': (0, 0.72),        
            'foot_r': (0, 0.36),       
            'foot_l': (0, 0.36),    
            
            # ARMS
            'shoulder_r': (0, 0.72),    
            'shoulder_l': (0, 0.72),  
            'armpit_r': (0, 0.36),      
            'armpit_l': (0, 0.36),           
            'upper_arm_r': (0, 0.72),     
            'upper_arm_l': (0, 0.72),     
            'elbow_r': (0, 0.27),                   # Hard
            'elbow_l': (0, 0.27),                   # Hard
            'forearm_r': (0, 0.54),                   
            'forearm_l': (0, 0.54),     
            'hand_r': (0, 0.27),
            'hand_l': (0, 0.27),

        },
    }
    dmg_absorbtion_data = ds_sub_categories(dmg_absorbtion)
###
class Vigor:
    def __init__(self):
        self.recovery_rate_df = self.recovery_rate_data # % healing rate
        self.intervention_receptivity_df = self.intervention_receptivity_data # % effectivenesss of interventions
        self.resistance_df = self.resistance_data # chronic damage absorbtion

    recovery_rate = { 
        'male': (10,3),
        'female': (10,3),
    }
    recovery_rate_data = ds_main_categories(recovery_rate)

    intervention_receptivity = {
        'male': {
            'pharmacological_effectiveness': (95,15),
            'surgery_success_rate': (100,15),
            'cybergnetic_integration': (100,15),
            'mutagenic_uptake': (97,15),
        },
        'female': {
            'pharmacological_effectiveness': (105,15),
            'surgery_success_rate': (100,15),
            'cybergnetic_integration': (100,15),
            'mutagenic_uptake': (103,15),
        },
    }
    intervention_receptivity_data = ds_sub_categories(intervention_receptivity)

    resistance = { 
        'male': {
            'elemental_burn': (5, 11.25),
            'elemental_freeze': (5, 11.25),
            'elemental_shock': (3, 11.25),
            'elemental_corrosive': (2, 11.25),
            'bio_bleed': (5, 11.25),
            'bio_poison': (5, 11.25),
            'bio_infection': (-5, 11.25),
            'bio_airway': (-2, 11.25),
            'bio_respiratory': (5, 11.25),
            'bio_circulatory': (-2, 11.25),
            },
        'female': {
            'elemental_burn': (-5, 11.25),
            'elemental_freeze': (-5, 11.25),
            'elemental_shock': (-3, 11.25),
            'elemental_corrosive': (-2, 11.25),
            'bio_bleed': (-5, 11.25),
            'bio_poison': (-5, 11.25),
            'bio_infection': (5, 11.25),
            'bio_airway': (2, 11.25),
            'bio_respiratory': (-5, 11.25),
            'bio_circulatory': (2, 11.25),
            },
        }
    resistance_data = ds_sub_categories(resistance)

#############################################################################

# Intelligence

class Memory:
    def __init__(self):
        self.information_retention_df = self.information_retention_data # scaled score memory (learning speed)

    information_retention = {
        'male':{
            'declaritive_semantic': (102,15), # general knowledge
            'delcaritive_episodic': (95,15), # personal events
            'implicit_procedural': (100,15), # skills and habits
            'implicit_perceptual': (100,15), # involves improving the ability to perceive or recognize stimuli through repeated exposure, like recognize birds based on their song over time
            'implicit_associative': (100,15), # involves learned association between two stimuli or a stimulus and a response, such as classical conditioning
            'implicit_nonassociative': (98,15), # involves changes in behavior after repeated exposure to a single stimulus, such as habituation (decreasing response) or sensitization (increasing response)           
        },
        'female':{
            'declaritive_semantic': (98,15), # general knowledge
            'delcaritive_episodic': (105,15), # personal events
            'implicit_procedural': (100,15), # skills and habits
            'implicit_perceptual': (100,15), # involves improving the ability to perceive or recognize stimuli through repeated exposure, like recognize birds based on their song over time
            'implicit_associative': (100,15), # involves learned association between two stimuli or a stimulus and a response, such as classical conditioning
            'implicit_nonassociative': (102,15), # involves changes in behavior after repeated exposure to a single stimulus, such as habituation (decreasing response) or sensitization (increasing response)           
        }
    }
    information_retention_data = ds_sub_categories(information_retention)
###
class Logic:
    def __init__(self):
        self.reasoning_df = self.reasoning_data # skill checks

    reasoning = {
        'male': {
            'deductive': (100,15), # Drawing specific conclusions from general rules or premises
            'inductive': (100,15), # Generalizing patterns from specific examples or data
            'abductive': (100,15), # Inferring the most likely explanation for incomplete data
            'analogical': (100,15), # Recognizing relational similarities between different domains
            'mathematical': (102,15), # Applying logic in numeric or symbolic domains
            'visual-spatial': (103,15), # Using visual structure or spatial logic to solve problems
            'algorithmic': (100,15), # Processing multi-step procedures or rules in order
            'critical_evaluation': (100,15), # Judging arguments for bias, validity, and internal consistency
        },
        'female': {
            'deductive': (100,15),
            'inductive': (100,15),
            'abductive': (100,15),
            'analogical': (100,15),
            'mathematical': (98,15),
            'visual-spatial': (97,15),
            'algorithmic': (100,15),
            'critical_evaluation': (100,15),
        },
    }
    reasoning_data = ds_sub_categories(reasoning)
###
class Fluency:
    def __init__(self):
        self.processing_speed_df = self.processing_speed_data # standard score ps

    processing_speed = {
        'male': (100, 15),
        'female': (102, 15)
    }

    processing_speed_data = ds_main_categories(processing_speed)

#############################################################################

# Sagacity

class Perception:
    def __init__(self):
        self.situational_awareness_df = self.situational_awareness_data # each 100 * 15z grants more general info
        self.sensory_sensitivity_df = self.sensory_sensitivity_data # each 100 * 15z grants more focused info

    situational_awareness = {
        'male': (100, 15),
        'female': (100,15)
    }
    situational_awareness_data = ds_main_categories(situational_awareness)

    sensory_sensitivity = {
        'male': (95,15),
        'female': (105,15)
    }
    sensory_sensitivity_data = ds_main_categories(sensory_sensitivity)
###
class Intuition:
    def __init__(self):
        self.instincts_df = self.instincts_data # ability to detect empathic influence (deception, charm, etc)
        self.o_interpersonal_insight_df = self.o_interpersonal_insight_data # abiltiy to know somone else's emotional state and other stats
        self.s_intrapersonal_insight_df = self.s_intrapersonal_insight_data # abiltiy to know one's own emotional state and other stats

    instincts = {
        'male': {
            'charm': (95,15),
            'intimidation': (102,15),
            'seduction': (95,15),
            'deception': (98,15),
        },
        'female': {
            'charm': (105,15),
            'intimidation': (98,15),
            'seduction': (105,15),
            'deception': (102,15),
        }
    }
    instincts_data = ds_sub_categories(instincts)

    o_interpersonal_insight = {
        'male': (95,15),
        'female': (105,15)
    }
    o_interpersonal_insight_data = ds_main_categories(o_interpersonal_insight)

    s_intrapersonal_insight = {
        'male': (95,15),
        'female': (105,15)
    }
    s_intrapersonal_insight_data = ds_main_categories(s_intrapersonal_insight)
###
class Composure:
    def __init__(self):
        self.stress_modulation_df = self.stress_modulation_data # efficacy of stress reduction
        self.emotional_stability_df = self.emotional_stability_data # baseline stress threshold


    stress_modulation = {
        'male': (102,15),
        'female': (98,15)
    }
    stress_modulation_data = ds_main_categories(stress_modulation)

    emotional_stability = {
        'male': (105,15),
        'female': (95,15)
    }
    emotional_stability_data = ds_main_categories(emotional_stability)

#############################################################################

# Influence

class Influence:
    def __init__(self):
        self.charm_df = self.charm_data
        self.seduction_df = self.seduction_data
        self.deception_df = self.deception_data
        self.intimidation_df = self.intimidation_data

    charm = {
        'male': (95,15),
        'female': (105,15)
    }
    charm_data = ds_main_categories(charm)

    seduction = {
        'male': (100,15),
        'female': (105,15)
    }
    seduction_data = ds_main_categories(seduction)

    deception = {
        'male': (95,15),
        'female': (105,15)
    }
    deception_data = ds_main_categories(deception)

    intimidation = {
        'male': (95,15),
        'female': (105,15)
    }
    intimidation_data = ds_main_categories(intimidation)

#############################################################################
