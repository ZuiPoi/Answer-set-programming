function readTextFile(file1)
{
    var res = []
    var loc = window.location.pathname;
    var dir = loc.substring(0, loc.lastIndexOf('/'));
    file = dir +file1
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                res = allText.split("\n");
                /*
                for (i in res) {
                alert(res[i])
                }
                */
               
            }
        }
    }
    rawFile.send(null);
    return res
}

