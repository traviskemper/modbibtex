#! /usr/bin/env python

import os, sys
from os import path

# Read in all files in current directory 
files = [f for f in os.listdir("./") if path.isfile(f)]
j_cnt = 0

# Open reference files of journal abbreviations
F = open("abbrev.text",'r')
abb_lines = F.readlines()
F.close

abb_list =[]
name_list =[]
for l in abb_lines:
    l_col = l.split(" ; ")
    if( len(l_col) >= 2 ):
        j_abb = str(l_col[0] ).lstrip(' ').rstrip()
        abb_list.append( j_abb)
        j_name = str(l_col[1] ).lstrip(' ').rstrip()
        name_list.append(j_name)

# Initialize strings to be appended 
long_lines =""        
short_lines =""
new_var_lines = ""
rmstr = ["The ","{","}",',',"\"","\\","\\n"]

w_new = True

# Loop over bib files 
for f in files:
    col = f.split(".")
    if( col[1] == "bib" ):
        F = open(f,'r')
        bib_lines = F.readlines()
        F.close
        if( w_new ):
            Fwvar = open("../bibfilesv2/%s"%(f),"w")
        new_bib = ""
        for l in bib_lines:
            l_col = l.split()
            new_line = True 
            if( len(l_col) ):
                if( l_col[0] == "journal" or  l_col[0] == "Journal"  or  l_col[0] == "JOURNAL"  ):
                    j_cnt +=1
                    j_name =  ""
                    for c in l_col[2:] :
                        j_name += ("%s ")%c
                    for rmstr_i in rmstr:
                        j_name  = j_name.replace(rmstr_i,"")
                    j_name = j_name.lstrip(' ').rstrip()
                    index_good = True  
                    try:
                        i = name_list.index(j_name)
                    except:
                        try:
                            i = abb_list.index(j_name)
                        except:
                            index_good = False 
                            print "      emacs %s      &  "%(f)
                            print  "|%s| Not found "%(j_name)
                            sys.exit("adsfa")
                        else:
                            index_good = True 
                    if( index_good ):
                        full_jname =  name_list[i]
                        j_var = full_jname.replace(" ","")
                        j_var = j_var.replace(":","")
                        j_var = j_var.replace("(","")
                        j_var = j_var.replace(")","")
                        long_lines += "@string{%s=\"%s\" \n"%(j_var,full_jname)
                        short_lines += "@string{%s=\"%s\"} \n"%(j_var,abb_list[i])
                        var_line = "journal = %s , \n"%(j_var)
                        new_var_lines += var_line
                        #var_bib_lines = bib_lines.replace(l,var_line)
                        new_line = False
                        new_bib += var_line
                        if( w_new ): Fwvar.write(var_line)
                        
                if( l_col[0] == "note" ):
                    new_line = False
            if(new_line):
                new_bib += l
                if( w_new ): Fwvar.write(l)
                
        if( w_new ): Fwvar.close()
        #print "new_bib",new_bib
        
print " Long "
print "---------------------"
print long_lines
print " Short "
print "---------------------"
print short_lines
print " New journal lines  "
print "---------------------"
print new_var_lines

# Write variable names with journal titles abbreviated 
F = open("short.bib","w")
F.write(short_lines)
F.close()

# Write variable names with full journal titles  
F = open("long.bib","w")
F.write(long_lines)
F.close()
