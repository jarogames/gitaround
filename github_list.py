#!/usr/bin/env python3
# pip install  PyGithub
from contextlib import contextmanager
from github import Github
import os
import getpass

################  CD from http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
#    print('>... from',prevdir,'entering',newdir)
    print('>... entering',newdir)
    try:
        yield
    finally:
        print('<... going back to ',prevdir)
        os.chdir(prevdir)


        

#exit(0)
#user='jaromrax'
user=input("Please enter github USER: ")
print("Please enter github password: ")
var=getpass.getpass()

# First create a Github instance:
g=Github( user , var)


####### create ALL
if not os.path.exists( 'ALL' ):
    os.makedirs( 'ALL' )

# Then play with your Github objects:
for repo in g.get_user().get_repos():
#    reponame='20160825_2nd_notebook_test'
    reponame=repo.name
    repopath='ALL/'+reponame+'/'
    print('==============', reponame, '===================')
    if not os.path.exists( repopath ):
        #os.makedirs( reponame )
        CMD='git clone git@github.com:'+user+'/'+reponame+'.git '+repopath
        print('i...   ',CMD)
        if (os.system(CMD) !=0):
            print('error with ', CMD)
            exit(1)
    ######## I read tags -  one line one tag, space sep.            
    FNAME=repopath+'.tags'
    print('trying',FNAME )
    try:
        fi=open(FNAME)
        print('opened',FNAME )
    except IOError:
        print('!... no{'+FNAME+'}found')
        continue
    for line in fi:
        if ( len(line.strip() )<1 ):
            break
        newdir=line.split()[0].strip()
        if ( len(newdir)<1 ):
            break
        newsub=line.split()[1].strip()
        if ( len(newsub)<1 ):
            break
        print('o... pair:',newdir,newsub )
        if not os.path.exists( newdir ):
            os.makedirs( newdir )
        print('i... going to SYMLINK')
        if not os.path.exists( newdir+'/'+newsub ):
            CMD='mkdir -p '+newdir+'/'+newsub
            os.system(CMD)
        with cd(newdir+'/'+newsub):
            print(  'T... ln -s ../../ALL/'+reponame+'/' ,  reponame )
            try:
                os.symlink(   '../../ALL/'+reponame+'/' , reponame )
            except:
                print("-... symlink canot be created")
                #                   print(  'T... ln -s  ', newsub,  'ALL/'+reponame+'/'  )
                   #os.symlink( 'ALL/'+reponame+'/' ,         NEWPATH )
#                   os.symlink(   '../ALL/'+reponame+'/' , newsub )



