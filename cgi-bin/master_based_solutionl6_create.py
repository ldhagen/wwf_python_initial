#!/usr/bin/env python

import sys, pickle, ldh6_test as l6


def  main(pkl_file,filename,letters):
    ifile = open(pkl_file,'r')
    master_dict = pickle.load(ifile)
    ifile.close()
    xxx = master_dict[filename]
    aaa = l6.CompleteSet(xxx,l6.yyy,letters)
    aaa.dump_valid_solutions('sd.txt')
    aaa.print_top_scores_in_order()
    aaa.dump_top_scores_in_order()

if __name__ == '__main__':
    pkl_file = sys.argv[1]
    filename = sys.argv[2]
    letters = sys.argv[3]
    main(pkl_file,filename,letters)
