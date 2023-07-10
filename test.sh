a=$1
b=$2
c=$3

# echo "${a}"
# echo "${b}"
# echo "${c}"
LOG_FILE="output.log"
ECHO_TEST(){
    echo "${a}"
    echo "${b}"
    python3 test.py "$@"
}

ECHO_TEST "$@"
exit 0