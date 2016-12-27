#!/usr/bin/env bash

mongoexport --db tweetsdb --collection tweets --out data/dumps/tweets.json