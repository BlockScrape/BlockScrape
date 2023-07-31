import {
    getCredentialCookie,
    HTTP_AUTH_HEADERS,
    HTTP_METHOD_GET, HTTP_STATUS_OK,
    ORDER_INFO,
    REQUEST_URL
} from "../../../global/constants/constants";
import {constants} from "http2";

export function getOrders(){
    return Promise.all([getOrderInfo()])
}

function getOrderInfo() {
    return fetch(REQUEST_URL + ORDER_INFO,
        {
            method: HTTP_METHOD_GET,
            headers: HTTP_AUTH_HEADERS(getCredentialCookie())
        })
        .then(response => {
            if(response.status != HTTP_STATUS_OK) {
                alert("Nope")
                return;
            }
            return response.json()
        })
        .then((data) => {
            if(data) {
                return data;
            }
            return [];
        })
}