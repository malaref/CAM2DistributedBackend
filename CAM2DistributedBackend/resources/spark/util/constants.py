# The timeout used for downloading a single image in seconds.
DOWNLOAD_TIMEOUT = 5

# Names of files/directories related to both the manager and the worker.
SUBMISSIONS_DIR_NAME = 'submissions/'
SOURCE_CODE_DIR_NAME = 'src/'
RESULTS_DIR_NAME = 'results/'

# Names of files/directories related to the manager.
MANAGER_CAM2_PATH = '/home/akaseb/BigData/system/cam2/'
MANAGER_API_FILE_PATH = MANAGER_CAM2_PATH + 'manager_api.py'
MANAGER_UPDATE_SUBMISSION_STATE_PATH = MANAGER_CAM2_PATH + \
                                       'update_submission_state.py'
MANAGER_UPDATE_WORKLOAD_PATH = MANAGER_CAM2_PATH + 'update_workload.py'
MANAGER_UPDATE_RESOURCES_PATH = MANAGER_CAM2_PATH + 'update_resources.py'
MANAGER_SUBMISSIONS_DIR_PATH = '/home/akaseb/cam2/submissions/'
MANAGER_TEMP_DIR_PATH = '/home/akaseb/cam2/temp/'
SSH_KEYS_DIR_PATH = '/home/akaseb/cam2/cloud_keys/'
WORKERS_REQUESTS_DIR_NAME = 'workers_requests/'

# Names of files/directories related to the worker.
WORKER_API_PATH = 'cam2/worker_api.py'
SUBMISSION_PROCESSES_FILE_NAME = 'submission_processes.pkl'
CAM2_API_PATH = 'cam2/core/worker/api/'
SUBMITTED_MODULE_NAME = 'main'
WORKER_USER_NAME = 'worker'

# The names of the request files.
REQUEST_EXTENSION = '.json'
USER_REQUEST_FILE_NAME = 'user_request' + REQUEST_EXTENSION
WORKER_REQUEST_FILE_NAME = 'worker_request' + REQUEST_EXTENSION

# The specifications of the error log files due to the analysis.
ERROR_FILE_EXTENSION = '.txt'
INITIALIZATION_ERROR_FILE_PREFIX = 'initialization_error_'
FRAME_ERROR_FILE_PREFIX = 'frame_error_'
FINALIZATION_ERROR_FILE_PREFIX = 'finalization_error_'
ERROR_FILE_PREFIX = 'error_'
ERROR_FILE_DATE_FORMAT = '_%Y-%m-%d_%H-%M-%S'
EXCEPTION_TRACE_PATTERN = 'src/main.py", '
CLASS_NAME_ERROR_MESSAGE = 'The submitted class name must be "MyAnalyzer".'
INACTIVE_CAMERA_ERROR_MESSAGE = 'This camera is currently inactive.'

# The possible states of a submission.
ALLOCATING_RESOURCES_SUBMISSION_STATE = 'Allocating resources'
RUNNING_SUBMISSION_STATE = 'Running'
COMPLETED_SUBMISSION_STATE = 'Completed'
TERMINATED_SUBMISSION_STATE = 'Terminated'
ABNORMALLY_TERMINATED_SUBMISSION_STATE = 'Abnormally terminated'

# The names of the events between the manager and the worker.
ON_NEW_SUBMISSION_EVENT = 'on_new_submission'
GET_SUBMISSION_RESULTS_EVENT = 'get_submission_results'
TERMINATE_SUBMISSION_EVENT = 'terminate_submission'
UPDATE_SUBMISSION_STATE = 'update_submission_state'
UPDATE_RESOURCES = 'update_resources'
UPDATE_WORKLOAD = 'update_workload'
TERMINATE_CAMERAS = 'terminate_cameras'
ADD_CAMERAS = 'add_cameras'

# The attributes of the JSON request file.
SUBMISSION_ID_ATTRIBUTE = 'submission_id'
PROGRAM_ATTRIBUTE = 'program'
TIMESTAMP_ATTRIBUTE = 'timestamp'
INTERVAL_ATTRIBUTE = 'interval'
DURATION_ATTRIBUTE = 'duration'
SNAPSHOTS_TO_KEEP_ATTRIBUTE = 'snapshots_to_keep'
IS_VIDEO_ATTRIBUTE = 'is_video'
MANAGER_HOST_NAME_ATTRIBUTE = 'manager_host_name'
CAMERAS_ATTRIBUTE = 'cameras'
CAMERA_TYPE_ATTRIBUTE = 'type'
CAMERA_TYPE_IP = 'ip'
CAMERA_TYPE_NON_IP = 'non_ip'
CAMERA_KEY_ATTRIBUTE = 'key'
CAMERA_IP_ATTRIBUTE = 'ip'
CAMERA_PORT_ATTRIBUTE = 'port'
CAMERA_RESOLUTION_ATTRIBUTE = 'resolution'
CAMERA_SNAPSHOT_PATH_ATTRIBUTE = 'snapshot_path'
CAMERA_MJPG_PATH_ATTRIBUTE = 'mjpg_path'
CAMERA_SNAPSHOT_URL_ATTRIBUTE = 'snapshot_url'
CAMERA_LATITUDE_ATTRIBUTE = 'latitude'
CAMERA_LONGITUDE_ATTRIBUTE = 'longitude'
CAMERA_RESOLUTION_WIDTH_ATTRIBUTE = 'resolution_width'
CAMERA_RESOLUTION_HEIGHT_ATTRIBUTE = 'resolution_height'

# The types of cloud instances.
AMAZON_INSTANCE_TYPE = 'amazon'
PURDUE_INSTANCE_TYPE = 'purdue'

# The minimum resolution of a downloaded snapshots.
MINIMUM_RESOLUTION_WIDTH = 32
MINIMUM_RESOLUTION_HEIGHT = 32

INIT_TRIALS = 5
REOPEN_STREAM_INTERVAL = 5
LOG_ERRORS = True

HIGH_THRESHOLD = 0.9
TARGET_THRESHOLD = 0.7
LOW_THRESHOLD = 0.4
