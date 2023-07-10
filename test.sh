a=$1
b=$2
c=$3

# echo "${a}"
# echo "${b}"
# echo "${c}"

ECHO_TEST(){
    python3 test.py
}

ECHO_TEST "$@"
exit 0