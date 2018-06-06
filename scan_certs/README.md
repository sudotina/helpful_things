# scan_certs
This is a python script created to scan Salt directories for pillar files, scan said files for references to PEM certs, and notify a Slack channel with which file contains the cert, the subject, and the cert's not after date.  Different warnings available for < 30 days to expiration/already expired and < 60 days to expiration.

Usage:
`./scan_certs.py`
