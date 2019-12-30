#!/bin/bash

# Define the usage function
function usage() {
	echo "Usage: $0 [OPTIONS] [--help] [master.tex]"
	echo "Identifies dependencies of a .tex file and packs them into a .zip file."
	echo "Moreover, the .zip file is tested whether its contents compile in a"
	echo "clean environment. In some cases, dependencies are not automatically"
	echo "detected and need to be added manually using --extra-files."
	echo
	echo "OPTIONS can be"
	echo "  --with-biblatex     includes system's biblatex package"
	echo "  --with-pdf          includes master.pdf file"
	echo "  --without-bibfiles  excludes .bib files"
	echo "  --arxiv             implies --with-biblatex --without-bibfiles"
	echo "                      and adds 00README.XXX"
	echo "  --extra-files       include an additional list of files specified by subsequent arguments"
	echo "  --verbose           be verbose"
	echo "  --help              print help and exit"
	echo "  --                  specifies the end of command options"
	echo
	echo "If master.tex is not given, the likely .tex master file in the current directory"
	echo "will be determined automatically." 
	echo
	echo "Examples:"
	echo "$0 --arxiv manuscript-numapde-preprint.tex" 
	echo "$0 --extra-files data/run1.csv data/run2.csv -- manuscript-numapde-preprint.tex"
}

# Set debugging flag
_DEBUG=false

# Declare intelligent debug function
# from http://www.cyberciti.biz/tips/debugging-shell-script.html
function DEBUG()
{
 [ "$_DEBUG" = "true" ] && $@
}

# Set the default options
INCLUDEBIBLATEX=false
INCLUDEBIBFILES=true
INCLUDEPDFFILE=false
INCLUDEARXIVHEADER=false
EXTRAFILES=()
VERBOSE=false

# Parse the command line arguments
# https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f
# https://www.assertnotmagic.com/2019/03/08/bash-advanced-arguments/
while (( "$#" )); do

	case "$1" in
		--extra-files)
			shift
			while [ "$#" -gt 0 -a "${1:0:2}" != "--" ]; do
				EXTRAFILES+=("$1")
				shift
			done
			;;

		--with-biblatex)
			INCLUDEBIBLATEX=true
			shift
			;;

		--with-pdf)
			INCLUDEPDFFILE=true
			shift
			;;

		--without-bibfiles)
			INCLUDEBIBFILES=false
			shift
			;;

		--arxiv)
			INCLUDEBIBLATEX=true
			INCLUDEBIBFILES=false
			INCLUDEARXIVHEADER=true
			shift
			;;

		--verbose)
			_DEBUG=true
			shift
			;;

		--)
			shift
			;;

		--help|-*)
			usage
			exit 1
			;;

		*)
			# An argument starting with anything but '-' represents master.tex.
			# Only one such argument can be given.
			if [ -z "${TEXFILE+x}" ]; then
				TEXFILE=$1
				DEBUG echo $TEXFILE
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
		echo $(findmastertexfiles)
		echo "ERROR: Unable to locate master file. Please specify it."
		echo
		exit 1
	else
		TEXFILE=$(findmastertexfiles)
	fi
fi

# Append .tex to $TEXFILE and remove ./ if necessary
TEXFILE="${TEXFILE/%.tex/}.tex"
TEXFILE="${TEXFILE/#.\//}"
echo "Using master file $TEXFILE."

# Check whether $TEXFILE is readable
if [ ! -r "$TEXFILE" ]; then
	echo "ERROR: $TEXFILE is not readable."
	exit 1
fi

# Create other derived file names
AUXFILE="${TEXFILE/%.tex/}.aux"
BCFFILE="${TEXFILE/%.tex/}.bcf"
FLSFILE="${TEXFILE/%.tex/}.fls"
PDFFILE="${TEXFILE/%.tex/}.pdf"
ZIPFILE="${TEXFILE/%.tex/}.zip"

# Resolve $FILE's dependencies by having LaTeX generate an .fls file
echo "Generating list of dependencies $FLSFILE"
latexmk -g -pdf -silent -recorder "$TEXFILE" >/dev/null

# Check whether $FLSFILE is readable
if [ ! -r "$FLSFILE" ]; then
	echo "ERROR: $FLSFILE is not readable."
	exit 1
fi


# Create a list of files which are to be included with their (relative) path names preserved
RELATIVEFILES=$(mktemp)

# Include all INPUT files which have relative path names
awk '/^INPUT [^/]/ {if (match($0,/^INPUT (\.\/)?(.*)/,a)) print a[2]}' "$FLSFILE" >> $RELATIVEFILES

# Remove certain files
grep -v "${TEXFILE/%.tex/}.aux" $RELATIVEFILES | sponge $RELATIVEFILES
grep -v "${TEXFILE/%.tex/}.out" $RELATIVEFILES | sponge $RELATIVEFILES
grep -v "${TEXFILE/%.tex/}.run.xml" $RELATIVEFILES | sponge $RELATIVEFILES
if [ "$INCLUDEPDFFILE" = "true" ]; then
	echo "$PDFFILE" >> $RELATIVEFILES
fi

# Remove duplicate lines
sort -u $RELATIVEFILES | sponge $RELATIVEFILES


# Create a list of files which are to be included with their path names junked
JUNKEDFILES=$(mktemp)

