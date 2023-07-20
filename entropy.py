import numpy as np

def calc_ent(symbols):
    prob_dict = {x:symbols.count(x)/len(symbols) for x in symbols}
    probs = np.array(list(prob_dict.values()))
    return - probs.dot(np.log2(probs))



