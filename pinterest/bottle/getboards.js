var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

page.onConsoleMessage = function(msg)
{
	console.log(msg);
}

if (system.args.length < 1 || system.args.length > 5) {
    console.log('Usage: getboards.js URL');
    phantom.exit(1);
} else {
    address = system.args[1];
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit();
        } else {
            window.setTimeout(function () {
            	
            	page.evaluate(function()
            	{
            		var boards = $(".boardName");
					for(var b = 0; b < boards.length; b+=1)
					{
					  var bname = $(boards[b]).text().trim();
					  var url = $(boards[b]).parent().attr("href").split("/")[2];
//					  console.log(bname);
					  console.log(url);
					}
            	});
                phantom.exit();
            }, 200);
        }
    });
}