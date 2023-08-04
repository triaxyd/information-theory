#Triantafyllos Xydis

import numpy as np


def compress(file,stats):
    # Turn file to binary based on codings
    compressed_file = ""
    for symbol in file:
        for key in stats:
            if symbol == key[0]:
                compressed_file += key[1]['code']
    return compressed_file


def decompress(file,stats):
    # Turn file to binary based on codings
    decompressed_file = ""
    current_code = ""
    for bit in file:
        current_code += bit
        for key in stats:
            if current_code == key[1]['code']:
                decompressed_file += key[0]
                current_code = ""
                break
    return decompressed_file


def make_list(file):
    # Create a list with all symbols
    symbols_list = []
    for symbol in file:
        symbols_list.append(symbol)
    return symbols_list


def get_stats(symbols_list):
    # Create a dictionary with symbol stats
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
    for symbol in stats:
        total_prob += symbol[1]['prob'] 

    current_prob = 0.0
    split_index = 0

    # Find the index to divide the list based on probability
    for symbol in stats:
        current_prob += symbol[1]['prob']
        if current_prob >= total_prob / 2:
            if current_prob - (total_prob / 2) > (total_prob / 2) - (current_prob - symbol[1]['prob']):
                split_index = stats.index(symbol) - 1
            else:
                split_index = stats.index(symbol)
            break

    # Divide the list 
    left_part = stats[:split_index + 1]
    right_part = stats[split_index + 1:]

    # Add prefix to each symbol
    if(len(left_part) == 1):
        left_part[0][1]['code'] = prefix + "0"
    else:    
        divide_list(left_part,prefix + "0")

    if(len(right_part) == 1):
        right_part[0][1]['code'] = prefix + "1"
    else:
        divide_list(right_part,prefix + "1")
    
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
    sorted_stats = sorted(coded_list, key=lambda x: x[0], reverse=False)


    '''
    # Print the stats
    for symbol in sorted_stats:
        print(symbol[0] + " - Occurences: " + str(symbol[1]['occ']) + " - Probability: " + str(round(symbol[1]['prob'],5)) + " - Expected Length: " + str(symbol[1]['w_len']) + " - Code: " + str(symbol[1]['code']))
        print("*********************")
    '''

    # Compress the file
    return compress(file,sorted_stats) , sorted_stats