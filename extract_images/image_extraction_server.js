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
            'Content-Type': 'application/json'
        };
        
        var url = request.url.split("=")[1];
        url = decodeURIComponent(url);

		//setTimeout( function(){
		
		var page = require('webpage').create();

		page.onConsoleMessage = function(msg) {
		    if(msg.indexOf("URL:") == 0)
		    {
		    	response.write(msg.split("URL:")[1]);
		    	response.close();
		    }
		};
		page.open(url, function(status) {
		    if ( status === "success" ) {
		        page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
		            page.evaluate(function() {
		            	
		            	
		            	
		            	var getImgSize = function(imgSrc) {
						    var newImg = new Image();
						    newImg.src = imgSrc;
						    var height = newImg.height;
						    var width = newImg.width;
						    return {"width":width,"height": height, "image_src":imgSrc};
						}
		            	
		                //console.log("URL:"+$($("img")[0]).attr("src"));
		                var images = $("img");	
		                var all=[];
		                for(var i=0;i<images.length;i++)
		                {
		                	//console.log($(images[i]).attr("src"));
		                	all.push( getImgSize( $(images[i]).attr("src") ));
		                }
		                console.log("URL:"+JSON.stringify(all));
		            });
		        });
		    }
		});
		
		
			
		//response.write("<h1>"+url+"</h1>");
        //response.close();
        
        
        //}, 5000 );
		//f(response,url);
        
           //response.write("<h1>"+url+"</h1>");
           //response.close();
        /*
        response.write('<html>');
        response.write('<head>');
        response.write('<title>Hello, world!</title>');
        response.write('</head>');
        response.write('<body>');
        response.write('<p>This is from PhantomJS web server.</p>');
        response.write('<p>Request data:</p>');
        response.write('<pre>');
        response.write(JSON.stringify(request, null, 4));
        response.write('</pre>');
        response.write('</body>');
        response.write('</html>');
        response.close();
        */
    });

    if (service) {
        console.log('Web server running on port ' + port);
    } else {
        console.log('Error: Could not create web server listening on port ' + port);
        phantom.exit();
    }
}
