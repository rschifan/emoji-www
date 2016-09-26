import re
from parser import *

try:
    input_file = open('sample.txt')
    for line in input_file.read().splitlines():
        if len(line.strip()) > 0:
            text = line.strip()
            print('TEXT: ' + text + '\t(' + show_unicode(text) + ')')
            if has_emoji(text):
                text = remove_emoji_whitespaces(text)
                text = pad_emoji_sequences(text)
                print('\tNo whitespaces, padded: ' + text)
                sequences = get_emoji_sequences(text)
                print('\tSEQUENCES:')
                for sequence in sequences:
                    print('\t\t' + sequence)
                    print('\t\tSequence length: ' + str(get_sequence_length(sequence)))
                    print('\t\tCanonical sequence: ' + get_canonical_sequence(sequence))
                    print('\t\tShort sequence: ' + get_short_sequence(sequence))
                    print('\t\tEMOJIS:')
                    for emoji in get_emojis(sequence):
                        print('\t\t\t' + emoji)
                        print('\t\t\tCanonical emoji: ' + get_canonical_emoji(emoji))
                        print('\t\t\tSkin color: ' + str(get_skin_tone(emoji)))
                        print('\t\t\tVariation: ' + str(get_variation(emoji)))
            print()
    input_file.close()
except Exception as e:
    print(line)
    print("Error reading input file: %s" %(e))
    traceback.print_exc()
    exit()
