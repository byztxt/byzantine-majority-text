#!/bin/bash
#
# This script takes one argument, a filename/path to git add / git commit.
#
# The commit message will be:
#
# "Update to latest version. Dr. Robinson's file date: MMM DD, YYYY"
#

FILENAME="$1"

if test "x${FILENAME}" = "x"; then
    echo "Please specify a filename to git add / commit."
    exit 1;
fi

if test -f ${FILENAME}; then
    echo "About to git add / git commit ${FILENAME}";
    echo "";
else
    echo "Not commiting ${FILENAME}, as it is not a regular file."
    exit 1;
fi

DATE=`ls -l ${FILENAME} | awk '{print $6 " " $7 ", " $8;}'`

MESSAGE="Update to the latest version from Dr. Robinson. His original file date: ${DATE}"

echo "Now git adding ${FILENAME}"
echo ""
git add ${FILENAME}

echo "Now git committing ${FILENAME} with commit message: '${MESSAGE}'"
echo ""
git commit -m "${MESSAGE}" ${FILENAME}

