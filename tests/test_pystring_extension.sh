#!/usr/bin/env bash

python ./babar/examples/pystring.py
make install

psql -d postgres <<SQL
DROP EXTENSION IF EXISTS pystring;
CREATE EXTENSION pystring;

select pyjoin(array ['a', 'b'], ', ');

SQL