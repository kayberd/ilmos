// COLORS
enum IlmosColors {
  RED = '#E84141',
  YELLOW = '#E8E841',
  GREY = '#969696',
  GREEN = '#41E894',
}

// ENDPOINT CONSTANTS
enum Networking {
  BASE_URL = 'http://144.122.71.38:8080/',
  OCCUPATIONS = 'occupations/',
  OCCUPATION = 'occupation/',
  OCCUPY = 'occupy/',
  RELEASE = 'release/',
  SEATS = 'seats/',
  SEAT = 'seat/',
  USERS = 'users/',
  SCAN_ALLOWED = 'scan-allowed/',
  QUEUE_SIZE = 'queue-size/',
  QUEUE_INDEX = 'queue-index/',
  ENQUEUE = 'enqueue/',
  DEQUEUE = 'dequeue/',
  NEW_USER = 'new-user/',
  IN_QUEUE = 'in-queue/',
}
enum DashboardColors {
  TAKEN_COLOR = IlmosColors.RED,
  BREAK_COLOR = IlmosColors.YELLOW,
  VACANT_COLOR = IlmosColors.GREEN,
  DISABLED_COLOR = IlmosColors.GREY,
}
enum QRResponseTexts {
  OCCUPY_SUCCESS = 'Success',
  SAME_USER_DIFF_SEATS = 'Same user cannot be seated on different seats!',
  SEAT_NOT_EMPTY = 'Seat is not empty!',
}

enum UserStatusText {
  WORKING = 'Working...',
  BREAK = 'Refreshing...',
  //TODO: QUEUE
}

enum TimerText {
  WORKING = 'Great Work Hocam!',
  BREAK = 'Come Back To Seat!',
}

enum ButtonText {
  LEAVE_QUEUE = 'Leave Queue',
  ENDSESSION = 'End Session',
  ENTER_QUEUE = 'Queue up now!',
}

enum Notifications {
  APP_ID = '7624b802-16e2-454b-a759-856384f5382d',
  QUEUE_TURN_TITLE = 'Hurry up!',
}

enum DeskStatus {
  TAKEN = 'TAKEN',
  BREAK = 'BREAK',
}
enum ProfileScreenTexts {
  NO_SESSION_TEXT = 'You should start to study',
}

enum QrScreenTexts {
  ON_SESSION_TEXT = "You've already taken a seat",
}

// NUMERIC CONSTANTS
const MAX_SEAT_NUM = 16;
const TABLE_CAPACITY = 4;
const REFRESH_PERIOD = 200;
const MAX_BREAK_MIN = 15 * 60 * 1000;
const REQUEST_HEADER = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
};

export {
  IlmosColors,
  Networking,
  DashboardColors,
  QRResponseTexts,
  UserStatusText,
  DeskStatus,
  ButtonText,
  TimerText,
  ProfileScreenTexts,
  QrScreenTexts,
  MAX_SEAT_NUM,
  TABLE_CAPACITY,
  REFRESH_PERIOD,
  REQUEST_HEADER,
  MAX_BREAK_MIN,
  Notifications,
};
