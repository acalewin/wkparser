Pulls Kanji data from Wanikani.

takes a supplied file and compares it line by line against the list of burned and enlightened elements.
If the percentage of known kanji in the line is above threshold it kicks the line out.

it caches the kanji data in kanji_cache.txt in case you want to use it offline.

Usage is:
   python wkreader.py -a <apikey> -i <input file> [-t <threshold percentage>] [-p] [-b]