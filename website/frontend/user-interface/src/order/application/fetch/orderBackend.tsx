import {
    doUtcDate,
    getCredentialCookie,
    HTTP_AUTH_HEADERS, HTTP_JSON_HEADERS_WITH_AUTH, HTTP_METHOD_DELETE,
    HTTP_METHOD_GET,
    HTTP_METHOD_POST,
    HTTP_STATUS_CREATED,
    HTTP_STATUS_OK,
    ORDER_CREATE, ORDER_DELETE,
    ORDER_INFO,
    REQUEST_URL
} from "../../../global/constants/constants";
import {notifications} from "@mantine/notifications";
import {IconX} from "@tabler/icons-react";

export function getOrders() {
    return Promise.all([getOrderInfo()])
}

function getOrderInfo() {
    return fetch(REQUEST_URL + ORDER_INFO,
        {
            method: HTTP_METHOD_GET,
            headers: HTTP_AUTH_HEADERS(getCredentialCookie())
        })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                alert("Nope")
                return;
            }
            return response.json()
        })
        .then((data) => {
            if (data) {
                return data;
            }
            return [];
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

export function saveOrder(data: {website_name: string, url: string, request_method: string, request_body: string, request_header: string, starting_date: Date, intervall_time: number, repetitions: number, termsOfService: boolean}) {
    const dataToSend = {
        name: data.website_name,
        url: data.url,
        starting_time: data.starting_date.getTime(),
        intervall_time: data.intervall_time,
        repetitions: data.repetitions,
        request_method: data.request_method,
        request_body: data.request_body,
        request_header: data.request_header
    }

    fetch(REQUEST_URL + ORDER_CREATE, {
        method: HTTP_METHOD_POST,
        headers: HTTP_JSON_HEADERS_WITH_AUTH(getCredentialCookie()),
        body: JSON.stringify(dataToSend)
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_CREATED) {
                alert("Nope");
                return;
            }
            return response.json()
        })
        .then((data) => {
            if (data) {
                window.location.reload();
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

export function deleteOrder(dataUuid: string) {
    const data = {
        uuid: dataUuid
    }
    fetch(REQUEST_URL + ORDER_DELETE, {
        method: HTTP_METHOD_DELETE,
        headers: HTTP_JSON_HEADERS_WITH_AUTH(getCredentialCookie()),
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.status !== HTTP_STATUS_OK) {
                alert("Nope")
                return;
            }
            return response.json();
        })
        .then((data) => {
            if (data) {
                window.location.reload();
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