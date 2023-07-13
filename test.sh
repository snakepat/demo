a=$1

# echo "${a}"
# echo "${b}"
# echo "${c}"
LOG_FILE="output.log"
ECHO_TEST(){
    echo "${a}" >> "$LOG_FILE"
    python3 upload.py "$@"
}

CHECK_CORE_FILE
ECHO_TEST "$@"
exit 0


CHECK_CORE_FILE() {
    CORE_FILE="/root/.aria2c/core"
    if [[ -e "${CORE_FILE}" ]]; then
        echo "can find core" >> "$LOG_FILE"