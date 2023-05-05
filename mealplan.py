# Script for parsing mealplans and generating a shopping list
# python mealplan.py mealplan.txt > list.txt


import sys
import re


def get_lines(file):
    names = ['Alex', 'Lucia']
    result = []
    with open(file) as f:
        lines = f.read().splitlines()
    for line in lines:
        for n in names:
            if n in line:
                result.append(line.strip())
    return result


def process(lines):
    items = []
    for line in lines:
        _, meal = line.split(':')
        ingred = meal.split(',')
        for i in ingred:
            part = ''.join(c for c in i if c != '(' and c != ')').split()
            qty = [z for z in part if z[0].isdigit()]
            if not qty:
                qty = '0'
            else:
                qty = qty[-1]
            item = ' '.join(z for z in part if z[0].isalpha())
            items.append((item, qty))
    return items


def split_quantity_units(s):
    # The regular expression pattern consists of two groups:
    # 1. A group of one or more digits (\d+)
    # 2. An optional group of one or more non-digit characters (\D*) (using * instead of +)
    pattern = r"(\d+)(\D*)"
    
    match = re.match(pattern, s)
    
    if match:
        quantity, units = match.groups()
        return int(quantity) if quantity else 0, units if units else 'x'
    else:
        return 0, 'g'


def main(file):
    lines = get_lines(file)
    items = sorted(process(lines))
    result = []
    current_item = items[0][0]
    current_qty, current_units = split_quantity_units(items[0][1])
    idx = 1
    items.append(('end', '0g'))  # sentinel
    while idx < len(items):
        item = items[idx][0]
        qty, units = split_quantity_units(items[idx][1])
        if item == current_item and units == current_units:
            current_qty += qty
        else:
            result.append((current_item, current_qty, current_units))
            current_item, current_qty, current_units = item, qty, units
        idx += 1
    for r in result:
        print(f'{r[0]} {r[1]}{r[2]}')


if __name__ == '__main__':
    main(sys.argv[1])
