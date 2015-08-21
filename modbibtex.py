#! /usr/bin/env python

import os, sys
from os import path


def get_options():
    import os, os.path
    from optparse import OptionParser
 
    usage = "usage: %prog [options] \n"
    parser = OptionParser(usage=usage)


    parser.add_option("-p","--path", dest="bib_path", type="string", default="./", help="path of bibtex files to be modified")
    parser.add_option("-n","--modpath", dest="modpath", type="string", default="./newbib/", help="path of bibtex files to be modified")
    parser.add_option("-a","--abbrev", dest="abbrev", default=False,action="store_true", help="Set full journal titles to variables and create a text file setting these variables to abbreviations  ")
    parser.add_option("--delnotes", dest="delnotes", default=False,action="store_true", help="Delete note lines ")
    parser.add_option("--abbrev_ref", dest="abbrev_ref", type="string", default="abbrev.text", help="Text file of abbreviations of journals and full text of journals")

    (options, args) = parser.parse_args()
    return options, args


def main():
    """
    Read in bibtex files and modify tags  
    """
    dlim = "--------------------------------------------------------------------------------"
    #        
    # Read options 
    #
    options, args = get_options()

    # Read in all files in bib_path directory 
    files = [f for f in os.listdir(options.bib_path) if path.isfile(f)]

    if( not os.path.isdir(options.modpath) ):
        log_line = "New bib path %s not found will attempt to make dir "%(options.modpath)
        print log_line
        os.mkdir(options.modpath)

    if( os.path.isdir(options.modpath) ):
        log_line = dlim+"\n"
        log_line += "New bib files will be printed in %s \n"%(options.modpath)
        log_line += dlim+"\n"
        print log_line
    else:
        error_line = "New bib file path not found %s "%(options.modpath)
        sys.exit(error_line)
        
    if( options.abbrev ):
        try:
            with open(options.abbrev_ref,'r') as F:
                abb_lines = F.readlines()
                F.close()
        except IOError:
            error_line = " Text file of abbreviations of journals and full text of journals %s not found"%(options.abbrev_ref)
            sys.exit(error_line)

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
    unknown_line = ""
    rmstr = ["The ","{","}",',',"\"","\\","\\n"]

    # Set write new files to true 
    w_new = True

    # Loop over bib files 
    for f in files:
        col = f.split(".")
        if( col[1] == "bib" ):
            # If .bib open file 
            F = open(f,'r')
            bib_lines = F.readlines()
            F.close
            if( w_new ):
                Fwvar = open("%s/%s"%(options.modpath,f),"w")
            new_bib = ""
            for l in bib_lines:
                l_col = l.split()
                new_line = True 
                if( len(l_col) ):
                    if(  options.abbrev ):

                        if( l_col[0] == "journal" or  l_col[0] == "Journal"  or  l_col[0] == "JOURNAL"  ):
                            j_name =  ""
                            for c in l_col[2:] :
                                j_name += ("%s ")%c
                            # Remove  commas, parentheses, etc. from name
                            for rmstr_i in rmstr:
                                j_name  = j_name.replace(rmstr_i,"")
                            j_name = j_name.lstrip(' ').rstrip()
                            index_good = True
                            # Find name in reference    
                            try:
                                i = name_list.index(j_name)
                            except:
                                try:
                                    i = abb_list.index(j_name)
                                except:
                                    index_good = False 
                                    unknown_line +=  "Journal name |%s| not found in bibtex file %s \n"%(j_name,f)
                                    print error_line
                                    #sys.exit("adsfa")
                                else:
                                    index_good = True 
                            if( index_good ):
                                full_jname =  name_list[i]
                                j_var = full_jname.replace(" ","")
                                j_var = j_var.replace(":","")
                                j_var = j_var.replace("(","")
                                j_var = j_var.replace(")","")
                                # Store abbreviation and full name as new variables 
                                long_lines += "@string{%s=\"%s\" \n"%(j_var,full_jname)
                                short_lines += "@string{%s=\"%s\"} \n"%(j_var,abb_list[i])
                                # Set journal tag to variable name 
                                var_line = "journal = %s , \n"%(j_var)
                                new_var_lines += var_line
                                #var_bib_lines = bib_lines.replace(l,var_line)
                                new_line = False
                                new_bib += var_line
                                if( w_new ):
                                    Fwvar.write(var_line)

                    if(  options.delnotes ):
                        if( l_col[0] == "note" ):
                            new_line = False
                if(new_line):
                    new_bib += l
                    if( w_new ): Fwvar.write(l)

            if( w_new ): Fwvar.close()
            #print "new_bib",new_bib

# Write variable names with journal titles abbreviated
    F = open("%s/abb.text"%(options.modpath),"w")
    F.write(short_lines)
    F.close()
    log_line = dlim+"\n"
    log_line += " Abbreviated title variables writen to %s \n"%("%sabb.text"%(options.modpath))
    log_line += dlim+"\n"
    print log_line


# Write variable names with full journal titles  
    F = open("%s/full.text"%(options.modpath),"w")
    F.write(long_lines)
    F.close() 
    log_line = dlim+"\n"
    log_line += " Full title variables writen to %s \n"%("%sfull.text"%(options.modpath))
    log_line += dlim+"\n"
    print log_line

    if( len(unknown_line) > 0 ):

        log_line = dlim+"\n"
        log_line += "Journal titles that were not found in %s : \n"%(options.abbrev_ref)
        print unknown_line+"\n"
        log_line += dlim+"\n"
        print log_line
    else:
        log_line = "All Journal titles found \n"
        print log_line
        
        
    
if __name__=="__main__":
    main()
    
