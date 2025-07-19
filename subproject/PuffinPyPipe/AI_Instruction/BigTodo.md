
Big TODO
=========

* We want to move to runner classes, using fozen dictionaries to create debug ETL paths through the same code as the full ETL
* debug ETL paths should be seperated at the schema level and not the table level.
* there is a post_import_scripts in every subdirectory for the raw imports. Instead there should be one post_import_scripts directory for the whole project. This way, all of the raw imports take place... then the subsequent steps are all ordered correctly.
* Switch to all lower-case table and column names. Otherwise we will be in "double qquote hell" because of Postgresql case sensitivity approach.
* Change the PECOS32423424 format to PECOS_234231243
