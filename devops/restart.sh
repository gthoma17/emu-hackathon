#!/bin/sh
fuser -n tcp -k 7002
sh /apps/crimes/devops/startup.sh