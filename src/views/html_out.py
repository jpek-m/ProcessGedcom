#!/usr/bin/env python3
# 24.10.2016 Kari Kujansuu
# 26.10.2016 Juha Mäkeläinen sysout-tulostus
##

started = False
seen = {}  # sisältää newplace:lukumäärä -pareja
orig = {}  # sisältää newplace:place -pareja

def init():
    global started

    print('<!DOCTYPE html>\n<html>\n<meta charset="UTF-8">\n<title>Nimimuunnokset</title>')
    print('''<style>
  td, th {border: 1px solid lightgray}
  th     {background-color: lightgray}
  td.num {text-align: right; color:gray}
  table  {border-style: solid; border-collapse: collapse}
</style>''')
    print('<html>\n<body>\n<table><tr><th>kpl</th><th>paikka</th><th>alkuperäinen</th></tr>')
    started = True

def close():
    global started

    for place in sorted(seen.keys()):
        print('<tr><td class="num">{}</td>\n    <td>{}</td>\n    <td>{}</td></tr>'.
              format(seen[place], place, orig[place]))
    print('</table>\n</body>\n<html>')


def show_place_conv(place, newplace = ""):
    global started

    if not started:
        init()

    if (newplace in seen):
        seen[newplace] += 1
    else:
        seen[newplace] = 1
        orig[newplace] = place
