#!/usr/bin/env bash

rm data/dumps/authors_tweets.7z

mongoexport --db tweetsdb --collection tweets --out data/dumps/tweets.json
mongoexport --db tweetsdb --collection authors --out data/dumps/authors.json

7z a data/dumps/authors_tweets.7z data/dumps/authors.json data/dumps/tweets.json

rm data/dumps/tweets.json
rm data/dumps/authors.json