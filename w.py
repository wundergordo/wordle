#!/usr/bin/python3
import sys
import string
import random

class letterClass:
    def __init__(self, c):
        #c is the letter
        self.c = c
        self.checked = False
        self.not_in_word = False
        self.correct_pos = []
        self.incorrect_pos = []

    def add_correct(self, p):
        #append position p to incorrect position list
        #don't duplicate
        found=False
        for el in self.correct_pos:
            if el == p:
                found=True
                break
        if (found==False):
            self.correct_pos.append(p)


    def add_incorrect(self, p):
        #append position p to incorrect position list
        #don't duplicate
        found=False
        for el in self.incorrect_pos:
            if el == p:
                found=True
                break
        if (found==False):
            self.incorrect_pos.append(p)

    def print(self):
        print(self.c, end=" ")
        if(self.checked != False):
            print("* ", end='')
        else:
            print("  ", end='')
        if(self.not_in_word != False):
            print("* ", end='')
        else:
            print("  ", end='')
        print("cp=[", end='')
        for cp  in self.correct_pos :
            print(' ', cp, end='')
        print("] ip=[", end='')
        for ip in self.incorrect_pos :
            print(' ', ip, end='')
        print("]")





class alphabetClass:
    def __init__(self):
        self.a = []
        for c in string.ascii_lowercase:
            self.a.append(letterClass(c))

    def print(self):
        i=0
        for el in self.a:
            print("{:2d}".format(i), end=' ')
            el.print()
            i+=1



class tc:
    normal = 0
    bold = 1
    ligt = 2
    italicized = 3
    underline = 4
    blink = 5
    fg_black = 30
    fg_red = 31
    fg_green = 32
    fg_yellow = 33
    fg_blue = 34
    fg_purple = 35
    fg_cyan = 36
    fg_white = 37

    bg_black = 40
    bg_red = 41
    bg_green = 42
    bg_yellow = 43
    bg_blue = 44
    bg_purple = 45
    bg_cyan = 46
    bg_white = 47

def textcolor(str, style, fg, bg):
    ret = "\033[{:d};{:d};{:d}m{:s}\033[0;0m".format(style, fg, bg, str)
    #ret = "\033[{:d}\-33[0;0m".format(style)
    return ret

def text_correct(str):
    ret=textcolor(str,tc.bold, tc.fg_white, tc.bg_green)
    return ret

def text_wrong(str):
    ret=textcolor(str,tc.bold, tc.fg_black, tc.bg_white)
    return ret

def text_wrong_place(str):
    ret=textcolor(str,tc.bold, tc.fg_black, tc.bg_yellow)
    return ret

def textformat(str, result):
    #result format
    # "nf" means letter not found, "np" found but not correct position, "cp" found in correct position
    if(result == "nf"):
        return text_wrong(str)
    if(result == "cp"):
        return text_correct(str)
    if(result == "np"):
        return text_wrong_place(str)
    print("textformat error")
    print(str)
    print(result)
    exit()


def checkletter(w,l):
    for i in range(len(w)):
        if(w[i] == l):
            return True
    return False

def checkword(w, il, ol):
    # check out letters
    for letter in ol:
        if(checkletter(w, letter)):
            return False
    for letter in il:
        if(checkletter(w, letter)==False):
            return False
    return True

def getcanwords(wl, il, ol):
    ret=[]
    for el in wl:
        if(checkword(el, il, ol)):
            ret.append(el)
    return ret

def checkword_al(w, al):
    #w is word to check
    #al is current alphabet
    #return True is word not eleminated by current alphabet

    #generate in list and out list
    il=[]
    ol=[]
    for el in al.a:
        if el.checked :
            if el.not_in_word :
                if checkletter(w, el.c)==True:
                    # word has letter that is not in the target word eleminate word
                    # from possible word list
                    # There is an issue if a letter is repeated
                    if(len(el.correct_pos)!=0 or len(el.incorrect_pos)!=0):
                        pass
                    else:
                        return False
            else:
                #letter is in target word
                if checkletter(w, el.c) == False :
                    # word is missing letter that should be in word
                    #eleminate word for possible word list
                    return False
                #check correct position
                for cp in el.correct_pos:
                    word_letter=w[cp]
                    if word_letter != el.c:
                        #letter at position cp is not el.c so word should be eleminated
                        return False

                #check letter found but we don't know the position
                for lp in el.incorrect_pos:
                    word_letter=w[lp]
                    if(word_letter == el.c):
                        #letter found in position that has been listed that it cannot be
                        return False
    return True

def prune_list(wl, al):
    #return the list of words from wl that are still possible given al alphebet
    rl=[]
    for word in wl:
        cw=checkword_al(word, al)
        if cw == True:
            rl.append(word)
    return rl





def loaddict(wl, list_file_name="/usr/share/dict/words"):
    #wl is word length
    wordlist=[]
    with open(list_file_name) as f:
        for l in f:
            w=l.split()
            if(len(w[0])==wl):
                if(w[0][0].islower()): # skip names
                    if(checkletter(w[0],"'")==False): #skip punctuation
                        wordlist.append(w[0])
    return wordlist

def usage(ex=True):
    print("w.py <letters in word> <letters not in word> n l n l")
    print("n l is letter position and letter")
    if(ex):
        exit(-1)


def parseargs(argv):
    print("length", len(argv))
    if(len(argv) < 3):
        usage()
    if((len(argv) % 2) == 0):
        print("wrong number of position arguments")
        usage()
    inletters=sys.argv[1]
    outletters=sys.argv[2]
    lpd = {}
    for i in range(3, len(argv), 2):
        lp = int(argv[i])
        ll = argv[i+1]
        lpd[lp] = ll
    print(lpd)
    return(inletters, outletters, lpd)

