import {
    COIN_INFO, COIN_UPDATE,
    getCredentialCookie,
    HTTP_AUTH_HEADERS, HTTP_JSON_HEADERS_WITH_AUTH,
    HTTP_METHOD_GET, HTTP_METHOD_PUT, HTTP_STATUS_OK,
    REQUEST_URL
} from "../../../global/constants/constants";
import {notifications} from "@mantine/notifications";
import {IconCheck, IconX} from "@tabler/icons-react";

export function getCoinStatus() {
    return fetch(REQUEST_URL + COIN_INFO, {
        method: HTTP_METHOD_GET,
        headers: HTTP_AUTH_HEADERS(getCredentialCookie())
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "get-coin-error",
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
                id: "coin-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}

export function updateCoinStatus(addition: number) {
    const data_to_send = {
        "addition": addition
    }
    return fetch(REQUEST_URL + COIN_UPDATE, {
        method: HTTP_METHOD_PUT,
        headers: HTTP_JSON_HEADERS_WITH_AUTH(getCredentialCookie()),
        body: JSON.stringify(data_to_send)
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                notifications.show({
                    id: "update-coin-error",
                    withCloseButton: true,
                    title: "Error",
                    message: "Cannot Validate User Token, Try to Logout",
                    icon: <IconX/>,
                    color: "red"
                });
            } else {
                notifications.show({
                    id: "update-coin-successful",
                    withCloseButton: true,
                    title: "Updated",
                    message: "Coin Value Updated",
                    icon: <IconCheck/>,
                    color: "green"
                })
                window.location.reload()
            }
        })
        .catch(rejected => {
            console.log(rejected)
            notifications.show({
                id: "coin-error",
                withCloseButton: true,
                title: "Error",
                message: "Backend not Reachable",
                icon: <IconX/>,
                color: "red"
            });
        });
}