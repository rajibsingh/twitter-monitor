#!/usr/bin/env bash

7z e -odata/dumps data/dumps/authors_tweets.7z
mongoimport --db tweetsdb --collection tweets --file data/dumps/tweets.json
mongoimport --db tweetsdb --collection authors --file data/dumps/authors.json
rm data/dumps/tweets.json
rm data/dumps/authors.json