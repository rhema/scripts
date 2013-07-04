from bottle import route, run, template
import time

"""
So a person starts at /start, enters the name of a pinterest user, and then magic should happen...
"""

start_page = """
<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js" type="text/javascript"></script>

  <body>
  <h3>Please enter your pinterest username below...</h3>
  </body>
  <div id="inputs">
  <input id="username"/>
  <input type="button" onclick="submitme()" value="OK"/>
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
       $("#inputs").html("This may take up to 30 seconds.</br><img src='http://i.imgur.com/WfwMbhu.gif'/>");
       setTimeout(do_change,100);
     }
  </script>
</html>
"""

@route('/')
def index(name='World'):
    return start_page

@route('/scrub/<name>')
def index(name='World'):
    time.sleep(10)
    return template('<b>Thanks! {{name}}</b>!', name=name)

run(host='localhost', port=8080)