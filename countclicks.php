<?php 

$url=$_GET['url'];
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

//for debugging

//foreach($input as $zeile)
//{
//	error_log("input: $zeile",0);
//}

$notfound=0;

//loop through each line of the array
for ($i = 0; $i < count($input); $i++) 
{
	$temp = explode("\t", $input[$i]);
	
	error_log("temp[1]: $temp[1]",0);
    error_log("url: $url",0);
    
    if ($temp[1] == $url)   //does the comparison always work?
    {
      //increase number of clicks
      $temp[0]++;
    }
    else
    {
    	$notfound++;
    }
    $output[] = implode("\t", $temp);
}

// if the link is not in the array, 
// add a new entry to the array
if ($notfound == count($input))
{
	$output[] = "1\t".$url;
}

// for debugging

//foreach($output as $zeile)
//{
// 	error_log("output: $zeile",0);
//}

//save data to file
$filepointer = fopen($filename, "w");
fwrite($filepointer, implode("\n", $output));
fclose($filepointer)

?>
