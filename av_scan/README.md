# av_scan 
This was invoked by a Jenkin's job to retrieve an API key from AWS secrets and sys.exit(1) if an infected file was found via a routine scan.  The exit code 1 was for triggering a specific notification event via the Jenkinsfile.

Usage:
stage execution in a Jenkinfile
`./av_scan.py`
