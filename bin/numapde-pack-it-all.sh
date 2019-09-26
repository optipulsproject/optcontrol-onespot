#!/bin/bash
# This script takes a .tex document, identifies its dependencies and packs
# them, by default, into a .zip file.
#
# Usage:    numapde-pack-it-all.sh [--options] [master.tex]

# Define the usage function
function usage() {
	echo "Usage: $0 [OPTIONS] [--help] [master.tex]"
	echo "where OPTIONS can be"
	echo "  --with-biblatex     includes system's biblatex package"
	echo "  --with-pdf          includes master.pdf file"
	echo "  --without-bibfiles  excludes .bib files"
	echo "  --arxiv             implies --with-biblatex --without-bibfiles"
	echo "                      and adds 00README.XXX"
	echo "  --verbose           be verbose"
	echo
	echo "If master.tex is not given, the likely .tex master file in the current directory"
	echo "will be determined automatically." 
}

# Set debugging flag
_DEBUG=false

# Declare intelligent debug function
# from http://www.cyberciti.biz/tips/debugging-shell-script.html
function DEBUG()
{
 [ "$_DEBUG" = "true" ] &&  $@
}

# Set the default options
INCLUDEBIBLATEX=false
INCLUDEBIBFILES=true
INCLUDEPDFFILE=false
INCLUDEARXIVHEADER=false
VERBOSE=false

# Parse the command line arguments
# https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f
# https://www.assertnotmagic.com/2019/03/08/bash-advanced-arguments/
while (( "$#" )); do

	case "$1" in
		--with-biblatex)
			INCLUDEBIBLATEX=true
			shift
			break
			;;

		--with-pdf)
			INCLUDEPDFFILE=true
			shift
			break
			;;

		--without-bibfiles)
			INCLUDEBIBFILES=false
			shift
			break
			;;

		--arxiv)
			INCLUDEBIBLATEX=true
			INCLUDEBIBFILES=false
			INCLUDEARXIVHEADER=true
			shift
			break
			;;

		--verbose)
			_DEBUG=true
			shift
			break
			;;

		--help|-*)
			usage
			exit 1
			;;

		*)
			# An argument starting with a 'non-' represents master.tex.
			# Only one such argument can be given.
			if [ -z ${TEXFILE+x} ]; then
				TEXFILE="$1"
				shift
			else
				usage
				exit 1
			fi
			;;

	esac
done

# If no master file has been given, or if it is empty, try to locate
# the likely master file by searching for documentclass
if [ -z "$TEXFILE" ]; then
	findmastertexfiles() {
		find . -maxdepth 1 -name "*.tex" -type f -print0 | xargs -0 grep -l documentclass
	}
	NOOFFILES=$(findmastertexfiles | wc -l)
	if [ "$NOOFFILES" != 1 ]; then
		usage
		echo
		echo "ERROR: Unable to locate master file. Please specify it."
		echo
		exit 1
	else
		TEXFILE=$(findmastertexfiles)
	fi
fi

