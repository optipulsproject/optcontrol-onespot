#!/bin/bash
# This script sets up the TEXINPUTS and BIBINPUTS environment variables, which
# are used as search paths for LaTeX and BibLaTeX files, respectively.

# Make sure this script is being sourced rather than executed, since otherwise
# the environment is being set in a new bash process 
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
	echo "Call this script using"
	echo "source ${0}"
	exit
fi

# Append ./numapde-latex to TEXINPUTS if necessary
if kpsewhich numapde-preprint.cls; then
	echo "  found so TEXINPUTS appears to be properly set."
	echo
else
	export TEXINPUTS=$TEXINPUTS:./numapde-latex//
	echo "Setting TEXINPUTS, which is now ${TEXINPUTS}"
	echo
fi

# Append ./numapde-bibliography to BIBINPUTS if necessary
if kpsewhich World.bib; then
	echo "  found so BIBINPUTS appears to be properly set."
	echo
else
	export BIBINPUTS=$BIBINPUTS:./numapde-bibliography//
	echo "Setting BIBINPUTS, which is now ${BIBINPUTS}"
	echo
fi

