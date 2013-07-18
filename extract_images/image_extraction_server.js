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
        
        var url = request.url.split("=")[1];
        url = decodeURIComponent(url);

		//setTimeout( function(){
		
		var page = require('webpage').create();

		page.onConsoleMessage = function(msg) {
		    if(msg.indexOf("URL:") == 0)
		    {
		    	response.write(msg.split("URL:")[1]);
		    	response.close();
		    	page.close()
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
		                	all.push( getImgSize( images[i].src) );
		                }
		                console.log("URL:"+JSON.stringify(all));
		            });
		        });
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
