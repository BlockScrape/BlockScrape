import {
    doUtcDate,
    HTTP_JSON_HEADERS,
    HTTP_METHOD_POST, HTTP_STATUS_CREATED,
    HTTP_STATUS_OK,
    LOGIN_TOKEN, LOGIN_TOKEN_MFA,
    REQUEST_URL,
    TOKEN_EXPIRE_HOURS, USER_CREATE_URL, VERIFY_MFA
} from "../global/constants/constants";
import {setCredentialCookie} from "../global/constants/constants";
import {notifications} from "@mantine/notifications";
import {IconCheck, IconX} from "@tabler/icons-react";


export function login_mfa(username: string, passwd: string, mfa_key: string) {
    let formdata = new FormData();
    formdata.append("username", username);
    formdata.append("password", passwd);
    formdata.append("client_secret", mfa_key);
    fetch(REQUEST_URL + LOGIN_TOKEN_MFA, {method: HTTP_METHOD_POST, body: formdata})
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "login-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Could not Validate User Credentials",
                    icon: <IconX/>,
                    color: "red"
                });
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
        .catch(rejected => {
            console.log(rejected)
            notifications.show({
                id: "server-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}


export function verify_mfa(username: string, mfa_key: string) {
    const dataToSend = {
        username: username,
        mfa_key: mfa_key
    }
    return fetch(REQUEST_URL + VERIFY_MFA, {
        method: HTTP_METHOD_POST,
        headers: HTTP_JSON_HEADERS,
        body: JSON.stringify(dataToSend)
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "verify-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Could not Validate User Credentials",
                    icon: <IconX/>,
                    color: "red"
                });
                return;
            }
            return response.json();
        })
        .catch(rejected => {
            console.log(rejected)
            notifications.show({
                id: "server-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}


export function login(username: string, passwd: string) {
    let formdata = new FormData();
    formdata.append("username", username);
    formdata.append("password", passwd);
    return fetch(REQUEST_URL + LOGIN_TOKEN, {method: HTTP_METHOD_POST, body: formdata})
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "login-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Could not Validate User Credentials",
                    icon: <IconX/>,
                    color: "red"
                });
                return;
            }
            return response.json();
        })
        .catch(rejected => {
            console.log(rejected)
            notifications.show({
                id: "server-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });

}

export function register(value: {
    first_name: string,
    last_name: string,
    birthdate: Date,
    username: string,
    email: string,
    password: string,
    termsOfService: boolean
}) {
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
        .then(response => {
            if (response.status !== HTTP_STATUS_CREATED) {
                notifications.show({
                    id: "register-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Cannot Validate User Token",
                    icon: <IconX/>,
                    color: "red"
                });
                return;
            }
            notifications.show({
                id: "register-okay",
                withCloseButton: true,
                title: "Okay",
                message: "REGISTERED",
                icon: <IconCheck/>,
                color: "green"
            });
            return response.json();
        })
        .then((data) => {
            if (data) {
                window.location.replace(window.location.origin);
            }
        })
        .catch(rejected => {
            console.log(rejected)
            notifications.show({
                id: "register-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}
