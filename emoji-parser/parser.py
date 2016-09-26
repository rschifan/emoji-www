import re
import emoji

CODEPOINTS = emoji.get_codepoints()
EMOJI = '(%s(?!%s))|(%s(?=%s))' %(CODEPOINTS['Emoji_Presentation'], CODEPOINTS['Text_Presentation_Selector'], CODEPOINTS['Emoji'], CODEPOINTS['Emoji_Presentation_Selector'])
EMOJI_CHARS = '%s|%s|%s|%s' %(EMOJI, CODEPOINTS['Emoji_Modifier'], CODEPOINTS['Emoji_ZWJ_Separator'], CODEPOINTS['Emoji_Presentation_Selector'])
EMOJI_SEQUENCE = '%s|%s|%s|%s|%s' %(CODEPOINTS['Emoji_ZWJ_Sequence'], CODEPOINTS['Emoji_Modifier_Sequence'], CODEPOINTS['Emoji_Flag_Sequence'], CODEPOINTS['Emoji_Combining_Sequence'], EMOJI)

SKIN_TONES = []
skin_tone = re.search('(?<=\[).+(?=\-)', CODEPOINTS['Emoji_Modifier'], re.UNICODE).group(0).encode('utf-8').decode('unicode_escape')
while skin_tone <= re.search('(?<=\-).+(?=\])', CODEPOINTS['Emoji_Modifier'], re.UNICODE).group(0).encode('utf-8').decode('unicode_escape'):
    SKIN_TONES.append(skin_tone)
    skin_tone = chr(ord(skin_tone) + 1)

HEAVY_BLACK_HEART = u'\u2764'
NEUTRAL_ZWJ_SEQUENCES = []
for zwj_sequence in re.sub('[\(\)]', '', CODEPOINTS['Emoji_ZWJ_Neutral'], re.UNICODE).split('|'):
    NEUTRAL_ZWJ_SEQUENCES.append(zwj_sequence.encode('utf-8').decode('unicode_escape'))
ZWJ_SEQUENCE_VARIATIONS = []
for zwj_variation in re.sub('[\(\)]', '', CODEPOINTS['Emoji_ZWJ_Sequence'], re.UNICODE).split('|'):
        ZWJ_SEQUENCE_VARIATIONS.append(zwj_variation.encode('utf-8').decode('unicode_escape'))

# Shows the Unicode characters corresponding to the text.
def show_unicode(text):
    return str(text.encode('unicode_escape'))

# Returns true if the text contains at least one emoji.
def has_emoji(text):
    return re.search(EMOJI, text, re.UNICODE) != None

# Returns a copy of the text without whitespaces between emoji sequences.
def remove_emoji_whitespaces(text):
    regex = '(%s)\s+(?=(%s))' %(EMOJI_SEQUENCE, EMOJI_SEQUENCE)
    return re.sub(regex, '\g<1>', text, 0, re.UNICODE)

# Returns a copy of the text with whitespaces between regular characters and emoji.
def pad_emoji_sequences(text):
    regex = '([\d\w])(?=%s)' %(EMOJI)
    text = re.sub(regex, '\g<1> ', text, 0, re.UNICODE)
    regex = '(?<=%s)([\d\w])' %(EMOJI)
    return re.sub(regex, ' \g<1>', text, 0, re.UNICODE)

# Returns all the sequences of emojis with no whitespaces in between contained in the text.
def get_emoji_sequences(text):
    sequences = []
    for match in re.finditer('(%s)+' %(EMOJI_SEQUENCE), text, re.UNICODE):
        sequences.append(match.group(0))
    return sequences

# Returns true if the token contains emoji and no other characters.
def is_emoji_sequence(sequence):
    regex = re.compile('^(%s)+$' %(EMOJI_CHARS), re.UNICODE)
    return regex.match(sequence) != None

# Returns the neutral "yellow" version of the sequence.
def get_canonical_sequence(sequence):
    sequence = re.sub(CODEPOINTS['Emoji_Modifier'], '', sequence, 0, re.UNICODE)
    if re.search(CODEPOINTS['Emoji_ZWJ_Sequence'], sequence, re.UNICODE):
        separators = len(re.findall(CODEPOINTS['Emoji_ZWJ_Separator'], sequence, re.UNICODE))
        if HEAVY_BLACK_HEART in sequence:
            separators += 1
        sequence = re.sub(CODEPOINTS['Emoji_ZWJ_Sequence'], NEUTRAL_ZWJ_SEQUENCES[separators - 1], sequence, re.UNICODE)
    return sequence

# Returns the number of emojis in the sequence, ignoring modifiers.
def get_sequence_length(sequence):
    return len(re.findall(EMOJI_SEQUENCE, sequence, re.UNICODE))

# Returns a copy of the sequence with up to maxLength consecutive repetitions per emoji.
def get_short_sequence(sequence, max_length = 3):
    regex = r'(%s)\1{%i,}' %(EMOJI_SEQUENCE, max_length)
    return re.sub(regex, '\g<1>\g<1>\g<1>', sequence, re.UNICODE)

# Returns all the emojis in the sequence.
def get_emojis(sequence):
    emojis = []
    for emoji in re.finditer(EMOJI_SEQUENCE, sequence, re.UNICODE):
        emojis.append(emoji.group(0))
    return emojis

# Returns the neutral "yellow" version of the emoji.
def get_canonical_emoji(emoji):
    return get_canonical_sequence(emoji)

# Returns the skin tone of an emoji as a Fitzpatrick type (1-5). Returns 0 for the "yellow" version, -1 if the emoji cannot be modified.
def get_skin_tone(emoji):
    skin_modifier = re.search(CODEPOINTS['Emoji_Modifier'], emoji, re.UNICODE)
    if skin_modifier:
        return SKIN_TONES.index(skin_modifier.group(0)) + 1
    if re.search(CODEPOINTS['Emoji_Modifier_Base'], emoji, re.UNICODE):
        return 0
    return -1

# Returns the variation number (1-22) of an emoji. Returns 0 for the neutral version, -1 if the emoji is not a ZWJ sequence.
def get_variation(emoji):
    if emoji in NEUTRAL_ZWJ_SEQUENCES:
        return 0
    if emoji in ZWJ_SEQUENCE_VARIATIONS:
        return ZWJ_SEQUENCE_VARIATIONS.index(emoji) + 1
    return -1
