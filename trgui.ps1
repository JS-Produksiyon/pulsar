param (
    [Parameter(Mandatory=$true)]
    [string]$action
)

# define languages available
$langs = @('de', 'en', 'tr')
$mainFile = '.\src\pulsar.py'
$trName = 'pulsar'
$trDir = 'translations\'
$tsDir = 'ts\'

Write-Output "Script to extract strings from a PyQT6 environment for translationito .ts files and compile the translated texts into .qm files."

Write-Output " "

if (Test-Path env:VIRTUAL_ENV) {
    switch ($action) {
        'extract' {
            # extract the strings from the given system
            $uiFiles = Get-ChildItem -Path ".\src\ui" -Filter *.ui -File | ForEach-Object {
                $_.FullName
            }
            $srcFiles = $mainFile + " " + $uiFiles -join " "
            foreach ($l in $langs) {
                $trArgs = $srcFiles + " -ts " + ".\src\" + $trDir + $tsDir + $trName + "_" + $l + ".ts"
                Write-Output "Extracting strings to $l"
                $prog = (Get-Command pyside6-lupdate.exe).Source
                Start-Process $prog -ArgumentList $trArgs
            }
        }
        'compile' {
            foreach ($l in $langs) {
                Write-Output "Compiling strings for $l"
                $trArgs = ".\src\" + $trDir + $tsDir + $trName + "_" + $l + ".ts -qm " + ".\src\" + $trDir + $trName + '_' + $l + ".qm"
                Write-Output $trArgs
                $prog = (Get-Command pyside6-lrelease.exe).Source
                Start-Process $prog -ArgumentList $trArgs
            }
        }
        default {
            Write-Output "You have not selected an appropriate action. Please use either 'compile' or 'extract'."
        }
    }
} else {
    Write-Output "This script must run in a Python virtual environment to extract the strings."
}