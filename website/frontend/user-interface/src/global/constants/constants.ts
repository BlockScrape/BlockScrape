import Cookies from "universal-cookie";

const REQUEST_URL = 'http://localhost:6543',
    USER_URL = '/user',
    LOGIN_TOKEN = '/token',
    TOKEN_EXPIRE_HOURS = 10,
    USER_CREATE_URL = USER_URL + '/create',
    VALIDATE_TOKEN = USER_URL + '/me',
    ORDER_URL = '/order',
    ORDER_INFO = ORDER_URL + '/info',
    ORDER_CREATE = ORDER_URL + '/create',
    ORDER_DELETE = ORDER_URL + '/delete',
    COIN_URL = '/coin',
    COIN_INFO = COIN_URL + '/info'

const HTTP_STATUS_OK = 200,
HTTP_STATUS_CREATED = 201,
HTTP_METHOD_POST = "POST",
HTTP_METHOD_PUT = "PUT",
HTTP_METHOD_DELETE = "DELETE",
HTTP_METHOD_GET = "GET";

const HTTP_JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

const HTTP_JSON_HEADERS_WITH_AUTH = (auth_token: string) => {
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    };
};

const HTTP_AUTH_HEADERS = (auth_token: string) => {
    return {
        'Authorization': 'Bearer ' + auth_token
    };
}

function setCredentialCookie(value: string, expires: number) {
    const cookies = new Cookies()
    let date = new Date();
    date.setTime(date.getTime() + (expires * 60 * 60 * 1000))
    cookies.set("token", value, {expires: date, path: '/'})
}

function getCredentialCookie() {
    const cookies = new Cookies()
    return cookies.get("token");
}

function doUtcDate(date: Date) {
    let year = "" + date.getFullYear()
    let day = ""
    let month = ""
    let hour = ""
    let minute = ""
    let second = ""
    if (date.getDate() < 10) {
        day = "0" + date.getDate()
    } else {
        day = "" + date.getDate()
    }
    if (date.getMonth() < 10) {
        month = "0" + date.getMonth()
    } else {
        month = "" + date.getMonth()
    }
    if (date.getHours() < 10) {
        hour = "0" + date.getHours()
    } else {
        hour = "" + date.getHours()
    }
    if (date.getMinutes() < 10) {
        minute = "0" + date.getMinutes()
    } else {
        minute = "" + date.getMinutes()
    }
    if (date.getSeconds() < 10) {
        second = "0" + date.getSeconds()
    } else {
        second = "" + date.getSeconds()
    }


    let dateString = year + "-" + month + "-" + day
    let timeString = "T" + hour + ":" + minute + ":" + second
    let timeZoneString = "+00:00"
    let utcDateString = dateString + timeString + timeZoneString
    return new Date(utcDateString)
}

export {
    REQUEST_URL,
    LOGIN_TOKEN,
    USER_CREATE_URL,
    ORDER_CREATE,
    ORDER_INFO,
    ORDER_DELETE,
    COIN_INFO,
    HTTP_METHOD_POST,
    HTTP_METHOD_PUT,
    HTTP_STATUS_CREATED,
    HTTP_METHOD_GET,
    HTTP_AUTH_HEADERS,
    HTTP_JSON_HEADERS,
    HTTP_JSON_HEADERS_WITH_AUTH,
    HTTP_METHOD_DELETE,
    HTTP_STATUS_OK,
    TOKEN_EXPIRE_HOURS,
    VALIDATE_TOKEN,
    doUtcDate,
    setCredentialCookie,
    getCredentialCookie
}