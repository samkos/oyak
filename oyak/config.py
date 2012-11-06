import getopt, sys, os


import exceptions, traceback


oyak_version = "0.5"

PORT = 8080
VISHNU_BUS = False
VISHNU_ADMIN = False
VISHNU_DEBUG = False
EDF = False
SERVER = False
DEBUG = False
TRACE = False
ARG_DEBUG = False
SSH_DEBUG = False
IHM_DEBUG = False
UNIX_DEBUG = False
GRAPHICS_DEBUG = False
FILE_DEBUG = False
SCHED_DEBUG = False
RESA_DEBUG = False
URL_DEBUG = False
DONE = True
FINGER = True
DUMP = False
USE_DUMP = False
DUMP_DEBUG = False
NOT_USE_DUMP_MACHINES = { "server" : '', "myserver": ''}
DJANGO_TRACE = False
AUTHENT_DEBUG = False
PORTAL_DEBUG = False
PROD = False


class MyError(Exception):
    """
    class reporting own exception message
    """
    def __init__(self, value):
        self.value  =  value
    def __str__(self):
        return repr(self.value)

def except_print():

    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    print "!!!!!!!!!!!!!!!!!!!!!!!!!"
    print exc_type
    print exc_value

    print "!!!!!!!!!!!!!!!!!!!!!!!!!"
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              file=sys.stderr)


def print_debug(s,r="nulll"):
  if debug:
    if r=="nulll":
      print s
    else:
      print s,":",r
      

#########################################################################
# welcome message
#########################################################################

def welcome_message():
    """ welcome message"""
    
    print """
                   #################################################
                   #                                               #
                   #      Welcome to Vishnu Web Portal 0.1 !       #
                   #                                               #
                   #################################################

                   
     """

#########################################################################
# usage ...
#########################################################################

def usage(message = None):
    """ helping message"""
    if message:
        print "  Error : %s \n" % message
    print "  usage: \n \t python server.py \
             \n\t\t[ --test] [ --test2] \
             \n\t\t[ --server] \
             \n\t\t[ --edf] \
             \n\t\t[ --vishnu       ] [ --vishnu_admin ] [ --vishnu_debug ] \
             \n\t\t[ --trace        ] [ --nofinger     ] \
             \n\t\t[ --dump         ] [--use_dump      ]\
             \n\t\t[ --debug        ] [ --resa_debug   ] [ --unix_debug  ] \
             \n\t\t[ --ihm_debug    ] [ --sched_debug  ] [ --dump_debug  ]  \
             \n\t\t[ --url_debug    ] [ --arg_debug    ] [ --ssh_debug   ]   \
             \n\t\t[ --django_debug ] |--graph_debug   ] [ --file_debug  ] \
             \n\t\t[ --authent_debug] [ --portal_debug ] [ --prod ] \
           \n"  

    sys.exit(1)

#########################################################################
# command line parsing...
#########################################################################

def parse(args=sys.argv[1:]):
    """ parse the command line and set global _flags according to it """

    global PORT,VISHNU_BUS,EDF,SERVER,DEBUG,TRACE,ARG_DEBUG,SSH_DEBUG,IHM_DEBUG,\
        UNIX_DEBUG,GRAPHICS_DEBUG,FILE_DEBUG,SCHED_DEBUG,RESA_DEBUG,URL_DEBUG,DONE,\
        FINGER,DUMP,USE_DUMP,DUMP_DEBUG,NOT_USE_DUMP_MACHINES,DJANGO_TRACE,VISHNU_ADMIN,\
        VISHNU_DEBUG, AUTHENT_DEBUG, PORTAL_DEBUG, PROD
    #print "parsing vishnu parameter : ",args
    try:
        opts, args = getopt.getopt(args, "h", 
                          ["help","python", "edf", "server", "vishnu", "vishnu_admin", "vishnu_debug",
                           "test", "test2",
                           "trace",
                           "debug","nofinger","dump","use_dump","dump_debug",
                           "ihm_debug","sched_debug","resa_debug","unix_debug",
                           "url_debug","arg_debug","ssh_debug","graph_debug","file_debug",
                           "django_debug", "authent_debug", "portal_debug","prod"])
    except getopt.GetoptError, err:
        # print help information and exit:
        usage(err)

    # first scan opf option to get prioritary one first
    # those who sets the state of the process
    # especially those only setting flags are expected here
    for option, argument in opts:
        if option in ("-h", "--help"):
            usage("")
        elif option in ("--trace"):
            TRACE = True
        elif option in ("--debug"):
            DEBUG = True
        elif option in ("--dump"):
            DUMP = True
        elif option in ("--dump_debug"):
            DUMP_DEBUG = True
        elif option in ("--use_dump"):
            USE_DUMP = True
            NOT_USE_DUMP_MACHINES = { "server" : '', "myserver": ''}
        elif option in ("--nofinger"):
            FINGER = False
        elif option in ("--ihm_debug"):
            IHM_DEBUG = True
        elif option in ("--ssh_debug"):
            SSH_DEBUG = True
        elif option in ("--arg_debug"):
            ARG_DEBUG = True
        elif option in ("--sched_debug"):
            SCHED_DEBUG = True
        elif option in ("--resa_debug"):
            RESA_DEBUG = True
        elif option in ("--url_debug"):
            URL_DEBUG = True
        elif option in ("--unix_debug"):
            UNIX_DEBUG = True
        elif option in ("--graph_debug"):
            GRAPHICS_DEBUG = True
        elif option in ("--file_debug"):
            FILE_DEBUG = True
        elif option in ("--django_debug"):
            DJANGO_DEBUG = True
        elif option in ("--authent_debug"):
            AUTHENT_DEBUG = True
        elif option in ("--portal_debug"):
            PORTAL_DEBUG = True
        elif option in ("--prod"):
            PROD = True
        elif option in ("--vishnu"):
            VISHNU_BUS = True
        elif option in ("--vishnu_debug"):
            VISHNU_DEBUG = True
        elif option in ("--vishnu_admin"):
            VISHNU_BUS = True
            VISHNU_ADMIN = True
        elif option in ("--server"):
            SERVER = True
        elif option in ("--edf"):
            EDF = True
        elif option in ("--test"):
            PORT = 8888
        elif option in ("--test2"):
            PORT = 7777


if VISHNU_BUS:
    HOME = os.environ['HOME']
    vishnu_directory = os.path.abspath(HOME)+"/local20/lib"
    sys.path.append(vishnu_directory)
    vishnu_directory = os.path.abspath(HOME)+"/local20/vishnu/2.0/lib"
    sys.path.append(vishnu_directory)
    vishnu_directory = os.path.abspath(HOME)+"/local20/vishnu/2.0/lib/swig_output"
    sys.path.append(vishnu_directory)




sendCartouche = False 

Handler = None      


def print_debug(s,r="nulll"):
  if debug:
    if r=="nulll":
      print s
    else:
      print s,":",r
      
import os,sys
ROOT_PATH = os.path.dirname(__file__)

import sqlite3
conn = sqlite3.connect('%s/db.sqlite' % ROOT_PATH)
conn.row_factory = sqlite3.Row                # acces facile aux colonnes

OYAK_DIR = "/tmp"