def wordresults(guess, results):
    gl=len(guess)
    rl=len(results)
    if(gl != rl):
        print("length mismatch wordresults")
    str=""
    for i in range(gl):
        str += textformat(guess[i], results[i])
    return str


def report_word(word, guess):
    #word is the word you are trying to guess
    #guess is the guess word

    gl=len(guess)
    wl=len(word)
    ret=[] # "nf" means letter not found, "np" found but not correct position, "cp" found in correct position
    for i in range(gl):
        gc=guess[i]
        ret.append("nf")
        for j in range(wl):
            if guess[i] == word[j]:
                if(i==j):
                    ret[i] = "cp"
                    break
                else:
                    ret[i] = "np"
    return ret

def guess_word(word, guess, alphabet):
    rp = report_word(word, guess)
    str= wordresults(guess, rp)
    #print("guess_word")
    #print(str)
    for i in range(len(word)):
        gc=guess[i]
        for el in alphabet.a:
            if gc==el.c:
                el.checked = True
                if rp[i] == "nf":
                    el.not_in_word = True
                if rp[i] == "np":
                    el.add_incorrect(i)
                if rp[i] == "cp":
                    el.add_correct(i)
    return str

def solve(word, wl):
    #print("entering solve for ", word)
    al=alphabetClass()
    done=False
    pl=prune_list(wl,al)
    total_guess = 0
    while(not done):
        total_guess += 1
        gl = len(pl)
        guess=pl[random.randint(0,gl-1)]
        str=guess_word(word, guess, al)
        pl=prune_list(pl,al)
        gl = len(pl)
        #print(total_guess, str, "possible words ", gl)
        if(guess == word):
            break
    return total_guess



def hist(word, wl):
    hist=[]
    for i in range(20):
        hist.append(0)
    for i in range(1000):
        s=solve(word,wl)
        hist[s]+=1
    for i in range(len(hist)):
        print(i, hist[i])

def solve2(word, wl):
    print("solve for", word)
    al=alphabetClass()
    if word=="usage":
        return 1
    if word=="chino":
        return 2
    if word=="grump":
        return 2
    str=guess_word(word,"alter", al)
    print(1, str, "possible words ")
    str=guess_word(word,"chino", al)
    print(2, str, "possible words ")
    str=guess_word(word,"musky", al)
    print(3, str, "possible words ")

    total_guess = 3
    pl=prune_list(wl,al)
    while(True):
        total_guess += 1
        gl=len(pl)
        guess=pl[random.randint(0,gl-1)]
        str=guess_word(word, guess, al)
        pl=prune_list(pl,al)
        gl = len(pl)
        print(total_guess, str, "possible words ", gl)
        if(guess == word):
            break
    return total_guess

def hist2(wl):
    l=len(wl)
    hist=[]
    N=1000
    for i in range(20):
        hist.append(0)
    for i in range(N):
        word=wl[random.randint(0,l-1)]
        s=solve2(word, wl)
        print(s)
        hist[s] += 1
    total=0
    for i in range(len(hist)):
        total+=i*hist[i]
        print(i, hist[i])
    print("total=",total, "average=", total/N)



def parse_input(str):
    x=str.split()
    print(x)
    if (len(x) != 2):
        print("did not have 2 5 letter groups in input")
        print("input must be 5 letter word followed by 5 chrater result")
        return False
    word=x[0]
    if (len(word)!=5):
        print("guess word not 5 letters")
        return False
    r=x[1]
    if (len(r)!=5):
        print("result string not 5 charaters")
        return False
    result=[]
    for el in r:
        if el == 'n':
            result.append("nf")
        elif el == 'c':
            result.append("cp")
        elif el == 'g':
            result.append("np")
        else:
            print("bad character in result")
            return False
    return [word, result]


def prune_alphabet(alphabet, guess, rp):
    #print("prune", guess, len(guess))
    for i in range(len(guess)):
        gc=guess[i]
        #print(i,gc)
        for el in alphabet.a:
            if gc==el.c:
                el.checked = True
                if rp[i] == "nf":
                    el.not_in_word = True
                if rp[i] == "np":
                    el.add_incorrect(i)
                if rp[i] == "cp":
                    el.add_correct(i)

def words_try(pl):
    l=len(pl)
    print(l, "possible words")

    if l > 200 :
        for i in range(10):
            print(pl[random.randint(0,l-1)], end=' ')
    else:
        for i in range(l):
            print(pl[i], end=' ')
    print()

def wordle_help(wl):
    al=alphabetClass()
    pl=prune_list(wl,al)
    total_guess = 0
    print("begining solve")
    print("enter guess word folled by result")
    print("result is n for not correct c for totally correct g for in word but not correct position")
    print("example input")
    print("chino nncgn")
    str=wordresults("chino", ["nf", "nf", "cp", "np", "nf"])
    print("string from wordle", str)

    print("good words for first try alert")
    print("good word for second try chino")

    while(True):
        total_guess += 1
        print("enter guess word followed by result")
        ins=input()
        x=parse_input(ins)
        if x != False :
            print("check")
            guess=x[0]
            result = x[1]
            #print("guess", guess, result)
            prune_alphabet(al, guess, result)
            #al.print()
            pl=prune_list(pl,al)
            words_try(pl)





if __name__ == "__main__":
    [inletters, outletters, lpd] = parseargs(sys.argv)

    print("in letters", inletters)
    print("out letters", outletters)
    words=loaddict(5)
    canw=getcanwords(words, inletters, outletters)
    for el in canw:
        print(el)

