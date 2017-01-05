#!/usr/bin/env bash

mongoexport --db tweetsdb --collection tweets --out data/dumps/tweets.json
mongoexport --db tweetsdb --collection authors --out data/dumps/authors.json