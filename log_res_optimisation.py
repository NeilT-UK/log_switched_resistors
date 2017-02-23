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
    return max_step/total_ratio

def how_good_Rs(r_list):
    # take an even length list of resistors
    # return a scalar of how good they are
    # check the input resistors for small values
    base = 0
    for r in r_list:
        if r<=low_limit:
            base += 1
    
    # add a unit resistor on the start, keeps the scaling
    Rs = [1]
    Rs.extend(r_list)
    v_list = calc_resistances(Rs)
    return goodness(v_list)+base



def short_print(inp):
    for val in inp:
        print('{:2.4f}, '.format(val), end='')
    print()
    



        
import numpy as np
import scipy.optimize as so
import random
import math

"""
import matplotlib.pyplot as plt
import matplotlib as mplt
import pylab as plb
"""



# make initial vector of resistors

low_limit = 0.3

start_pos = []
for i in range(8):
    start_pos.append(random.uniform(0.3, 10))
start_pos = [1,1,1,1]

rs = np.array(start_pos)

print(how_good_Rs(rs))

opt = so.minimize(how_good_Rs, rs, method='Nelder-Mead')

print(opt)
result = opt['x']
print()
print(result)

print()
print()
print('starting array')
short_print(start_pos)
print('with low limit of ', low_limit)

all_Rs = [1]+list(result)
print()
print('resistors')
short_print(all_Rs)
print('resistance range ', max(all_Rs)/min(all_Rs))

values = calc_resistances(all_Rs)
print()
print('give {} resistance values'.format(len(values)))
short_print(values)

ratios = calc_steps(values)
max_ratio = max(ratios)
total_ratio = values[-1]/values[0]
print()
print('total ratio   ', total_ratio)
print('max_ratio     ', max_ratio)
print('goodness      ', max_ratio/total_ratio)

print()
print('detail ratios')
short_print(ratios)



"""

# optional graph plot

plb.ion()
f = plb.figure()
s = f.add_subplot("111")

dB_list = []
for res in values:
    dB_list.append(20*math.log10(res))

x_axis = list(range(len(values)))
line = mplt.lines.Line2D( x_axis, dB_list, marker='o' )

s.add_line( line )
s.relim()
s.autoscale_view()
s.figure.canvas.draw()
plb.draw()

wait = input('pausing - ')

"""









