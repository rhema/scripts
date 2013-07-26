var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

var renderme = 1;

var nopint = system.args[1].split("pinterest.com/")[1];
//console.log("HOW WE SEE IF PINBOARD:"+system.args[1]);
var parts = nopint.split("/");
var not_userpage = 0;
if(parts.length == 2)
{
	not_userpage = 1;
	console.log("THIS IS A USERPAGE");
}
else
{
	console.log("THIS IS A PINBOARD");
}


var fs = require('fs');
var outfile = 0;
var uid = system.args[2].split("/")[1];
console.log("UID:"+uid);

if(not_userpage == 1)
{
	outfile = fs.open('pinboards/all.csv','a');
}
else
{
	fname = "pinboards/"+uid+"/meta.csv";
	outfile = fs.open(fname,'a'); 
}

page.onConsoleMessage = function(msg)
{
	console.log(msg);
	if(msg == "nopenopenope")
	{
		renderme = 0;
	}
	if(msg.split(":")[0] == "DATA")
	{
	   outfile.writeLine(uid+msg.split(":")[1]);
	}
}

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: rasterize.js URL filename [paperwidth*paperheight|paperformat] [zoom]');
    console.log('  paper (pdf output) examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 600, height: 600 };
    if (system.args.length > 3 && system.args[2].substr(-4) === ".pdf") {
        size = system.args[3].split('*');
        page.paperSize = size.length === 2 ? { width: size[0], height: size[1], margin: '0px' }
                                           : { format: system.args[3], orientation: 'portrait', margin: '1cm' };
    }
    if (system.args.length > 4) {
        page.zoomFactor = system.args[4];
    }
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit();
        } else {
            window.setTimeout(function () {
            	
            	page.evaluate(function()
            	{
            		//Need to tell if board or user page from here...
            		var fullname = "nopenopenope";
            		if ($(".fullname").length > 0)
            		{
            			fullname = $($(".fullname")[0]).html();
            		}
            		else
            		{
            			fullname = $(".userProfileHeaderName").html();
            		}
            		
            		//console.log("I HEARBY GIVE THIS FIRST NAME TO YOU!!!!");
            		//console.log(fullname);
            		
		    		//$(".firstAttribution").children(".attributionName").html("anon"); //$("attributionTitle").contains()
		    		$(".firstAttribution:contains("+fullname+")").children(".attributionName").html("anon").html("anon");
					var pins = $(".pinHolder");
					for(var p = 0; p < pins.length; p+=1)
					{
						var img = $("img",pins[p]).attr("src");
						//console.log(img);
						$(pins[p]).html("<img src='"+img+"'/>");
					}
					$(".userProfileHeaderName").html("anon");
					$(".fullname").html("anon");
					
					var buttontexts = $(".InfoBarBase a");
					var data = $(".BoardHeader h1").text();
					if(data.length > 0)
					   data = ","+data;
					for(var i in buttontexts)
					{
					  if(buttontexts[i].innerHTML)
					  {
					    var numstring = $(buttontexts[i]).text().trim().split(" ")[0];
					    if(isNaN(numstring) == false)
					    data += ","+numstring;
					  }
					}
					
					var boards = $(".boardName");
					var bs = [];
					for(var b = 0; b < boards.length; b+=1)
					{
					  var bname = $(boards[b]).parent().attr("href").split("/")[2];
					  bs.push(bname);
					}
					var bnames = (bs.join("|"));
					if(bnames.length > 0)
					  bnames = ","+bnames;
					data += bnames;
					
					console.log("DATA:"+data);

            	});
            	if(renderme == 1)
            	{
                	page.render(output);
                }
                else
                {
                	console.log("THIS WILL NOT RENDER BECAUSE SCRUBBING FAILED.");
                }
                outfile.close();
                phantom.exit();
            }, 200);
        }
    });
}