#!/usr/bin/env python3
# 24.10.2016 Kari Kujansuu
# 26.10.2016 Juha Mäkeläinen sysout-tulostus
##

from views import html_out
from models import gedcom_places
from models import gedcom_names


def init_places(args):
        gedcom_places.read_parishes(args.parishfile)        
        gedcom_places.read_villages(args.villagefile)
        gedcom_places.test()


def process_gedcom(args):
    linenum = ""
    line = ""
    cnt_in = 0
    if args.output_gedcom:
        f = open(args.output_gedcom,"w",encoding=args.encoding)
    else:
        f = None
    try:
        for linenum, line \
                in enumerate(open(args.input_gedcom, encoding=args.encoding)):
            line = line.strip()
            tkns = line.split(None,2)
            cnt_in += 1
            if tkns[0] == '0':
                if len(tkns) < 3:
                    path = line
                else:
                    a = tkns[2].split(None,2)
                    path = "{} {}".format(tkns[0], a[0])
                #print ("Path: {!r} Line: {!r} ".format(path, line))
            
            if tkns[1] == "PLAC":
                newline = gedcom_places.process(args, tkns, cnt_in)
                if newline:
                    line = newline
            if (path == '0 INDI') & (tkns[1] == "NAME"):
                #print ("Name: {}".format(line))
                newline = gedcom_names.process(args, tkns, cnt_in)
                if newline:
                    line = newline

            if f:
                f.write(line + "\n")

    except (Exception) as e:
        print("*** Virhe rivillä {}: {}\n\t linenum='{}', line='{}'".
              format(str(e), str(linenum), line))
    finally:
        if f: 
            f.close()
        else: 
            if args.list_html: 
                html_out.close()
        print ("--- Total {} input lines".format(cnt_in))


def check(input, expected_output, reverse=False, add_commas=False,
          ignore_lowercase=False, ignore_digits=False):
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


