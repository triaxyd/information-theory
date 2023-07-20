#Triantafyllos Xydis

import numpy as np



def make_list(file):
    symbols_list = []
    for symbol in file:
        symbols_list.append(symbol)
    return symbols_list


def get_stats(symbols_list):
    stats = {}
    for symbol in symbols_list:
        if symbol in stats:
            stats[symbol]['occ'] += 1
        else:
            stats[symbol] = {'occ': 1 , 'prob': 0 ,'log2' : 0 , 'w_len': 0 , 'code': ''}

    #count the probability of each symbol
    total_symbols = len(symbols_list)
    for symbol in stats:
        stats[symbol]['prob'] = stats[symbol]['occ'] / total_symbols

    #get log2 and word length of each symbol
    for symbol in stats:
        stats[symbol]['log2'] = - np.log2(stats[symbol]['prob'])
        stats[symbol]['w_len'] = int(np.ceil(stats[symbol]['log2']))
    
    return stats


def divide_list(stats,prefix=""):
    total_prob = 0.0
    for item in stats:
        total_prob += item[1]['prob'] 

    current_prob = 0.0
    split_index = 0

    # Find the index to divide the list in half based on probability
    for item in stats:
        current_prob += item[1]['prob']
        if current_prob >= total_prob / 2:
            if current_prob - (total_prob / 2) > (total_prob / 2) - (current_prob - item[1]['prob']):
                split_index = stats.index(item) - 1
            else:
                split_index = stats.index(item)
            break

    # Divide the list in half
    left_part = stats[:split_index + 1]
    right_part = stats[split_index + 1:]

    # Add prefix to each symbol
    if(len(left_part) == 1):
        left_part[0][1]['code'] = prefix + "0"
    else:    
        left_divided = divide_list(left_part,prefix + "0")

    if(len(right_part) == 1):
        right_part[0][1]['code'] = prefix + "1"
    else:
        right_divided = divide_list(right_part,prefix + "1")
    
    # Merge the two lists
    merged_list = left_part + right_part

    return merged_list
    
    
    
def shannon_fano(file):
    # Create the list of symbols
    symbols_list = make_list(file)

    # Get occurrences and probability for each symbol
    stats = get_stats(symbols_list)

    # Sort the stats dictionary based on probs in descending order
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['prob'], reverse=True)

    # Divide the list recursively and add prefix to each symbol
    coded_list = divide_list(sorted_stats)


    # Sort the coded list based on symbols in ascending order
    sorted_codes = sorted(coded_list, key=lambda x: x[0], reverse=False)
    for item in sorted_codes:
        print(item[0] + " - Occurences: " + str(item[1]['occ']) + " - Probability: " + str(round(item[1]['prob'],5)) + " - Expected Length: " + str(item[1]['w_len']) + " - Code: " + str(item[1]['code']))
        print("*********************")
    








