import requests as req
import wordfreq
from langdetect import detect, DetectorFactory

def get_book(id):
    try:
        resp = req.get('https://www.gutenberg.org/ebooks/' + str(id))
    except Exception as e:
        print("except", e)
    for line in resp.text.split("\n"):
        if "Plain Text" in line:
            url = 'https://www.gutenberg.org' + line.split("href=\"")[1].split("\"")[0]
            resp = req.get(url)
            book = resp.text
            #print(book)
            return book
            #print(book)

def remove_non_letters(word):
    word = word.lower()
    new_word = ''
    for char in word:
        if char >= 'a' and char <= 'z':
            new_word += char
    return new_word

def remove_non_letters_upper(word):
    word = word.upper()
    new_word = ''
    for char in word:
        if char >= 'A' and char <= 'Z':
            new_word += char
    return new_word

def is_name_format(word):
    if len(word) == 0: return False
    if not word[0].isupper(): return False
    for char in word:
        allow = False
        if char >= 'A' and char <= 'Z':
            allow = True
        elif char >= 'a' and char <= 'z':
            allow = True
        if not allow: return False
    if word.replace(word[0],'').islower(): return True
    return False

abbrevs = {}
protected = True
protected_abbrevs = []
ff = open('AutoHotkey.ahk', 'r')
lines = ff.readlines()
ahk_lines = []
ff.close()
for line in lines:
    line = line.replace("\n","")
    abbrev = line.split("::")[1]
    if protected:
        protected_abbrevs.append(abbrev)
    if abbrev == 'zz':
        protected = False
    word = line.split("::")[2]
    ahk_lines.append(line)
#    print(abbrev, word)
    abbrevs[word] = abbrev

ff = open('words_big.txt', 'r')
lines = ff.readlines()
ff.close()
real_words = []
for line in lines:
    line = line.replace("\n", "")
    real_words.append(line)
to_remove = []

acronym_count = {}

for i in range(60,100000):
    print(i)
    book = get_book(i)
    if book is None: continue
    book = book.replace("\n", " ")
    DetectorFactory.seed = 0
    lang = detect(book)
    #print(lang)
    if lang != 'en': continue
    if "thesaurus" in book.lower() or "dictionary" in book.lower() or "world factbook" in book.lower() or "federalist papers" in book.lower(): continue
    if " les " in book: continue
    if " das " in book: continue
    if " es " in book: continue
    if " los " in book: continue
    #continue
    for word in book.split(" "):
        orig_word = word
        word = remove_non_letters(word)
     #   if orig_word.isupper(): print(word,"---")
        if word.lower() in protected_abbrevs: continue
        if word != orig_word and not orig_word.isupper() and not is_name_format(orig_word): continue
        if len(word) > 4: continue
        if word.lower() not in abbrevs.values(): continue
        if word in to_remove: continue
        freq = wordfreq.word_frequency(word, 'en')
        if freq < 0.000001 and not orig_word.isupper() and not is_name_format(orig_word): continue
        if word.lower() not in real_words and not orig_word.isupper() and not not is_name_format(orig_word): continue
        if is_name_format(orig_word):
            if orig_word.lower() not in real_words:
                print(orig_word.lower(), len(to_remove))
                to_remove.append(orig_word.lower())
        elif orig_word.isupper():
            new_word = remove_non_letters_upper(orig_word).lower()
            if new_word not in acronym_count.keys():
                acronym_count[new_word] = 0
            acronym_count[new_word] += 1
      #      print(orig_word, acronym_count[word])
            if acronym_count[new_word] >= 3:
                print(new_word, len(to_remove))
                to_remove.append(new_word)
            pass
        else:
            print(word, len(to_remove))
            to_remove.append(word)
    print(i, len(book))
    new_ahk_lines = []
    for line in ahk_lines:
        abbrev = line.split("::")[1]
        if abbrev in to_remove: continue
        new_ahk_lines.append(line + "\n")

    ff = open('AutoHotKey.ahk', 'w')
    for line in new_ahk_lines:
        ff.write(line)
    ff.close()