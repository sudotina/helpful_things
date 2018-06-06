# sync_rpms
Used along side a systemd timer. 


**Description:**
This script will look for a file named REFRESH in subdirectories under user agent's home dir, validate rpms as signed by an expected key ID and not 0 filesize, move them to the correct repo location on the system, and run createrepo update to make the rpms available to yum. This is designed for randomly pushed small batches of rpms to manage 3 dynamic yum repositories.

Usage:
`./sync_rpms.py`

Output:
```
Refresh file found in /home/agent/centos7 directory.
/home/agent/centos7/failed.rpm is an invalid size. Skipping...
/home/agent/centos7/lsof-4.87-4.el7.x86_64.rpm has been moved to /usr/share/yum/centos/7/x86_64/
Deleted /home/agent/centos7/REFRESH
Syncing Repo Location: /usr/share/yum/centos/7/x86_64/ 
Spawning worker 0 with 1 pkgs
Workers Finished
Saving Primary metadata
Saving file lists metadata
Saving other metadata
Generating sqlite DBs
Sqlite DBs complete
Process completed for centos7 directory.
Refresh file found in /home/agent/centos6 directory.
/home/agent/centos6/notvalid.rpm is an invalid size. Skipping...
Deleted /home/agent/centos6/REFRESH
Process completed for centos6 directory.
```

