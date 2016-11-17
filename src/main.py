#!/usr/bin/env python3
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import argparse

from models import process_gedcom

if __name__ == "__main__":
    # Parse arguments and start processing of gedcom file
    
    parser = argparse.ArgumentParser(description='Manipulates GEDCOM information')
    # Onput and output .ged files
    parser.add_argument('input_gedcom', 
    			help="Name of the input GEDCOM file")
    parser.add_argument('output_gedcom',
                        help="Name of the output GEDCOM file; this file will be created/overwritten", 
                        nargs='?')
    parser.add_argument('--encoding', type=str, default="utf-8",
                        help="UTF-8, Latin-1 tai jokin muu")
    # Display options
    parser.add_argument('--list-html', type=str, default="",
                        help='Prints a list of changes in html')
    parser.add_argument('--display-changes', action='store_true',
                        help='Display changed places')
    parser.add_argument('--display-ignored', action='store_true',
                        help='Display ignored places')
    # Place processing args
    parser.add_argument('--reverse', action='store_true',
                        help='Reverse the order of places')
    parser.add_argument('--add-commas', action='store_true',
                        help='Replace spaces with commas')
    parser.add_argument('--ignore-lowercase', action='store_true',
                        help='Ignore lowercase words')
    parser.add_argument('--ignore-digits', action='store_true',
                        help='Ignore numeric words')
    parser.add_argument('--minlen', type=int, default=0,
                        help="Ignore words shorter that minlen")
    parser.add_argument('--auto-order', action='store_true',
                        help='Try to discover correct order...')
    parser.add_argument('--auto-combine', action='store_true',
                        help='Try to combine certain names...')
    parser.add_argument('--match', type=str,
                        help='Only process places containing this string')
    parser.add_argument('--parishfile', type=str,
                        help='File with a list of parishes', default="../data/seurakunnat.txt")
    parser.add_argument('--villagefile', type=str,
                        help='File with a list of villages', default="../data/kylat.txt")
    # Place processing args
    parser.add_argument('--indi-names', action='store_true',
                        help='Check and repair person names')

    args = parser.parse_args()
    if (args.reverse or args.add_commas or args.auto_order):
        print("*** Processing places")
        process_gedcom.init_places(args)

    if (args.indi_names):
        print("*** Processing person names")
    else:
        print("Nothing to do!")
        exit
    
    if (args.list_html):
        print("*** creating " + args.list_html)
        process_gedcom.init_html(args)

    process_gedcom.process_gedcom(args)
