#!/bin/sh

mongosh "localhost:27017" <<EOF
use db1
db.createCollection("students")
quit
EOF
