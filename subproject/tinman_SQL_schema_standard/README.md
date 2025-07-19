TinMan SQL Naming Conventions
=========

Gievs structure to databases with heart. 

This document outlines which naming conventions from the style guide can or cannot currently be enforced using SQLFluff, and provides configuration settings for enforceable rules. This ruleset is a extension and merger of three different rulesets for SQL tables: 

* [https://x.com/sehrope](https://x.com/sehrope) wrote [How I Write SQL, Part 1: Naming Conventions](https://launchbylunch.com/posts/2014/Feb/16/sql-naming-conventions/)
* [DURC](https://github.com/ftrotter/durc_is_crud) naming conventions
* [SQLFluff default rules](https://docs.sqlfluff.com/en/stable/configuration/default_configuration.html)

We intend to write additional sqlfluff rules to support the rules that sqlfluff does not already support when possible. eventually. given infinite time and resources.

⸻

Rules Not Currently Enforceable by SQLFluff
------

These require either a custom rule, external linter, or manual review:

* Use full English words, not abbreviations
* Don’t use data types as names
* Use singular nouns for table names
* Primary key should be named id
* Foreign keys should follow the pattern <table>_id
  * Two foreign keys in the table requires a prefix on the foreign key column, to differentiate the two links. Like <helpfulname>_<table>_id etc.
  * Foreign keys can and will be created dynamically based on this naming convention. 
* Name indexes explicitly with table and column
* Name constraints clearly
* The varchar or text field in the table is assumed to be the "auto-suggest search" field for the table. If this is not true, then the table needs an explicit select_name field or postfixed field. 
* DURC Reserved names:
  * a column named select_name or that ends in _select_name is reserved for the field that will power an auto-suggest lookup on the table.
  * column names with a postfix of _markdown are used to invoke a front-end markdown editor
  * column names with a postfix of _code will invoke a code-editor on the front end. 

⸻

Rules Enforceable by SQLFluff
------

These can be configured using standard SQLFluff rules:
* Avoid quoted identifiers
	→ L014: Discourages use of quoted identifiers.
* Use all lowercase for identifiers
	→ L010: Enforces case on keywords and identifiers.
* Use underscores to separate words (snake_case)
	→ L040: Enforces naming convention patterns.
* Avoid reserved words as identifiers
	→ L036: Detects use of reserved keywords as identifiers.

⸻

.sqlfluff Configuration
----

```conf
[sqlfluff]
dialect = postgres

[sqlfluff:rules]
exclude_rules = L009  # Optional: skip alias prefixing if undesired

[sqlfluff:rules:L010]
capitalisation_policy = lower  # Force lowercase for identifiers

[sqlfluff:rules:L014]
extended_capitalisation_policy = lower  # Reinforce lowercase for quoted identifiers
ignore_words = ''  # Do not allow any exceptions

[sqlfluff:rules:L036]
# No config needed — enabled by default

[sqlfluff:rules:L040]
capitalisation_policy = lower
naming_convention = snake_case
```

