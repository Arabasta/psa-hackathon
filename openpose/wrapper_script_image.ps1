# PowerShell script to execute OpenPoseDemo.exe with arguments
# Define the path to the OpenPoseDemo.exe
$openPoseExePath = ".\bin\OpenPoseDemo.exe"  # The dot and backslash (.\) tells PowerShell it's a local executable

# Define the arguments for OpenPoseDemo.exe
$imageDir = "../fastapi/raw_image/"
$outputDir = "../fastapi/rendered_image/"

# Construct the command with arguments
$command = "$openPoseExePath --image_dir $imageDir --write_images $outputDir"

# Execute the command
Invoke-Expression $command
