#!/bin/bash
# This script updates all or selected submodules within the current repository.

# Initialize all submodules, in case this has not been done
git submodule init

# Pull from all submodules 
git submodule update --remote --merge

