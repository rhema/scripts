var port, server, service,
    system = require('system');

if (system.args.length !== 2) {
    console.log('Usage: simpleserver.js <portnumber>');
    phantom.exit(1);
} else {
    port = system.args[1];
    server = require('webserver').create();

    service = server.listen(port, function (request, response) {

        console.log('Request at ' + new Date());
        console.log(JSON.stringify(request, null, 4));
        response.statusCode = 200;
        response.headers = {
            'Cache': 'no-cache',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': '1000',
            'Access-Control-Allow-Headers': '*'
        };
        
        
        
        var url = request.url.split("?url=")[1];
        url = decodeURIComponent(url);

		//setTimeout( function(){

		var page = require('webpage').create();
		var finished = 0;


		//Take up to X seconds
        setTimeout(function(){
        	console.log("Timeout check.");
        	if(finished)
        	{
        		console.log("Already responded");
        		return;
        	}
        	if(response)
        	{
	        	response.statusCode=500;
	        	response.write("Timeout.");
	        	response.close();
	        	page.close();
        	}
        }
        ,20000);//20 seconds
        
		page.onConsoleMessage = function(msg) {
		    if(msg.indexOf("URL:") == 0)
		    {
		    	response.write(msg.split("URL:")[1]);
		    	console.log(msg);
		    	response.close();
		    	page.close()
		    	finished=1;
		    }
		    else
		    {
		    	//console.log("NOISE----:"+msg);
		    }
		};
		page.open(url, function(status) {
		    if ( status === "success" ) {
		        page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js", function() {
		            page.evaluate(function() {		            			            	
         
         			//https://www.google.com/search?q=banana
		            // var cites = $("cite");
		            // for(var c in cites)
		            // {
		            	// console.log("URL:",$(cites[c]).text());
		            // }
		            var alinks = $(".r a");
		            
		            var res = [];
		            
		            for(var i in alinks)
		            {
		            	var dirty_link = $(alinks[i]).attr('href');
		            	if(dirty_link)
		            	{
			            	var clean = dirty_link.split("/url?q=")[1];
			            	if(clean)
			            	{
			            	  clean = clean.split("&sa")[0];
			            	  
			            	  res.push(clean);	
			            	}


		            	///url?q=
		            	}
		            }
		            
		            console.log("URL:"+JSON.stringify({'results':res}));
		            //console.log("URL:"+clean);
		            });
		        });
		    }
		    else
		    {
		    	response.statusCode=500;
	        	response.write("Page failed to load.  Nothing extracted.");
	        	response.close();
	        	page.close();
	        	finished = 1;
		    }
		});
    });

    if (service) {
        console.log('Web server running on port ' + port);
    } else {
        console.log('Error: Could not create web server listening on port ' + port);
        phantom.exit();
    }
}