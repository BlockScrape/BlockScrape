import Cookies from "universal-cookie";

export function setCredentialCookie(value: string, expires: number) {
    const cookies = new Cookies()
    let date = new Date();
    date.setTime(date.getTime() + (expires*60*60*1000))
    cookies.set("token", value, {expires: date, path: '/'})
}

export function getCredentialCookie() {
    const cookies = new Cookies()
    return cookies.get("token");
}