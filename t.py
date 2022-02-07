#!/usr/bin/python3

from w import *

if __name__ == "__main__":
    x=alphabetClass()
    #wl=loaddict(5, "/home/dan/code/wordlist/words/20k.txt")
    wl=loaddict(5)
    hist2(wl)
    exit()
    x.a[0].checked = True
    x.a[0].not_in_word = True
    wordle_help(wl)
    exit()
    #print("length of word list before", len(wl))
    #pl=prune_list(wl,x)
    #print("length of word list after empty prune", len(pl))

    hist("skill", wl)
    exit()

    guess("skill", "alert", x)
    pl=prune_list(wl,x)
    print("length of word list after one word", len(pl))
    guess("skill", "chino", x)
    pl=prune_list(wl,x)
    print("length of word list after two words", len(pl))
    print(pl)
    x.print()

    exit()
    guess("swill","alert", x)
    x.print()
    exit()
    wl=loaddict(5, "/home/dan/code/wordlist/words/20k.txt")
    print("length =", len(wl))
    wl2=loaddict(5,)
    print("length2 =", len(wl2))
    rp=report_word("aloft", "alert")
    print(rp)
    print(wordresults("alert", rp))
    rp=report_word("aloft", "chino")
    print(rp)
    print(wordresults("chino", rp))

    exit()
    #[inletters, outletters, lpd] = parseargs(sys.argv)

    print("in letters", inletters)
    print("out letters", outletters)
    words=loaddict(5)
    canw=getcanwords(words, inletters, outletters)
    for el in canw:
        print(el)
