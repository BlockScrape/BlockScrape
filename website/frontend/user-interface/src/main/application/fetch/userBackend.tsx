import {
    getCredentialCookie,
    HTTP_AUTH_HEADERS,
    HTTP_METHOD_GET, HTTP_STATUS_OK,
    REQUEST_URL,
    USER_INFO
} from "../../../global/constants/constants";
import {notifications} from "@mantine/notifications";
import {IconX} from '@tabler/icons-react';

export function getUser() {

    return fetch(REQUEST_URL + USER_INFO, {
        method: HTTP_METHOD_GET,
        headers: HTTP_AUTH_HEADERS(getCredentialCookie())
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "get-user-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Cannot Validate User Token, Try to Logout",
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
                id: "register-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}