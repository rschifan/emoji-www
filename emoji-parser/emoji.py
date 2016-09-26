import re
import json
import os.path
import urllib.request

def get_codepoints(version = 'latest', store = True):
    CODEPOINTS = 'codepoints_%s.json' %(version)
    
    if os.path.isfile(CODEPOINTS):
        with open(CODEPOINTS) as fp:
            return json.load(fp)
    else:
        codepoints = fetch_codepoints(version)
        if store:
            with open(CODEPOINTS, 'w') as fp:
                json.dump(codepoints, fp)
        return codepoints

def fetch_codepoints(version = 'latest'):
    EMOJI_DATA = 'http://unicode.org/Public/emoji/%s/emoji-data.txt' %(version)
    EMOJI_SEQUENCES = 'http://unicode.org/Public/emoji/%s/emoji-sequences.txt' %(version)
    EMOJI_ZWJ_SEQUENCES = 'http://unicode.org/Public/emoji/%s/emoji-zwj-sequences.txt' %(version)
    
    RANGE = '..'
    SEQUENCE = ' '
    
    codepoints = dict()
    codepoints['Text_Presentation_Selector'] = '\\uFE0E'
    codepoints['Emoji_Presentation_Selector'] = '\\uFE0F'
    codepoints['Emoji_ZWJ_Separator'] = '\\u200D'
    codepoints['Emoji_ZWJ_Neutral'] = '(\\U0001F441\\u200D\\U0001F5E8)|\\U0001F46A|\\U0001F491|\\U0001F48F'
    
    def add_codepoints(url, separator):
        groups = []
        response = urllib.request.urlopen(url)
        charset = response.headers.get_content_charset()
        lines = response.readlines()
        for i in range(0, len(lines)):
            line = lines[i].decode(charset).strip()
            if len(line) > 0 and not line.startswith('#'):
                points = line[0:line.index(';')].strip().split(separator)
                group = line[line.index(';') + 1:line.index('#')].strip()
                if group not in codepoints.keys():
                    groups.append(group)
                    if separator == RANGE:
                        codepoints[group] = '['
                    else:
                        codepoints[group] = '('
                elif separator == SEQUENCE:
                    codepoints[group] += '|('
                for j in range(0, len(points)):
                    if len(points[j]) == 5:
                        codepoint = '\\U000' + points[j]
                    else:
                        codepoint = '\\u' + points[j]
                    codepoints[group] += re.sub('\*', '\\*', codepoint)
                    if separator == RANGE and j < len(points) - 1:
                        codepoints[group] += '-'
                if separator == SEQUENCE:
                    codepoints[group] += ')'
        if separator == RANGE:
            for group in groups:
                codepoints[group] += ']'
    
    add_codepoints(EMOJI_DATA, RANGE)
    add_codepoints(EMOJI_SEQUENCES, SEQUENCE)
    add_codepoints(EMOJI_ZWJ_SEQUENCES, SEQUENCE)
    
    return codepoints
