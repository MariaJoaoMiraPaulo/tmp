#!/bin/bash

case $1 in 
"build")
    cd docker && docker build -t subject_analyzer_image .
    ;;
"remove")
    EXISTS=$(docker ps -a | grep -E subject_analyzer_container)
    echo $EXISTS
    if [ -n "$EXISTS" ]; then
        docker rm subject_analyzer_container
    fi
    ;;
"stop")
    RUNING=$(docker ps | grep subject_analyzer_container)
    if [ -n "$RUNING" ]; then
        docker stop subject_analyzer_container
    fi
    ;;
"run")
    docker run -d -v $(pwd):/app --name subject_analyzer_container -p 5000:5000 subject_analyzer_image
    ;;
esac