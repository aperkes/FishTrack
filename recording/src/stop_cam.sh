#!/bin/bash

pid=$(pgrep -f raspistill)
kill $pid
