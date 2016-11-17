# coding=UTF-8
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from views import html_out

NONAME = 'N'

def process_name(args, name):
    try:
        parts = name.split('/')
        givn, surn, spfx = parts
        if (givn):
            gnames = givn.split()
            l = len(gnames) - 1
            if (l > 0) & \
               ((gnames[l].endswith('poika') | (gnames[l].endswith('tytär')))):
                #print('# {} | {!r} | {!r}'.format(gnames, surn, spfx))
                spfx = gnames[l]
                gnames = gnames[:l]
                givn = ' '.join(gnames)
            else:
                givn = givn.rstrip()
        else:
            givn = NONAME

    except (Exception) as e:
        print("*** Virhe {}: {}".format(str(e), name))
        return name
    
    return (givn + ' /' + surn + '/ ' + spfx).rstrip()
 
def process(args, tkns, incnt):
    # Here tkns[1] == "NAME", tkns[2] is like 'Johan Johanpoika /Sihvola/'

    #print("{:>5}: {}".format(incnt, tkns))
    if len(tkns) < 3:
        return ""
    name = tkns[2]
    newname = process_name(args, name)
    if newname != name: 
        if args.display_changes:
            print("{:>5}: NAME '{:<40} -> '{}'".format(incnt, name + "'",newname))
        tkns[2] = newname  
        line = " ".join(tkns)
    else:
        line = ""
    if args.list_html:
        html_out.show_name_conv(name, newname)
    return line

#if __name__ == "__main__":
#    print("Hello World")
