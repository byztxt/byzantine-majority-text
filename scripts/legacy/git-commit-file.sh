#!/bin/bash
#
# This script takes one argument, a filename/path to git add / git commit.
#
# The commit message will be:
#
# "Update to latest version. Original file date: MMM DD, YYYY"
#
# Written by Ulrik Sandborg-Petersen.
#
# Copyright (C) 2019  Ulrik Sandborg-Petersen.
#
# Released under the MIT License.
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

MESSAGE="Update to the latest version. Original file date: ${DATE}"

echo "Now git adding ${FILENAME}"
echo ""
git add ${FILENAME}

echo "Now git committing ${FILENAME} with commit message: '${MESSAGE}'"
echo ""
git commit -m "${MESSAGE}" ${FILENAME}

