CHECK_CORE_FILE() {
    CORE_FILE="$(dirname $0)/core"
    if [[ -f "${CORE_FILE}" ]]; then
        . "${CORE_FILE}"
    else
        echo "!!! core file does not exist !!!"
        exit 1
    fi
}

DEFINITION_PATH() {
    LOCAL_PATH="${TASK_PATH}"
    if [[ -f "${TASK_PATH}" ]]; then
        REMOTE_PATH="${DRIVE_NAME}:${DRIVE_DIR}${DEST_PATH_SUFFIX%/*}"
    else
        REMOTE_PATH="${DRIVE_NAME}:${DRIVE_DIR}${DEST_PATH_SUFFIX}"
    fi
}

LOG_FILE="test.log"

UPLOAD(){
    echo "${LOCAL_PATH}" > "$LOG_FILE"
    python3 upload.py "${LOCAL_PATH}"
}

CHECK_CORE_FILE "$@"
CHECK_PARAMETER "$@"
CHECK_FILE_NUM
CHECK_SCRIPT_CONF
GET_TASK_INFO
GET_DOWNLOAD_DIR
CONVERSION_PATH
UPLOAD "$@"
CLEAN_UP
exit 0