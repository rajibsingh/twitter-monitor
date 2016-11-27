#!/bin/bash

mongoexport --db tweetsdb --collection tweets --out dumps/tweets.json

mongoimport --db test --collection tweets --file dumps/tweets.json

