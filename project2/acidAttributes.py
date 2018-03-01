
# Hydrophobic - 'H'
# Polar - 'P'
# Small - 'S'
# Proline - 'R'
# Tiny - 'T'
# Aliphatic - 'L'
# Aromatic - 'A'
# Positive - '+'
# Negative - '-'
# Charged - 'C'
attributeTypes = {'H': {'name': 'Hydrophobic'}, 
        'P': {'name': 'Polar'},
        'S': {'name': 'Small'},
        'R': {'name': 'Proline'},
        'T': {'name': 'Tiny'},
        'L': {'name': 'Aliphatic'},
        'A': {'name': 'Aromatic'},
        '+': {'name': 'Positive'},
        '-': {'name': 'Negative'},
        'C': {'name': 'Charged'}
    }
attributes = dict()

attributes['A'] = {'H': 1, 'P': 0, 'C': 0, 'S': 1, 'T': 1, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['C'] = {'H': 1, 'P': 0, 'C': 0, 'S': 1, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['D'] = {'H': 0, 'P': 1, 'C': 1, 'S': 1, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 1, 'R': 0}
attributes['E'] = {'H': 0, 'P': 1, 'C': 1, 'S': 0, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 1, 'R': 0}
attributes['F'] = {'H': 1, 'P': 0, 'C': 0, 'S': 0, 'T': 0, 'L': 0, 'A': 1, '+': 0, '-': 0, 'R': 0}
attributes['G'] = {'H': 1, 'P': 0, 'C': 0, 'S': 1, 'T': 1, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['H'] = {'H': 0, 'P': 1, 'C': 1, 'S': 0, 'T': 0, 'L': 0, 'A': 1, '+': 1, '-': 0, 'R': 0}
attributes['I'] = {'H': 1, 'P': 0, 'C': 0, 'S': 0, 'T': 0, 'L': 1, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['K'] = {'H': 0, 'P': 1, 'C': 1, 'S': 0, 'T': 0, 'L': 0, 'A': 0, '+': 1, '-': 0, 'R': 0}
attributes['L'] = {'H': 1, 'P': 0, 'C': 0, 'S': 0, 'T': 0, 'L': 1, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['M'] = {'H': 1, 'P': 0, 'C': 0, 'S': 0, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['N'] = {'H': 0, 'P': 1, 'C': 0, 'S': 1, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['P'] = {'H': 1, 'P': 0, 'C': 0, 'S': 1, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 1}
attributes['Q'] = {'H': 0, 'P': 1, 'C': 0, 'S': 0, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['R'] = {'H': 0, 'P': 1, 'C': 1, 'S': 0, 'T': 0, 'L': 0, 'A': 0, '+': 1, '-': 0, 'R': 0}
attributes['S'] = {'H': 0, 'P': 1, 'C': 0, 'S': 1, 'T': 1, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['T'] = {'H': 1, 'P': 1, 'C': 0, 'S': 1, 'T': 0, 'L': 0, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['V'] = {'H': 1, 'P': 0, 'C': 0, 'S': 1, 'T': 0, 'L': 1, 'A': 0, '+': 0, '-': 0, 'R': 0}
attributes['W'] = {'H': 1, 'P': 0, 'C': 0, 'S': 0, 'T': 0, 'L': 0, 'A': 1, '+': 0, '-': 0, 'R': 0}
attributes['Y'] = {'H': 1, 'P': 1, 'C': 0, 'S': 0, 'T': 0, 'L': 0, 'A': 1, '+': 0, '-': 0, 'R': 0}
