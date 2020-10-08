#!/bin/bash

#http://dan.doezema.com/2013/04/programmatically-create-title-tabs-within-the-mac-os-x-terminal-app/

function new_tab() {
  TAB_NAME=$1
  COMMAND=$2
  osascript \
    -e "tell application \"Terminal\"" \
    -e "tell application \"System Events\" to keystroke \"t\" using {command down}" \
    -e "do script \"printf '\\\e]1;$TAB_NAME\\\a'; $COMMAND\" in front window" \
    -e "end tell" > /dev/null
}

new_tab "Jenkins" "cd ./toolsdir; ./jenkins-start.sh"
new_tab "Nexus IQ Server" "cd ./toolsdir; ./nexus-iq-server-start.sh"
new_tab "Nexus Repo 3" "cd ./toolsdir; ./nexus3-start.sh"
new_tab "SonarQube" "cd ./toolsdir; ./sonarqube-start.sh"

