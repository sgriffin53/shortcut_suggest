
import time
import keyboard
import wordfreq
import inflect
from nltk.corpus import wordnet as wn
global banned_abbrevs

banned_abbrevs = ["ai", "lol", "didn", "wasn", "got", "gp", "gps"]
def get_abbrev(word, real_words, abbrevs):
    global banned_abbrevs
    abbrev = word[0]
    i = 0
    three_abbrevs = []
    four_abbrevs = []
    five_abbrevs = []
    for char in word:
        i += 1
        if i == 1: continue
        new_abbrev = abbrev + char
        j = 0
        for char2 in word:
            j += 1
            if j <= 1: continue
            three_abbrev = new_abbrev + char2
            if three_abbrev not in three_abbrevs: three_abbrevs.append(three_abbrev)
        if new_abbrev in real_words: continue
        if new_abbrev in abbrevs.values(): continue
        if new_abbrev in banned_abbrevs: continue
        if len(new_abbrev) <= 1: continue
        return new_abbrev
    i = 0
    three_abbrevs.reverse()
    for abbrev in three_abbrevs:
        #first_letter = abbrev[0]
        i+=1
        j = 0
        for char in word:
            j += 1
            if j <= 1: continue
            four_abbrev = abbrev + char
          #  if word == "access": print(":", four_abbrev)
            four_abbrevs.append(four_abbrev)
        if abbrev in real_words: continue
        if abbrev in abbrevs.values(): continue
        if len(abbrev) <= 1: continue
        return abbrev
    i = 0
    for abbrev in four_abbrevs:
        i += 1
        j = 0
        for char in word:
            j += 1
            if j <= 1: continue
            five_abbrev = abbrev + char
            five_abbrevs.append(five_abbrev)
        if abbrev in real_words: continue
        if abbrev in abbrevs.values(): continue
        if len(abbrev) <= 1: continue
        return abbrev
    for abbrev in five_abbrevs:
        i = 0
        if abbrev in real_words: continue
        if abbrev in abbrevs.values(): continue
        if len(abbrev) <= 1: continue
        return abbrev
    return None

def add_new_words(words_history, real_words, abbrevs):
    if len(words_history) < 50: return abbrevs
    sorted_words = sorted(words_history, key=words_history.get, reverse=True)
    i = 0
    for word in sorted_words:
        count = words_history[word]
        if count < 3: continue
        if word in abbrevs.keys(): continue
        i += 1
        if i > 1500000: break
        new_abbrev = get_abbrev(word, words, abbrevs)
        if new_abbrev is None: continue
        if len(new_abbrev) == 4 and len(word) == 5: continue
        abbrevs[word] = new_abbrev
        ff = open('AutoHotkey.ahk', 'a')
        ff.write('::' + new_abbrev + '::' + word + "\n")
        ff.close()
        print("Added " + word + " as " + new_abbrev)
    return abbrevs

def add_plurals(abbrevs):
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    plurals = {}
    for key in abbrevs.keys():
        word = key
        if word not in nouns: continue
        abbrev = abbrevs[key]
        engine = inflect.engine()
        plural = engine.plural(word)
        if plural in abbrevs.keys(): continue
        print(word, plural)
        plurals[word] = plural
    for word in plurals.keys():
        plural = plurals[word]
        orig_abbrev = abbrevs[word]
        suffixes = ['s', 'z', 'j', 'ss', 'zz', 'jj']
        for suffix in suffixes:
            new_abbrev = orig_abbrev + suffix
            if new_abbrev in abbrevs.values():
                continue
            ff = open('AutoHotkey.ahk', 'a')
            ff.write('::' + new_abbrev + '::' + plural + "\n")
            ff.close()
            print("Added " + new_abbrev + " as " + plural)
            break



ff = open('AutoHotkey.ahk', 'r', encoding='utf-8')
lines = ff.readlines()
ff.close()

global keystrokes
keystrokes = ''
def keyEvent(e):
    global keystrokes
    if e.event_type == 'down':
        keystrokes += e.name

abbrevs = {}
for line in lines:
    line = line.replace("\n", "")
    abbrev = line.split("::")[1]
    word = line.split("::")[2]
    abbrevs[word.lower()] = abbrev


ff = open('words.txt', 'r')
lines = ff.readlines()
ff.close()
words = []
for line in lines:
    line = line.replace("\n", "")
    words.append(line)

#add_plurals(abbrevs)

keyboard.hook(keyEvent)
words_history = {}
do_dict_add = False
if do_dict_add:
    for word in words:
        if word in abbrevs: continue
        if word in banned_abbrevs: continue
        if '-' in word or '(' in word or ')' in word: continue
        abbrev = get_abbrev(word, words, abbrevs)
        #if word != "access:": continue
        if len(word) < 5: continue
        if abbrev is None: print(word, "None")
        #print(word)
        #if abbrev == None: continue
        freq = wordfreq.word_frequency(word, 'en')
        if len(abbrev) > 1 and freq > 0.0000040:
            print(word, abbrev)
            words_history[word] = 5
    print("Adding " + str(len(words_history)) + " words.")
    add_new_words(words_history, words, abbrevs)
tot_chars_typed = 1
chars_saved = 0
while True:
    if 'space' in keystrokes or 'comma' in keystrokes or "." in keystrokes:
        keystrokes = keystrokes.replace("space","").replace("comma","").replace(",","").replace(".","").lower()
        if len(keystrokes) > 4:
            if "back" in keystrokes or "caps lock" in keystrokes or "ctrl" in keystrokes or "right shift" in keystrokes or "left shift" in keystrokes or "alttab" in keystrokes or "'" in keystrokes:
                keystrokes = ''
                continue
            value = 0
            if keystrokes in words_history.keys():
                value = words_history[keystrokes]
            value += 1
            words_history[keystrokes] = value
            if len(words_history) > 1000:
                words_history.pop(0)
            abbrevs = add_new_words(words_history, words, abbrevs)
        if keystrokes in abbrevs.keys() and len(keystrokes) > 4 and "'" not in keystrokes:
            chars_saved += len(keystrokes) - len(abbrevs[keystrokes])
            percent = chars_saved * 100 / tot_chars_typed
            percent = round(percent, 1)
            print("Suggestion:", abbrevs[keystrokes], "for", keystrokes, "- Saved:", str(chars_saved) + "/" + str(tot_chars_typed) + " (" + str(percent) + "%)")
            #print("Potential chars saved: " + str(chars_saved) + " (" + str(percent) + "%")
        tot_chars_typed += len(keystrokes) + 1
        keystrokes = ''
    time.sleep(0.05)