#!/usr/bin/env python

import json, os, re

phonetic_words = {}

with open("cmudict.rep") as cmudict_source:
    for _ in range(49):
        next(cmudict_source)
    for line in cmudict_source:
        entry = line.split('  ')
        if (len(entry) > 0):
            phonetic_words[entry[0]] = [[p for p in s.split()] for s in entry[1].split(" - ")]

with open(os.path.expanduser("~/.local/share//plover/main.json")) as data_file:
    stenodict = json.load(data_file)

onset = {
    'B': 'PW',
    'CH': 'KH',
    'D': 'TK',
    'DH': 'TH',
    'F': 'TP',
    'G': 'TKPW',
    'HH': 'H',
    'JH': 'SKWR',
    'K': 'K',
    'L': 'HR',
    'M': 'PH',
    'N': 'TPH',
    'P': 'P',
    'R': 'R',
    'S': 'S',
    'SH': 'SH',
    'T': 'T',
    'TH': 'TH',
    'V': 'SR',
    'W': 'W',
    'Y': 'KWR',
    'Z': 'S*'
}

nucleus = {
    'AA': 'O',
    'AE': 'A',
    'AH':  'U',
    'AO': 'AU',
    'AW': 'OU',
    'AY': 'AOEU',
    'EH': 'E',
    'ER': 'ER',
    'EY': 'AEU',
    'IH': 'EU',
    'IY': 'AOE',
    'OW': 'OE',
    'OY': 'OEU',
    'UH': 'U',
    'UW': 'AOU'
}

coda = {
    'ER': 'R',
    'B':'B',
    'CH': 'FP',
    'D': 'D',
    'DH': '*T',
    'F': 'F',
    'G': 'G',
    'JH': 'PBLJ',
    'K': 'BG',
    'L': 'L',
    'M': 'PL',
    'N': 'PB',
    'NG': 'PBG',
    'P': 'P',
    'R': 'R',
    'S': 'S',
    'SH': 'RB',
    'T': 'T',
    'TH': '*T',
    'V': 'F',
    'Z': 'Z'
}

def word_to_steno(word):
    outline = []
    for syllable in phonetic_words[word.upper()]:
        segs = []
        seg = []

        for phone in syllable:
            if phone[-1].isnumeric():
                segs.append(seg)
                segs.append([phone])
                seg = []
            else:
                seg.append(phone)
        segs.append(seg)

        if len(segs) == 3:
            stroke = ''
            for phone in segs[0]:
                stroke += onset.get(phone[:2], '')
            for phone in segs[1]:
                stroke += nucleus.get(phone[:2], '')
            for phone in segs[2]:
                stroke += coda.get(phone[:2], '')
            outline.append(stroke)
    return '/'.join(outline)

generated_dict = {}
duplicate_regex = re.compile('\(\d\)')
steno_regex = re.compile('^S?T?K?P?W?H?R?(-|A?O?\*?E?U?)F?R?P?B?L?G?T?S?D?Z?$')
for word in phonetic_words.keys():
    outline = word_to_steno(word)

    bad_stroke = False
    for stroke in outline.split('/'):
        if steno_regex.match(stroke) is None:
            bad_stroke = True
    if bad_stroke:
        continue
    
    if duplicate_regex.match(word[-3:]) is not None:
        translation = word[:-3].lower()
    else:
        translation = word.lower()

    generated_dict[outline] = translation
    
with open("generated_dict.json", 'w') as output:
    output.write(json.dumps(generated_dict, indent=2))

matching_dict = {}
with open("matching_outlines", 'w') as output:
    for outline, word in generated_dict.items():
        if outline in stenodict.keys():
            print(word.lower(), file=output);

            if word == stenodict[outline].lower():
                matching_dict[outline] = stenodict[outline]

with open("matching_dict.json", 'w') as output:
    output.write(json.dumps(matching_dict, indent=2))