# Append .tex to $TEXFILE and remove ./ if necessary
TEXFILE=${TEXFILE/%.tex/}.tex
TEXFILE=${TEXFILE/#.\//}
echo "Using master file $TEXFILE."

# Check whether $TEXFILE is readable
if [ ! -r "$TEXFILE" ]; then
	echo "ERROR: $TEXFILE is not readable."
	exit 1
fi

# Create other derived file names
AUXFILE=${TEXFILE/%.tex/}.aux
BCFFILE=${TEXFILE/%.tex/}.bcf
FLSFILE=${TEXFILE/%.tex/}.fls
PDFFILE=${TEXFILE/%.tex/}.pdf
ZIPFILE=${TEXFILE/%.tex/}.zip

# Resolve $FILE's dependencies by having LaTeX generate an .fls file
echo "Generating list of dependencies $FLSFILE"
latexmk -g -pdf -silent -recorder $TEXFILE >/dev/null

# Check whether $FLSFILE is readable
if [ ! -r "$FLSFILE" ]; then
	echo "ERROR: $FLSFILE is not readable."
	exit 1
fi


# Create a list of files which are to be included with their (relative) path names preserved
RELATIVEFILES=$(mktemp)

# Include all INPUT files which have relative path names
awk '/^INPUT [^/]/ {if (match($0,/^INPUT (\.\/)?(.*)/,a)) print a[2]}' $FLSFILE >> $RELATIVEFILES

# Remove certain files
grep -v ${TEXFILE/%.tex/}.aux $RELATIVEFILES | sponge $RELATIVEFILES
grep -v ${TEXFILE/%.tex/}.out $RELATIVEFILES | sponge $RELATIVEFILES
grep -v ${TEXFILE/%.tex/}.run.xml $RELATIVEFILES | sponge $RELATIVEFILES
if [ "$INCLUDEPDFFILE" = "true" ]; then
	echo "$PDFFILE" >> $RELATIVEFILES
fi

# Remove duplicate lines
sort -u $RELATIVEFILES | sponge $RELATIVEFILES


# Create a list of files which are to be included with their path names junked
JUNKEDFILES=$(mktemp)

# Include all INPUT files which have /home path names
awk '{if (match($0,/^INPUT (\/home\/.*)/,a)) print a[1]}' $FLSFILE >> $JUNKEDFILES

# Remove duplicate lines
sort -u $JUNKEDFILES | sponge $JUNKEDFILES


# Include .bib files if desired; these may have absolute or relative path names
if [ "$INCLUDEBIBFILES" = "true" ]; then
	if [ -r $BCFFILE ]; then
		# Search the .bcf file for .bib sources (biblatex)
		# <bcf:datasource type="file" datatype="bibtex">World.bib</bcf:datasource>
		awk '{if (match($0,/<bcf:datasource type="file" datatype="bibtex">(.*)<\/bcf:datasource>/,a)) print a[1]}' $BCFFILE | sort -u | xargs kpsewhich | grep '^./' >> $RELATIVEFILES
		awk '{if (match($0,/<bcf:datasource type="file" datatype="bibtex">(.*)<\/bcf:datasource>/,a)) print a[1]}' $BCFFILE | sort -u | xargs kpsewhich | grep '^/' >> $JUNKEDFILES
	elif  [ -r $AUXFILE ]; then
		# Search the .aux file for .bib sources (bibtex)
		# \bibdata{World}
		for bibfile in $(awk '{if (match($0,/\\bibdata{(.*)}/,a)) print a[1]}' $AUXFILE | tr "," "\n"); do echo ${bibfile/%.bib/}.bib; done | sort -u | xargs kpsewhich | grep '^./' >> $RELATIVEFILES
		for bibfile in $(awk '{if (match($0,/\\bibdata{(.*)}/,a)) print a[1]}' $AUXFILE | tr "," "\n"); do echo ${bibfile/%.bib/}.bib; done | sort -u | xargs kpsewhich | grep '^/' >> $JUNKEDFILES
		echo
	else
		echo ".bib files are to be included but neither $BCFFILE nor $AUXFILE are readable."
		exit 1
	fi
fi

# Include biblatex dependencies if desired
if [ "$INCLUDEBIBLATEX" = "true" ]; then
	awk '{if (match($0,/^INPUT (.*\/biblatex\/.*)/,a)) print a[1]}' $FLSFILE >> $JUNKEDFILES
fi

# Create and include arXiv header if desired
if [ "$INCLUDEARXIVHEADER" = "true" ]; then
	# Prepare the control file for arXiv
	echo "$TEXFILE toplevelfile" > 00README.XXX
	echo "nohypertex" >> 00README.XXX
	echo 00README.XXX >> $RELATIVEFILES
fi


DEBUG echo
DEBUG echo "The following files will be included with relative path names (as printed):"
DEBUG cat $RELATIVEFILES
DEBUG echo

DEBUG echo "The following files will be included with their path names junked:"
DEBUG cat $JUNKEDFILES
DEBUG echo

# Clear and create the zip file
rm -f $ZIPFILE
zip --quiet $ZIPFILE $(cat $RELATIVEFILES)
zip --quiet -j $ZIPFILE $(cat $JUNKEDFILES)


# Create a function to unpack and process the file in a sterile environment
# #1 is the name of the .zip file
# #2 is the name of the .tex file
# #3 is the $INCLUDEBIBFILES flag: if false, do not run biber or bibtex to try and generate the .bbl file
function validate() {
	# Create a tempoary directory
	TMPDIR=$(mktemp -d)

	# Call a new bash with $TEXINPUTS, $BIBINPUTS, $BSTINPUTS unset;
	# unzip the .zip file, and try to process it using latexmk
	env -u TEXINPUTS -u BIBINPUTS -u BSTINPUTS ZIPFILE=$1 TEXFILE=$2 PDFFILE=${2/%.tex/}.pdf INCLUDEBIBFILES=$3 TMPDIR=$TMPDIR \
		bash -c 'unzip $ZIPFILE -d $TMPDIR && \
		cd $TMPDIR && \
		if [ "$INCLUDEBIBFILES" = "true" ]; then \
			BIBTEXFLAG="-bibtex"; \
		else \
			BIBTEXFLAG="-bibtex-"; \
		fi && \
		latexmk -interaction=nonstopmode -pdf $BIBTEXFLAG $TEXFILE; \
		RESULT=$?; \
		if [ -f ${TMPDIR}/$PDFFILE ]; \
			then okular ${TMPDIR}/$PDFFILE; \
		fi; \
		exit $RESULT' > /dev/null

	# Report success or failure
	if [[ $? != 0 ]]; then
		echo
		echo "latexmk run in $TMPDIR FAILED"
	else
		echo
		echo "latexmk run in $TMPDIR SUCCESSFUL"
	fi
}

# Validate the zip file contents
validate $ZIPFILE $TEXFILE $INCLUDEBIBFILES

