# emoji-www

# Plan
Are there different emoji usages per borough / neighborhood ?
Are there emojis that occur in certain areas more than others?  
Are there neighborhoods which overuse or underuse emojis?
If you take a topic (ie. soccer)

Objects/sentiment from image.
Emoji w.r.t. Points of Interest.
Create an alternative map of Manhattan based on emoji-driven neighborhoods.

# Usage

- ``test.py`` script uses ``sample.txt`` 

- ``emoji.py`` will try to fetch the latest emoji definitions from unicode.org and store them in a file called
``codepoints_latest.json`` 
 
 
# Data
pid2info, nycemoji.csv https://drive.google.com/drive/u/1/folders/0Bw7JqtQBdsZSSDdWN1VlMHVNN1E

# Data format
Files ``chinese.tsv`` and ``english.tsv`` contain the extracted short canonical sequences, emojis, canonical emojis, skin tones and variations from each caption, with a Chinese and English pre-processing respectively.

Schema is: post_id<tab>comma_separated_sequences<tab>comma_separated_emojis<tab>comma_separated_canonical_emojis<tab>comma_separated_skin_tones<tab>comma_separated_variations

Example: 
``977726107265881718_452803412	👭👫👬👪💑🌸🙌	👭,👫,👬,👩‍👩‍👧,👩‍❤️‍👩,🌸,🙌🏼	👭,👫,👬,👪,💑,🌸,🙌	-1,-1,-1,-1,-1,-1,2	-1,-1,-1,20,15,-1,-1``
These files are meant to compute the counts.

Files ``chinese-tokens.tsv`` and ``english-tokens.tsv`` contain the Chinese and English pre-processed captions tokenized as we discussed (i.e., isolating the short canonical emoji sequences in context).
Schema is: post_id<tab><T/E><tab>text/emoji_sequence<tab><T/E><tab>text/emoji_sequence<tab><T/E><tab>text/emoji_sequence...
Example: 
``492186542997358343_11986392	T	Pretty sure that's a smile! E	🐾🐺	T	#shibatatum	E	🐕🐾``
These files are meant to compute the embeddings.
