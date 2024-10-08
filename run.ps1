# PowerShell script: run_script.ps1

# Check if at least one command argument is provided
if ($args.Length -eq 0) {
    Write-Host "Usage: .\run_script.ps1 <cmd1> <cmd2> ..."
    exit 1
}

# Define the path to the Python executable and the Python script
$pythonExe = "./ppdf/Scripts/python.exe"
$pythonScript = "./src/main.py"

# Execute the Python script with the provided arguments
& $pythonExe $pythonScript @args

# Optionally, capture the exit code and print it if needed
$exitCode = $LASTEXITCODE
Write-Host "Process exited with code $exitCode"
