#!/usr/bin/python
# Written by: sudotina

from __future__ import print_function
import os, subprocess, shutil, glob, sys, fcntl

f = open('/var/run/sync_rpms', 'w')
try:
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    sys.exit('sync_rpms.py process is already running.')

def refresh_file_exists(location):
    if os.path.isfile(os.path.join(location,"REFRESH")):
        print('Refresh file found in {} directory.'.format(location), file=sys.stderr)
        return True

    return False

def find_valid_rpms(directory):
    rpms = glob.glob(os.path.join("/home/agent/", directory, "*.rpm"))
    valid_rpms = []

    for rpm in rpms:
        if os.stat(rpm).st_size == 0:
            print('{} is an invalid size. Skipping...'.format(rpm), file=sys.stderr)
            continue

        if directory == 'centos6' or directory == 'centos7':
            if not has_valid_sig(rpm):
                print('{} is not signed. Skipping...'.format(rpm), file=sys.stderr)
                continue

        valid_rpms.append(rpm)

    return valid_rpms

def has_valid_sig(rpm):
    out = subprocess.check_output(['/usr/bin/rpm', '-v', '--checksig', rpm])
    if "key ID f4a80eb5: OK" in out:
        return True
    return False

def process_rpms(directory, valid_rpms, destination):
    for rpm in valid_rpms:
        shutil.move(rpm, destination)
        print('{} has been moved to {}'.format(rpm, destination), file=sys.stderr)

    delete_refresh(directory)
    sync_repo(destination)

def delete_refresh(directory):
    refresh_file = os.path.join("/home/agent/", directory, "REFRESH")
    os.remove(refresh_file)
    print('Deleted {}'.format(refresh_file), file=sys.stderr)

def sync_repo(destination):
    out = subprocess.check_output(['createrepo', '--update', destination])
    print("Syncing Repo Location: {} \n{}".format(destination, out), file=sys.stderr)

# Main
repositories = {
    'centos7': 'centos/7/x86_64/',
    'centos6': 'centos/6/x86_64/',
    'apps': 'applications/7/x86_64/',
}

for agent_dir, yum_repo_loc in repositories.iteritems():
    if refresh_file_exists(os.path.join("/home/agent/", agent_dir)):
        valid_rpms = find_valid_rpms(agent_dir)
        if valid_rpms:
            process_rpms(agent_dir, valid_rpms, os.path.join("/usr/share/yum/", yum_repo_loc))
        else:
            delete_refresh(agent_dir)
        print('Process completed for {} directory.'.format(agent_dir), file=sys.stderr)