# Include all INPUT files which have /home path names
HOME_ESCAPED=$(echo "$HOME" | sed 's/\//\\\//g')
awk "{if (match(\$0,/^INPUT ($HOME_ESCAPED\/.*)/,a)) print a[1]}" "$FLSFILE" >> $JUNKEDFILES

# Remove duplicate lines
sort -u $JUNKEDFILES | sponge $JUNKEDFILES


# Include .bib files if desired; these may have absolute or relative path names
if [ "$INCLUDEBIBFILES" = "true" ]; then
	if [ -r "$BCFFILE" ]; then
		# Search the .bcf file for .bib sources (biblatex)
		# <bcf:datasource type="file" datatype="bibtex">World.bib</bcf:datasource>
		awk '{if (match($0,/<bcf:datasource type="file" datatype="bibtex">(.*)<\/bcf:datasource>/,a)) print a[1]}' "$BCFFILE" | sort -u | xargs kpsewhich | grep '^./' >> $RELATIVEFILES
		awk '{if (match($0,/<bcf:datasource type="file" datatype="bibtex">(.*)<\/bcf:datasource>/,a)) print a[1]}' "$BCFFILE" | sort -u | xargs kpsewhich | grep '^/' >> $JUNKEDFILES
	elif  [ -r "$AUXFILE" ]; then
		# Search the .aux file for .bib sources (bibtex)
		# example: \bibdata{World}
		for bibfile in $(awk '{if (match($0,/\\bibdata{(.*)}/,a)) print a[1]}' "$AUXFILE" | tr "," "\n"); do echo ${bibfile/%.bib/}.bib; done | sort -u | xargs kpsewhich | grep '^./' >> $RELATIVEFILES
		for bibfile in $(awk '{if (match($0,/\\bibdata{(.*)}/,a)) print a[1]}' "$AUXFILE" | tr "," "\n"); do echo ${bibfile/%.bib/}.bib; done | sort -u | xargs kpsewhich | grep '^/' >> $JUNKEDFILES
		echo
	else
		echo ".bib files are to be included but neither $BCFFILE nor $AUXFILE are readable."
		echo "Please make sure $BCFFILE (in case of biblatex) or $AUXFILE (in case of bibtex) exist."
		echo "Stopping because of unclear .bib sources."
		exit 1
	fi
fi

# Include biblatex dependencies if desired
if [ "$INCLUDEBIBLATEX" = "true" ]; then
	awk '{if (match($0,/^INPUT (.*\/biblatex\/.*)/,a)) print a[1]}' "$FLSFILE" >> $JUNKEDFILES
fi

# Create and include arXiv header if desired
if [ "$INCLUDEARXIVHEADER" = "true" ]; then
	# Prepare the control file for arXiv
	echo "$TEXFILE toplevelfile" > 00README.XXX
	echo "nohypertex" >> 00README.XXX
	echo 00README.XXX >> $RELATIVEFILES
fi

# Include additional files
for FILE in "${EXTRAFILES[@]}"
do
	echo "$FILE" >> $RELATIVEFILES
done

DEBUG echo
DEBUG echo "The following files will be included with relative path names (as printed):"
DEBUG cat $RELATIVEFILES
DEBUG echo

DEBUG echo "The following files will be included with their path names junked:"
DEBUG cat $JUNKEDFILES
DEBUG echo

# Clear and create the zip file
rm -f "$ZIPFILE"
if [ -s $RELATIVEFILES ]; then
	while read FILE; do
		DEBUG echo zip --quiet "$ZIPFILE" "$FILE"
		zip --quiet "$ZIPFILE" "$FILE"
	done <$RELATIVEFILES
fi
if [ -s $JUNKEDFILES ]; then
	while read FILE; do
		DEBUG echo zip --quiet -j "$ZIPFILE" "$FILE"
		zip --quiet -j "$ZIPFILE" "$FILE"
	done <$JUNKEDFILES
fi


# Create a function to unpack and process the file in a sterile environment
# #1 is the name of the .zip file
# #2 is the name of the .tex file
# #3 is the $INCLUDEBIBFILES flag: if false, do not run biber or bibtex to try and generate the .bbl file
function validate() {
	# Create a tempoary directory
	TMPDIR=$(mktemp -d)

	# Call a new bash with $TEXINPUTS, $BIBINPUTS, $BSTINPUTS unset;
	# unzip the .zip file, and try to process it using latexmk
	env -u TEXINPUTS -u BIBINPUTS -u BSTINPUTS ZIPFILE="$1" TEXFILE="$2" PDFFILE="${2/%.tex/}.pdf" INCLUDEBIBFILES="$3" TMPDIR="$TMPDIR" \
		bash -c 'unzip "$ZIPFILE" -d "$TMPDIR" && \
		cd "$TMPDIR" && \
		if [ "$INCLUDEBIBFILES" = "true" ]; then \
			BIBTEXFLAG="-bibtex"; \
		else \
			BIBTEXFLAG="-bibtex-"; \
		fi && \
		latexmk -interaction=nonstopmode -pdf "$BIBTEXFLAG" "$TEXFILE"; \
		RESULT=$?; \
		if [ -f "${TMPDIR}/$PDFFILE" ]; \
			then (okular "${TMPDIR}/$PDFFILE" &); \
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
DEBUG echo validate "$ZIPFILE" "$TEXFILE" "$INCLUDEBIBFILES"
validate "$ZIPFILE" "$TEXFILE" "$INCLUDEBIBFILES"
echo $JUNKEDFILES
echo $RELATIVEFILES
