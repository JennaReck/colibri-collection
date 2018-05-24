#Portable Google App Engine Command Line Rewriter
#Written by David Lambert (http://www.codepenguin.com)
 
#Rewrite the command line with correct paths
import sys, os, re
new_cmd = 'apppython.exe google_appengine/%s' % sys.argv[1]
gae_version = re.search('release: "(.*?)"',open('google_appengine/VERSION','r').read()).group(1)
appname = sys.argv[-1].rstrip('/').split('/')[-1]
if sys.argv[1] == 'dev_appserver.py' and os.path.exists(appname):
  new_cmd += ' --blobstore_path=google_appengine_datastores/%s_blobstore' % (appname)
  new_cmd += ' --datastore_path=google_appengine_datastores/%s_datastore' % (appname)
  new_cmd += ' --history_path=google_appengine_datastores/%s_history' % (appname)
  if gae_version >= "1.5.0":
    new_cmd += ' --skip_sdk_update_check'
    new_cmd += ' --rdbms_sqlite_path=google_appengine_datastores/%s_rdbms' % (appname)
new_cmd += " " + " ".join(sys.argv[2:])
#Write new command to the batch file
f = open('_cmdrewrite.bat','w')
f.write(new_cmd)
f.close()