# trait = [0,1,2,3,4,5,6]
# total_selected = raw
# total_possible = 3 * Questions
# trait_ratio = total_selected / total_possible

# Initial perosnality test matches neo-pi-r test for baseline

# When a player character acts in accordance to their personalities, stress redution
# When a player character acts against their personality, stress increases
#   * Extent of change and thresholds determined by composure and decision

# Enough decions agaisnt ones personlity will eventually shift it into a new one
# More choices that align with certain personality traits makes it harder and harder to change and requires mroe and mroe stress to do so

personality_trait_questions_values = {
                    'openness': [1,2,3,4,5,6,7],
                    'conscientiousness': [1,2,3,4,5,6],
                    'extraversion': [5,4,3,2,1],
                    'agreeableness': [1,1,2,2,3,3],
                    'neuroticism':[7,7,7,7,7,7]
                    }

personality_trait_working_values = {
                    'openness': (0,0),
                    'conscientiousness': (0,0),
                    'extraversion': (0,0),
                    'agreeableness': (0,0),
                    'neuroticism': (0,0),
                    }

def base_personality_setup():
    for trait,choice in personality_trait_questions_values.items():
        total_possible = len(choice) * 7
        [[choice.__setitem__(selected, choice[selected] + choice[selected-1])]for selected in range(1,len(choice))]
        # trait_ratio = choice[::-1][0] / total_possible
        personality_trait_working_values[trait] = (choice[::-1][0],total_possible)

def personality_update(trait_letter,selected,possible):
    if trait_letter == 'o':
        trait_letter = 'openness'
    elif trait_letter == 'c':
        trait_letter = 'conscientiousness'
    elif trait_letter == 'e':
        trait_letter = 'extraversion'
    elif trait_letter == 'a':
        trait_letter = 'agreeableness'
    elif trait_letter == 'n':
        trait_letter = 'neuroticism'
    else:
        return(f'"{trait_letter.title()}" does not pair with personality traits, check for typo')
    
    try:
        initial_tuple = personality_trait_working_values[trait_letter]
        change_tuple = (selected,possible)
        updated_tuple = tuple(initial_tuple + change_tuple for initial_tuple,change_tuple in zip(initial_tuple,change_tuple))
        personality_trait_working_values[trait_letter] = updated_tuple
    except:
        print(f'Verify that {selected} and {possible} are intergers')
