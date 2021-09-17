#!/bin/bash

set -e

while true;do
	./unpatch.sh
	sleep 5
	./patch.sh
done
