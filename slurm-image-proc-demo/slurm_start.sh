#!/bin/bash
/usr/sbin/create-munge-key
service munge restart
service slurmctld restart
service slurmd restart
