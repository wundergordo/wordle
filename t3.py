#!/usr/bin/python3

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
    ret=textcolor(str,tc.bold, tc.fg_white, tx.bg_green)
    return ret

def text_wrong(str):
    ret=textcolor(str,tc.bold, tc.fg_black, tc.bg_white)
    return ret

def text_wrong_place(str):
    ret=textcolor(str,tc.bold, tc.fg_black, tc.bg_yellow)
    return ret

print(textcolor("fred", tc.normal, tc.fg_black, tc.bg_yellow))

