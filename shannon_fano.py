#Triantafyllos Xydis

import numpy as np

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


def make_list(file):
    symbols_list = []
    for symbol in file:
        symbols_list.append(symbol)
    return symbols_list


def shannon_fano(file):
    # Create the list of symbols
    symbols_list = make_list(file)

    # Get occurrences and probability for each symbol
    stats = get_stats(symbols_list)

    # Sort the stats dictionary based on probs in descending order
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['prob'], reverse=True)

    print(sorted_stats)




