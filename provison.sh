#!/usr/bin/env bash
mkdir -p parts

cd ${PWD}/parts
wget http://download.redis.io/releases/redis-3.0.7.tar.gz
tar xzf redis-3.0.7.tar.gz
cd redis-3.0.7 && make
