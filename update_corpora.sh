#!/bin/bash
#
# This script clones the Git repository for Darius Kazemi's corpora
# project and copies all the data files to olipy/data/corpora. The resulting
# data is then committed to the olipy repository.
#
# Currently this is the most reliable way to make sure olipy ships
# with _some_ version of corpora, even though it probably won't be the
# latest version by the time olipy is installed.
#
# For history, see:
# https://github.com/aparrish/pycorpora/issues/8#issuecomment-386848837
#
CORPORA_REPO='https://github.com/dariusk/corpora'
CORPORA_REPO_DIR='corpora-original-repo'
CORPORA_DEST_DIR='olipy/data/corpora-original'
rm -rf $CORPORA_REPO_DIR
git clone $CORPORA_REPO $CORPORA_REPO_DIR
rsync -avp $CORPORA_REPO_DIR/data $CORPORA_DEST_DIR
cd $CORPORA_REPO_DIR
CORPORA_REV=`git rev-parse HEAD`
cd ..
rm -rf $CORPORA_REPO_DIR
git add $CORPORA_DEST_DIR
git commit -am "Brought corpora-original up to date with $CORPORA_REPO revno $CORPORA_REV"

