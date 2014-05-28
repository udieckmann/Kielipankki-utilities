#! /bin/sh
# -*- coding: utf-8 -*-

# Extract from or update the information to be written to the .info
# file of a Corpus Workbench corpus (or a list of corpora): the total
# number of sentences and the date of the last update.
#
# Usage: cwbdata-extract-info.sh [options] [corpus ... | --all] [> .info]
#
# For more information: cwbdata-extract-info.sh --help

# TODO: By default, backup the previous .info files when using
# --update; an option for omitting backups.


progname=`basename $0`

cwbdir=${CWBDIR:-/usr/local/cwb}
cwb_regdir=${CORPUS_REGISTRY:-/v/corpora/registry}
tmpdir=${TMPDIR:-${TEMPDIR:-${TMP:-${TEMP:-/tmp}}}}

update=
verbose=
test=
all_corpora=

if which wdiff &> /dev/null; then
    wdiff=wdiff
else
    wdiff=diff
fi

tmpfile=$tmpdir/$progname.$$.tmp


warn () {
    echo "$progname: Warning: $1" >&2
}

error () {
    echo "$progname: $1" >&2
    exit 1
}

echo_verb () {
    if [ "x$verbose" != "x" ]; then
	echo "$@"
    fi
}

cleanup () {
    rm -f $tmpfile
}

cleanup_abort () {
    cleanup
    exit 1
}


trap cleanup 0
trap cleanup_abort 1 2 13 15


usage () {
    cat <<EOF
Usage: $progname [options] [corpus ... | --all] [> .info]

Extract from or update the information to be written to the .info file
of a Corpus Workbench corpus (or a list of corpora): the total number
of sentences and the date of the last update. Corpus name arguments
may contain shell wildcards.

Options:
  -h, --help      show this help
  -c, --cwbdir DIR
                  use the CWB binaries in DIR (default: $cwb_bindir)
  -r, --registry DIR
                  use DIR as the CWB registry (default: $cwb_regdir)
  -t, --test      test whether the .info files need updating
  -u, --update    update the .info files for the corpora if needed
  -v, --verbose   show information about the processed corpora
  -A, --all       process all corpora in the CWB corpus registry
EOF
    exit 0
}


# Test if GNU getopt
getopt -T > /dev/null
if [ $? -eq 4 ]; then
    # This requires GNU getopt
    args=`getopt -o "hc:r:tuvA" -l "help,cwbdir:,registry:,test,update,verbose,all" -n "$progname" -- "$@"`
    if [ $? -ne 0 ]; then
	exit 1
    fi
    eval set -- "$args"
fi
# If not GNU getopt, arguments of long options must be separated from
# the option string by a space; getopt allows an equals sign.

# Process options
while [ "x$1" != "x" ] ; do
    case "$1" in
	-h | --help )
	    usage
	    ;;
	-c | --cwbdir )
	    cwbdir=$2
	    shift
	    ;;
	-r | --registry )
	    cwb_regdir=$2
	    shift
	    ;;
	-t | --test )
	    test=1
	    update=1
	    ;;
	-u | --update )
	    update=1
	    ;;
	-v | --verbose )
	    verbose=1
	    ;;
	-A | --all )
	    all_corpora=1
	    ;;
	-- )
	    shift
	    break
	    ;;
	--* )
	    warn "Unrecognized option: $1"
	    ;;
	* )
	    break
	    ;;
    esac
    shift
done


cwb_describe_corpus=
for path in $cwbdir/cwb-describe-corpus $cwbdir/bin/cwb-describe-corpus \
    `which cwb-describe-corpus 2> /dev/null`; do
    if [ -x $path ]; then
	cwb_describe_corpus=$path
	break
    fi
done
if [ "x$cwb_describe_corpus" = "x" ]; then
    error "cwb-describe-corpus not found in $cwbdir, $cwbdir/bin or on PATH; please specify with --cwbdir"
fi

if [ ! -d "$cwb_regdir" ]; then
    error "Cannot access registry directory $cwb_regdir"
fi

get_corpus_dir () {
    corpname=$1
    echo `
    $cwb_describe_corpus -r "$cwb_regdir" $corpname |
    grep '^home directory' |
    sed -e 's/.*: //'`
}

get_all_corpora () {
    ls "$cwb_regdir" |
    grep -E '^[a-z_-]+$'
}

extract_info () {
    corpdir=$1
    corpname=$2
    sentcount=`
    $cwb_describe_corpus -r "$cwb_regdir" -s $corpname |
    grep -E 's-ATT sentence +' |
    sed -e 's/.* \([0-9][0-9]*\) .*/\1/'`
    updated=`
    ls -lt --time-style=long-iso "$corpdir" |
    head -2 |
    tail -1 |
    awk '{print $6}'`
    echo "Sentences: $sentcount"
    echo "Updated: $updated"
}

tmpfile=$tmpdir/$progname.$$.tmp

if [ "x$all_corpora" != "x" ]; then
    corpora=`get_all_corpora`
else
    # Expand the possible shell wildcards in corpus name arguments
    corpora=`cd $cwb_regdir; echo $*`
fi

for corpus in $corpora; do
    if [ ! -e "$cwb_regdir/$corpus" ]; then
	warn "Corpus $corpus not found in registry $cwb_regdir"
	continue
    fi
    corpdir=`get_corpus_dir $corpus`
    if [ "x$update" = "x" ]; then
	echo_verb $corpus:
	extract_info $corpdir $corpus
    else
	extract_info $corpdir $corpus > $tmpfile
	outfile=$corpdir/.info
	if [ -e $outfile ] && cmp -s $tmpfile $outfile; then
	    echo_verb "$corpus up to date"
	else
	    if [ "x$test" != "x" ]; then
		echo "$corpus outdated"
		if [ "x$verbose" != "x" ]; then
		    $wdiff $outfile $tmpfile
		fi
	    else
		cp -p $tmpfile $outfile
		echo_verb "$corpus updated"
	    fi
	fi
    fi
done
