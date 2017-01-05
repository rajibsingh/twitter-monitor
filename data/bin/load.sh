#!/usr/bin/env bash

mongoimport --db test --collection tweets --file data/dumps/tweets.json
mongoimport --db test --collection authors --file data/dumps/authors.json