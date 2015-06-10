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

function trackClick()
{
	//alert("trackClick");
	
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

	var trackimage = new Image();
	trackimage.src = "countclicks.php?url="+url; //this does not work in Safari, but why???
	//alert(trackimage.src);

}

function initCountClicks()
{
	//alert("initCountClicks");
	var links = document.getElementsByTagName("a"); //now links is a list of all links in the document
	for(var i=0; i<links.length;++i)
	{
		addEvent(links[i], "click", trackClick);
	}
}

addEvent(window, "load", initCountClicks);

//var trackimage = new Image();
//trackimage.src = "php/countclicks.php?url=testtest.html";  //this does work in Safari!!
