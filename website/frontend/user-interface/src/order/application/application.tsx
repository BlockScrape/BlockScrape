import {Table} from '@mantine/core';
import {OpenOrder} from "./open/openOrder";
import {getOrders} from "./fetch/orderBackend";
import {getCredentialCookie, HTTP_AUTH_HEADERS} from "../../global/constants/constants";
import {useEffect, useState} from "react";

export default function OrderApplication() {
    let elements = [
        {uuid: "", name: "", url: "", starting_date: new Date(), intervall: 0, repetitions: 0},
    ]
    const rows = elements.map((element) => (
            <OpenOrder
                uuid={element.uuid}
                name={element.name}
                url={element.url}
                starting_date={element.starting_date}
                intervall={element.intervall}
                repetitions={element.repetitions}
            />
        )
    )
    const [contentData, setData] = useState(rows);
    useEffect(() => {
        getOrders().then((response) => {
            let temp = response[0].map((element: { uuid: string; name: string; scraping_url: string; start_timestamp: number; intervall: number; repetitions: number; }) => (
                    <OpenOrder
                        uuid={element.uuid}
                        name={element.name}
                        url={element.scraping_url}
                        starting_date={new Date(element.start_timestamp * 1000)}
                        intervall={element.intervall}
                        repetitions={element.repetitions}
                    />
                )
            )
            console.log(response)
            setData(temp)
        });
    },[]);
    return (
        <Table highlightOnHover withBorder>
            <thead>
            <tr key={"Description"}>
                <th>Name</th>
                <th>Starting Date</th>
                <th>Intervall</th>
                <th>Repetitions</th>
            </tr>
            </thead>
            <tbody>{contentData}</tbody>
        </Table>
    )
        ;
}