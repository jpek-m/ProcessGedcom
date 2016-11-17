#!/usr/bin/env python3
# 24.10.2016 Kari Kujansuu
# 26.10.2016 Juha Mäkeläinen sysout-tulostus
##

f = None
seen = {}  # sisältää newplace:lukumäärä -pareja
orig = {}  # sisältää newplace:place -pareja
cnt_plac = 0
cnt_name = 0
cnt_total = 0

def init(args):
    global f
    if (args.list_html):
        #print ("*** Creating {}".format(args.list_html))
        f = open(args.list_html,"w")
    else:
        return

    f.write('<!DOCTYPE html>\n<html>\n<meta charset="UTF-8">\n<title>Nimimuunnokset</title>\n')
    f.write('''<style>
  td, th {border: 1px solid lightgray}
  th     {background-color: lightgray}
  td.num {text-align: right; color:gray}
  table  {border-style: solid; border-collapse: collapse}
</style>
''')
    f.write('<html>\n')

def close():
    global cnt_plac, cnt_name, cnt_total
    if f == None:
        return
    f.write('<body>\n<p>Käsiteltiin {} tietoa gedcomista. Löytyi {} eri nimeä ja {} paikkaa</p>\n'.
            format(cnt_total, cnt_name, cnt_plac))
    f.write('<table><tr><th>kpl</th><th>nimi</th><th>alkuperäinen</th></tr>\n')
    for place in sorted(seen.keys()):
        f.write('<tr><td class="num">{}</td>\n    <td>{}</td>\n    <td>{}</td></tr>\n'.
              format(seen[place], place, orig[place]))
    f.write('</table>\n</body>\n</html>\n')

def show_name_conv(name, newname = ""):
    global cnt_name, cnt_total
    if f == None:
        return
    key = "NAME " + newname
    cnt_total += 1
    if (key in seen):
        seen[key] += 1
    else:
        seen[key] = 1
        orig[key] = name
        cnt_name += 1

def show_place_conv(place, newplace = ""):
    global cnt_plac, cnt_total
    if f == None:
        return
    key = "PLACE " + newplace
    cnt_total += 1
    if (key in seen):
        seen[key] += 1
    else:
        seen[key] = 1
        orig[key] = place
        cnt_plac += 1
