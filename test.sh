a=$1

# echo "${a}"
# echo "${b}"
# echo "${c}"
LOG_FILE="output.log"
ECHO_TEST(){
    echo "${a}" >> "$LOG_FILE"
    python3 upload.py "$@"
}

ECHO_TEST "$@"
exit 0