#!/usr/bin/env python3
# 24.10.2016 Kari Kujansuu
# 26.10.2016 Juha Mäkeläinen sysout-tulostus
##

from collections import defaultdict 
from views import html_out
import static.places

ignored = [name.strip() for name \
           in static.places.ignored_text.splitlines()
              if name.strip() != ""]


parishes = set()

villages = defaultdict(set)

def numeric(s):
    return s.replace(".","").isdigit()

def read_parishes(parishfile):
    for line in open(parishfile,encoding="utf-8"):
        line = line.strip()
        if line == "":
            continue
        num,name = line.split(None,1)
        for x in name.split("-"):
            name2 = x.strip().lower()
            parishes.add(auto_combine(name2))
         
def read_villages(villagefile):
    for line in open(villagefile,encoding="utf-8"):
        line = line.strip()
        if line == "":
            continue
        parish,village = line.split(":",1)
        parish = parish.strip().lower()
        village = village.strip().lower()
        villages[auto_combine(parish)].add(village)

def ignore_place(args,names):
    for name in names:
        if len(name) < args.minlen:
            return True
        if name.lower() in ignored:
            return True
        if args.ignore_digits and numeric(name):
            return True
        if args.ignore_lowercase and name.islower():
            return True
    return False

def auto_combine(place):
    for s in static.places.auto_combines:
        place = place.replace(s,s.replace(" ","-"))
    return place
    
def revert_auto_combine(place):
    for s in static.places.auto_combines:
        place = place.replace(s.replace(" ","-"),s)
    return place

def process_place(args,place):
    if args.match and place.find(args.match) < 0: return place
    if args.add_commas and "," not in place:
        if args.auto_combine:
            place = auto_combine(place)
        names = place.split()
        if ignore_place(args,names): 
            if args.auto_combine:
                place = revert_auto_combine(place)
            if args.display_ignored:
                print("ignored: " + place)
            return place
        place = ", ".join(names)
    if "," in place:
        names = [name.strip() \
                 for name in place.split(",") if name.strip() != ""]
        if len(names) == 1: 
            if args.auto_combine:
                place = revert_auto_combine(place)
            return place
        do_reverse = False
        if args.auto_order:
            #print(sorted(parishes))
            #print(sorted(villages["helsingin-pitäjä"]))
            #print(names)
            if names[0].lower() in parishes \
               and names[1].lower() in villages[names[0].lower()] \
               and names[-1] not in static.places.countries:
                do_reverse = True
            if names[0] in static.places.countries:
                do_reverse = True
        if args.reverse or do_reverse:
            names.reverse()
            place = ", ".join(names)
    if args.auto_combine:
        place = revert_auto_combine(place)
    return place
 
def process(args, tkns, incnt):
    # Here tkns[1] == "PLAC":
    if len(tkns) < 3:
        return ""
    place = tkns[2]
    newplace = process_place(args,place)
    if newplace != place: 
        if args.display_changes:
            print("{:>5}: PLAC '{:<40} -> '{}'".format(incnt, place + "'",newplace))
        tkns[2] = newplace  
        line = " ".join(tkns)
    else:
        line = ""
    if args.list_html:
        html_out.show_place_conv(place, newplace)
    return line

def check(input,expected_output,reverse=False,add_commas=False,ignore_lowercase=False,ignore_digits=False):
    class Args: pass
    args = Args()
    args.reverse = reverse
    args.add_commas = add_commas
    args.ignore_lowercase = ignore_lowercase
    args.ignore_digits = ignore_digits
    args.display_ignored = False
    args.display_ignored = False
    args.auto_order = True
    args.auto_combine = True
    args.minlen = 0
    args.match = None
 
    newplace = process_place(args,input)
    if newplace != expected_output:
        print("{}: expecting '{}', got '{}'".format(input,expected_output,newplace))
        #print(repr(parishes))
        xxx

def test():
    check("Helsingin pitäjä Herttoniemi","Herttoniemi, Helsingin pitäjä",add_commas=True,reverse=False)
    check("Rättölä, Heinjoki","Heinjoki, Rättölä",reverse=True)
    check("Rättölä Heinjoki","Rättölä, Heinjoki",add_commas=True)
    check("Rättölä Heinjoki","Heinjoki, Rättölä",add_commas=True,reverse=True)
    check("Rättölä, Heinjoki","Rättölä, Heinjoki",add_commas=True)
    check("Viipurin mlk","Viipurin mlk",add_commas=True)
    check("Viipurin msrk","Viipurin msrk",add_commas=True)
    check("Koski tl","Koski tl",add_commas=True)
    check("Koski TL","Koski TL",add_commas=True)
    check("Koski","Koski",add_commas=True)
    check("Koski","Koski",reverse=True)

    check("Koski förs","Koski, förs",add_commas=True,ignore_lowercase=False)
    check("Koski förs","Koski förs",add_commas=True,ignore_lowercase=True)

    #check("Rio de Janeiro","Rio, de, Janeiro",add_commas=True,ignore_lowercase=False)
    check("Rio de Janeiro","Rio de Janeiro",add_commas=True,ignore_lowercase=True)

    check("Stratford upon Avon","Stratford, upon, Avon",add_commas=True,ignore_lowercase=False)
    check("Stratford upon Avon","Stratford upon Avon",add_commas=True,ignore_lowercase=True)
    
    check("Äyräpää Vuosalmi N:o 4", "Äyräpää, Vuosalmi, N:o, 4",add_commas=True,ignore_digits=False)
    check("Äyräpää Vuosalmi N:o 4", "Äyräpää Vuosalmi N:o 4",add_commas=True,ignore_digits=True)


