#!/usr/bin/env bash

VERSION=15.0.1

INITIAL_ENV=env

PYTHON=/usr/bin/python3

URL_BASE=https://pypi.python.org/packages/source/v/virtualenv

wget ${URL_BASE}/virtualenv-${VERSION}.tar.gz

tar xzf virtualenv-${VERSION}.tar.gz

${PYTHON} virtualenv-${VERSION}/virtualenv.py ${INITIAL_ENV}

rm -rf virtualenv-${VERSION}

${INITIAL_ENV}/bin/pip install virtualenv-${VERSION}.tar.gz