<?php header("content-type: text/javascript"); 

 //-------------------------------------------------------------
 // Prevent Caching (see http://www.lingo4u.de/article/fontsize)
 //-------------------------------------------------------------

  header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
  header('Last-Modified: '.gmdate('D, d M Y H:i:s').' GMT');
  header('Cache-Control: no-store');
  header('Pragma: no-cache');

  list($usec, $sec) = explode(' ',microtime());
  print('/* '.((float)$usec + (float)$sec)." */\n");
  
 //------------------------------------------------------------- 

$filename="php/clicks.txt";

if(file_exists($filename))
{
	// read file and convert each line into an element
	// of the array input
	
	$input = file($filename);
}
else
{
	// if file doesn't exist initialize input as empty
	// array
	$input=array();
}

// remove annoying escape sequences like \n,\r at the end of each line
for ($i = 0; $i < count($input); $i++) 
{
	$input[$i]=trim($input[$i]);
}

//write first part of javascript
echo "var liste = new Array(\n";

for ($i = 0; $i < count($input); $i++) 
{
	// split each line into two strings
	$temp = explode("\t", $input[$i]);
	
	// $size = 1.0 + log((1.0+$temp[1]),4);
	// $size = 1.0 + log($temp[0],4);
	
	// finally write the css for each link in input
    //echo "a[href=\"$temp[0]\"] {color:red; font-size:".$size."em;}\n";
     //echo "a[href=\"$temp[0]\"]:hover:after {content:\"/A (".$temp[1]." Clicks)\";}\n";
     
     
     if ( $i < (count($input)-1))
     {
     	echo "[\"$temp[1]\",$temp[0]],\n"; //write each line of the array for javascript
     }
     else
     {
     	echo "[\"$temp[1]\",$temp[0]]"; //for the last line do not write ",\n"
     }	
}

echo ");";

// P.S.: When saving this file as UTF-8 make sure to save it 
// without(!) BOM (byte order mark), because of a bug in PHP5 
// (see http://bugs.php.net/bug.php?id=22108)

?>

//var liste = new Array(
//["http://www.google.de",5],
//["http://www.heise.de",3],
//["http://www.astro.uni-wuerzburg.de",10],
//["test.html",8]);

var tip = null;

// See 
// http://onlinetools.org/articles/unobtrusivejavascript/chapter4.html
// http://ichwill.net/chapter4 (in german)
// and
// http://www.scottandrew.com/weblog/articles/cbs-events
//
function addEvent(obj, evType, fn)
{
	if (obj.addEventListener) //for Firefox-like browsers
	{
		obj.addEventListener(evType, fn, false); 
		return true;
	}
	else if (obj.attachEvent) //for IE-like browsers
	{ 
		var r = obj.attachEvent("on"+evType, fn); 
		return r; 
	} 
	else 
	{ 
		return false; 
	} 
}

function createTooltip(obj)
{
	var url;
	
	if(this==window) //for IE-like browsers "this" points to window
	{
		// getAttribute in IE returns the absolute path by default
		// use second parameter = 2, if you want to have only the 
		// attribute text, see 
		// http://www.glennjones.net/Post/809/getAttributehrefbug.htm
		
		url= obj.getAttribute("href", 2);
	}
	else
	{
		url=obj.getAttribute("href");
	}
	
	// alert(url);
	
	// var url = obj.getAttribute("href");
	var clicks = 0;
	
	for(var i=0; i<liste.length;++i)
	{
		if(liste[i][0]==url)
		{
			clicks = liste[i][1];
		}
	}
	
	if(clicks > 0)
	{	
		
				
		var t=document.createElement("div");
		//var tmessage=document.createTextNode("Dies ist " + url + " mit " + clicks + " Klicks");
		var tmessage=document.createTextNode(clicks + " Klicks");
		var size = 0.8*(1.0 + Math.log(clicks)/Math.log(100));
	
		t.className = "tooltip";
		t.id = url;
		t.style.fontSize = size + "em";
	
		document.getElementsByTagName("body")[0].appendChild(t);
		document.getElementsByTagName("body")[0].lastChild.appendChild(tmessage);
	}
}
	
	
function initTooltips()
{
	//alert("window load event");
	var links = document.getElementsByTagName("a"); //now links is a list of all links in the document
	for(var i=0; i<links.length;++i)
	{
		addEvent(links[i], "mouseover", showtooltip);
		addEvent(links[i], "mouseout", hidetooltip);
		createTooltip(links[i]);
	}	
}

function showtooltip()
{	
	var url;
	
	// instead of using "this" in IE, you have to use 
	// "window.event.srcElement" to access the element which called the 
	// function, see
	// http://www.quirksmode.org/js/events_properties.html
	
	if(this==window) //for IE-like browsers "this" points to window
	{
		// getAttribute in IE returns the absolute path by default
		// use second parameter = 2, if you want to have only the 
		// attribute text, see 
		// http://www.glennjones.net/Post/809/getAttributehrefbug.htm
		
		url= window.event.srcElement.getAttribute("href", 2);
	}
	else
	{
		url=this.getAttribute("href");
	}
	
	//alert(url);
	
	tip = document.getElementById(url);
	//alert(tip);
	if(tip != null)
	{
		tip.style.display="block";
	}
}

function hidetooltip()
{
	if(tip != null)
	{
		tip.style.display="none";
	}
}


//
// See http://webmatze.de/webdesign/javascript/tooltips.htm
// and http://www.quirksmode.org/js/events_properties.html
//
function updateTIP(e) {
	x = (document.all) ? window.event.clientX + document.body.scrollLeft : e.pageX;
	y = (document.all) ? window.event.clientY + document.body.scrollTop  : e.pageY;
	if (tip != null) {
		tip.style.left = (x + 20) + "px";
		tip.style.top 	= (y + 20) + "px";
	}
}

document.onmousemove = updateTIP;

addEvent(window, "load", initTooltips)
