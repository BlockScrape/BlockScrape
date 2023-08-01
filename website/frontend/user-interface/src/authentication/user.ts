import Cookies from "universal-cookie";
import {
    doUtcDate,
    HTTP_JSON_HEADERS,
    HTTP_METHOD_POST, HTTP_STATUS_CREATED,
    HTTP_STATUS_OK,
    LOGIN_TOKEN,
    REQUEST_URL,
    TOKEN_EXPIRE_HOURS, USER_CREATE_URL
} from "../global/constants/constants";
import {setCredentialCookie, getCredentialCookie} from "../global/constants/constants";


export function login(username: string, passwd: string) {
    let formdata = new FormData();
    formdata.append("username", username);
    formdata.append("password", passwd);
    fetch(REQUEST_URL + LOGIN_TOKEN, {method: HTTP_METHOD_POST, body: formdata})
        .then(response => {
            if (response.status != HTTP_STATUS_OK) {
                alert("Nope")
                return;
            }
            return response.json();
        })
        .then((data) => {
            if (data) {
                setCredentialCookie(data.access_token, TOKEN_EXPIRE_HOURS);
                window.location.reload();
            }
        })

}

export function register(value: { first_name: string, last_name: string, birthdate: Date, username: string, email: string, password: string, termsOfService: boolean }) {
    const data = {
        firstname: value.first_name,
        lastname: value.last_name,
        username: value.username,
        passwd: value.password,
        email: value.email,
        birthdate: doUtcDate(value.birthdate).getTime()
    };
    fetch(REQUEST_URL + USER_CREATE_URL, {
        method: HTTP_METHOD_POST,
        headers: HTTP_JSON_HEADERS,
        body: JSON.stringify(data)
    })
        .then( response => {
            if(response.status != HTTP_STATUS_CREATED) {
                alert("NOPE");
                return;
            }
            return response.json();
        })
        .then((data) => {
            if(data) {
                window.location.reload();
            }
        })
}
