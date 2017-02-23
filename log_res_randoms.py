# program to compute resistance of my series/parallel switched resistors
# rewritten to sort out spaghetti


def calc_resistance(resistors, switch_code):
    # given an iterable of odd length of resistor values
    # and a binary code for switch closures
    # the switches being in my standard 'hopping along by two' pattern
    # return the resistance of that configuration

    # build list of nodes and resistors
    # first node, connected
    node_pol = 1
    items = [['node',node_pol, 1]]

    # middle nodes
    for bit in range(len(resistors)):
        node_pol = -node_pol
        items.append(['res', resistors[bit]])
        items.append(['node', node_pol, 0])

    # last node, connected
    items[-1][2] = 1

    # set the nodes to the switch values
    code_copy = int(switch_code)
    for item in items[2:-2]:
        if item[0]=='node':
            item[2] = code_copy & 1
            code_copy >>= 1

    # now pass though coallescing all resistors that are in series
    done = False
    while not done:
        done = True
        for (i, item) in enumerate(items):
            if (item[0]=='node'): # if it's a node item
                if item[2]==0:    # and if this node is unswitched
                    done = False
                    items[i-1][1] += items[i+1][1]    # sum the resistors on either side to the left
                    del items[i]   # remove the node
                    del items[i]   # remove the RH resistor
                    break      # force a restart of the loop
                               # as we've modified the length of the list inside a for

    # now pass through finding whether each resistor contributes or not
    total_current = 0
    for (i, item) in enumerate(items):
        if item[0]=='res':
            pd = abs(items[i-1][1]-items[i+1][1])/2
            current = pd/item[1]
            total_current += current

    return 1/total_current


def calc_resistances(resistors):
    # return a sorted list of all distinct values
    # when the switches are cycled through all possible settings
    
    res_vals = set()
    settings = pow(2, len(resistors)-1)
    # print(settings)
    for switch_code in range(settings):
        res = calc_resistance(resistors, switch_code)
        res = round(res, 6)   # quantise to 6 digits to remove near duplicates
        res_vals.add(res)

    res_list = list(res_vals)
    res_list.sort()
    return res_list
        

def calc_steps(r_list):
    # return a list of the ratios
    ratios = []
    first = r_list[0]
    for second in r_list[1:]:
        ratios.append(round(second/first, 6))
        first = second
    return ratios

def goodness(value_list):
    # return a goodness function from the sorted value list, the lower the better
    # as a first crack, try minimising the size of the maximum step
    # but max_step normalised to total_ratio looks better
    total_ratio = value_list[-1]/value_list[0]
    # print(total_ratio)
    
    ratios = calc_steps(value_list)
    max_step = max(ratios)
    return (max_step/total_ratio, max_step, total_ratio)

def how_good_Rs(r_list):
    # take an even length list of resistors
    # return a scalar of how good they are
    # add a unit resistor on the start, keeps the scaling
    Rs = [1]
    Rs.extend(r_list)
    v_list = calc_resistances(Rs)
    return goodness(v_list)


def short_print(inp):
    for val in inp:
        print('{:2.4f}, '.format(val), end='')
    print()


import random       

n_res = 9
best = 1
spread = (0.2, 4)

for go in range(10):
    rs = []
    for r in range(n_res-1):
        rs.append(random.uniform(*spread))

    good = how_good_Rs(rs)
    if good[0]<best:
        best = good[0]
        print()
        short_print(rs)
        print(good)


"""
rs = [ 1.46560092,  2.14791218]
rx = [1]+rs
print(calc_steps(calc_resistances(rx)))

"""





