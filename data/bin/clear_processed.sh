#!/usr/bin/env bash

mongo --eval "db.processed_tweets.deleteMany({})"