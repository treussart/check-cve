#!/usr/bin/env bash

WORKING_DIR="$(dirname "$0")"/

cd "${WORKING_DIR}" || exit 1

function init() {
  export PYTHONPATH=$PYTHONPATH:"${WORKING_DIR}"/check_cve
}

function check() {
  flake8 "${WORKING_DIR}"/check_cve
  result_flake8="$?"
  if [ "$result_flake8" -ne 0 ]; then
      echo "Tests failed : PEP-8 Not Compliant"
      exit "$result_flake8"
  fi
}

function usage() {
    echo "Run tests"
    printf "\\t-h --help\\n"
    printf "\\t-s --check\\n"
    printf "\\t-a --all\\n"
    printf "\\n"
    printf "Examples:\\n"
    printf "\\t./test.sh -s\\n"
}


while [ "$1" != "" ]; do
    PARAM=$(echo "$1" | awk -F= '{print $1}')
    # VALUE=$(echo "$1" | awk -F= '{print $2}')
    case $PARAM in
    -h | --help)
        usage
        exit
        ;;
    -s | --check)
        check
        exit
        ;;
    -a | --all)
        init
        check
        exit
        ;;
    *)
        echo "ERROR: unknown parameter \"$PARAM\""
        usage
        exit 1
        ;;
    esac
    shift
done

init
check
