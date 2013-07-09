from bottle import route, run, template
import subprocess
import time
import random
import os
from bottle import error

save_location = "pinboards/"

import string
d = dict.fromkeys(string.ascii_lowercase, 0)

def get_hash(long=5):
    ret = ""
    for i in range(0,long):
        ret += d.keys()[int(random.random()*26)]
    return ret

"""
So a person starts at /start, enters the name of a pinterest user, and then magic should happen...

phantomjs should either be in this folder or in /usr/local/bin


"""

start_page = """
<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" type="text/javascript"></script>

  <body>
  <h3>Please enter your Pinterest username below:</h3>
  </body>
  <div id="inputs">
  <input id="username" onkeydown="if (event.keyCode == 13) document.getElementById('okbutton').click()" />
  <input id="okbutton" type="button" onclick="submitme()" value="OK"/>
  </div>
  
  
  <script>
  var username = "";
  
     function do_change()
     {
       document.location = "/scrub/"+username;
     }
     function submitme()
     {
       console.log("click");
       username = $("#username").val();
       $("#inputs").html("This may take up to 30 seconds.</br><img height='100px' width='100px' src='http://i.imgur.com/WfwMbhu.gif'/>");
       setTimeout(do_change,100);
     }
  </script>
</html>
"""

fail_page = """
<html>
  <body>
  <h3>Opps! That didn't work.  Please check your username and <a href="/">try again</a>.</h3>
  </body>
</html>
"""

@route('/')
def index(name='World'):
    return start_page

@error(404)
def error404(error):
    return fail_page

@route('/scrub/<name>')
def index(name='World'):
    v = ["/usr/local/bin/phantomjs", "getboards.js", "http://pinterest.com/"+name, "temp.pdf", "12in*8in"]
    #v = ["/usr/local/bin/phantomjs", "scrubscreen.js", "http://pinterest.com/"+name, "temp.pdf", "12in*8in", "&"]
    #v = ["/Users/rhema/Documents/aptana_workspace/scripts/pinterest/bottle/derp.sh","one","two","three"]
    #print v
    #subprocess.Popen(v,shell=True)
    ####proc = subprocess.Popen(v, shell=True,stdout=subprocess.PIPE)#call " ".join(v)
    proc = subprocess.Popen(" ".join(v), shell=True,stdout=subprocess.PIPE)#call " ".join(v)
    output = proc.stdout.read()
    #print "WHERE IS YOU LOG NOW!!!",output
    hash = get_hash()
    os.mkdir(save_location+hash)
    current_folder = save_location+hash+"/"
    current_file = current_folder+"all.pdf"
    
    v = ["/usr/local/bin/phantomjs", "scrubscreen.js", "http://pinterest.com/"+name, current_file, "12in*8in"]#, "&"]
    subprocess.call(" ".join(v), shell=True)
    if output == "" or "Usage:" in output:
        return fail_page
    print "BOARDS--->",output
    for b in output.split("\n"):
        if len(b) == 0:
            continue
        current_file =  current_folder+b+".pdf"
        v = ["/usr/local/bin/phantomjs", "scrubscreen.js", "http://pinterest.com/"+name+"/"+b, current_file, "12in*8in", "&"]
        subprocess.call(" ".join(v), shell=True)
#        
    #subprocess.Popen(v, shell=True, close_fds=False)
#    time.sleep(1)
    return template('<h3>It worked!</h3>Please scroll down and enter this into the box: <h3>{{hash}}</h3>', hash=hash)

run(host='localhost', port=12001)