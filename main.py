
import time
import keyboard

def get_abbrev(word, real_words, abbrevs):
    abbrev = word[0]
    i = 0
    for char in word:
        i += 1
        if i == 1: continue
        new_abbrev = abbrev + char
        if new_abbrev in real_words: continue
        if new_abbrev in abbrevs: continue
        return new_abbrev
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
        if i > 5: break
        new_abbrev = get_abbrev(word, words, abbrevs)
        if new_abbrev is None: continue
        abbrevs[word] = new_abbrev
        ff = open('AutoHotkey.ahk', 'a')
        ff.write('::' + new_abbrev + '::' + word + "\n")
        ff.close()
        print("Added " + word + " as " + new_abbrev)
    return abbrevs

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
    abbrevs[word] = abbrev

ff = open('words.txt', 'r')
lines = ff.readlines()
ff.close()
words = []
for line in lines:
    line = line.replace("\n", "")
    words.append(line)
keyboard.hook(keyEvent)
words_history = {}
while True:
    if 'space' in keystrokes or 'comma' in keystrokes:
        keystrokes = keystrokes.replace("space","").replace("comma","")
        if len(keystrokes) > 4:
            if "backback" in keystrokes or "caps lock" in keystrokes or "ctrl" in keystrokes or "alttab" in keystrokes:
                keystrokes = ''
                continue
            value = 0
            if keystrokes in words_history.keys():
                value = words_history[keystrokes]
            value += 1
            words_history[keystrokes] = value
            if len(words_history) > 500:
                words_history.pop(0)
            abbrevs = add_new_words(words_history, words, abbrevs)
        if keystrokes in abbrevs.keys() and len(keystrokes) > 4 and "'" not in keystrokes:
            print("Suggestion:", abbrevs[keystrokes], "for", keystrokes)
            #print(keystrokes)
        keystrokes = ''
    time.sleep(0.05)