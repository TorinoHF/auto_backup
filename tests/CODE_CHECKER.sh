#!/bin/bash

# Define bold color codes
BOLD_YELLOW='\033[1;33m'
BOLD_RED='\033[1;31m'
BOLD_GREEN='\033[1;32m'
BOLD='\033[1m'
NC='\033[0m' # No Color (reset)

declare -a FILES=() 
# add all files ending with .py to FILES
FILES=$(find . -name '*.py' -a -not -path './tests/*')

test-pylint() {
    for FILE in $FILES; do
        echo -e "${BOLD}CHECKING${NC}: $FILE"
        # Run Pylint
        echo -e "${BOLD_YELLOW}CHECKING WITH PYLINT${NC}"
        pylint $FILE
        if [ $? -ne 0 ]; then
            echo -e "${BOLD_RED}PYLINT CHECK FAILED!${NC}"
            exit 1
        fi
    done
}

test-flake8() {
    for FILE in $FILES; do
        echo -e "${BOLD}CHECKING${NC}: $FILE"
        # Run Flake8
        echo -e "${BOLD_YELLOW}CHECKING WITH FLAKE8${NC}"
        if [ $? -ne 0 ]; then
            echo -e "${BOLD_RED}FLAKE8 CHECK FAILED!${NC}"
            exit 1
        fi
    done
}

test-all() {
    test-pylint
    test-flake8
}

# Check parameters
[[ $# == 0 ]] && test-all
while [[ $# -gt 0 ]]; do
    case "$1" in

    all) test-all ;;
    pylint) test-pylint ;;
    flake8) test-flake8 ;;

    --help)
        echo "run_tests.sh: entrypoint to launch tests locally or on CI"
        echo ""
        echo "Normal usage:"
        echo "    run_tests.sh [parameters] [test|all]   # no arguments: test all!"
        echo ""
        echo "Specific tests:"
        echo "    run_tests.sh pylint                    # test with pylint"
        echo "    run_tests.sh flake8                    # test with flake8"
        echo ""
        echo "Parameters:"
        echo "    --help                                 # print this help"
        exit 1
        ;;
    *)
        echo "Unknown option: $1"
        exit 2
        ;;
    esac
    shift
done
