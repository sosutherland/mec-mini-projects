# JSON data to RDMBS

The python script quote_db.py has three functions.

Use `-c` or `--create` to create the database in quote.db.

Use `-s` or `--store` to store the JSON data from xpath-scraper-result.json into the database.

Use `-q` with a sql statement to query the database.

## SQLLite3 table schema

| **quote**    |
|--------------|
| quote_id     |
| quote_text   |
| quote_author |

| **tag**  |
|----------|
| tag_id   |
| quote_id |
| tag_text |

## Examples

### Get all quotes from an author
`python quotes_db.py -q "SELECT quote_id, quote_text FROM quote WHERE quote_author = 'Ernest Hemingway'"`

### Get all tags for a quote
`python quotes_db.py -q "SELECT tag_text FROM tag WHERE quote_id = 58"`

### Get all authors for a tag
`python quotes_db.py -q "SELECT quote_author FROM quote JOIN tag ON quote.quote_id = tag.quote_id WHERE tag_text = 'friends'"`