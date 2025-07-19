# PuffinPyPipe

A Python Library that uses CSViper to import Public Use Files (PUFs) into PostGreSQL.
There eventually will be a readme in each project directory detailing the source of data, and how it works etc etc.
In many cases there are other programs that need to be run in order to obtain the data csv files needed by this project.

## General Concepts

* The subdirectories are for the various Public Use Files. They are self-contained scripts created by [CSViper](https://github.com/ftrotter/csviper).
* The .gitignore will assume that any ./?/?/data subdirectory is excluded, so that it is safe to have the data in the project tree.
* We are also assuming that the database credentials will live in .env in the parent directory.
* This project was born from similar code that generated MySQL import scripts in this manner, but for now CSViper is focused only on PostGreSQL imports. YMMV if you try to use the legacy MySQL scripts.

## How it works

* csviper can compile a database import script from a csv source and knows how to run those scripts
* First it generates a data model, which can be tweaked before being compiled into an import script
* Then it generates an import script, which can be tweaked before being run. This script takes an "All VARCHAR" approach to the import process and expects data typing to be handled by post import SQL or scripts.
* finally, there is a stand-alone python import script for each project (go.postgresql.py) which can be run without csviper.
* There is space for custom raw-swl in each project under the /{subproject}/post_import_sql/ directory. When ETL data tweaks are simple, this can be enough.
* Subsequent runs of the import script can be directed at new data files using a pattern match for the expected file name
* There are "runner" scripts in the main directory that invoke the csviper compile process and run the import scripts, which expect configuration data from setup.env

## Running the project

* Make a copy of setup.env.example and put the needed datafiles in the right place.
* Custom ETL for each project currently lives under /{subproject}/post_import_scripts/
* These scripts will soon be put into one place, but for now they have to be run in a "just so" in order to get them to work. 
* These scripts should be fully idempotent, but likely are not completely there yet. 
* Eventually these will be fully ordered out, but for now they must be run in the following order

## Import Script ordering

Perform the raw imports on all the scripts. All the "compile" and "invoke" scripts need to be run first
Then run the post_import_scripts in the following order

* ./nucc/post_import_scripts/Step05_fix_column_types.py
* ./
* ./nppes_main/post_import_scripts/before_pecos.sh
* ./