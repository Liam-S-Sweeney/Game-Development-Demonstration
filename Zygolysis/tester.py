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
            'gross_motor_control',]},
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
            'pain_tolereance',
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

# for field,subfield in all_fields.items():
#     for subfield_name,trait in subfield.items():
#         # print(field)