#!/bin/bash

docker run -it --rm --net=host -v ./grafana/defaults.ini:/usr/share/grafana/conf/defaults.ini grafana/grafana-oss:latest