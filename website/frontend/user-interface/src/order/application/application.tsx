import {Table} from '@mantine/core';
import {OpenOrder} from "./open/openOrder";
import {getOrders} from "./fetch/orderBackend";
import {useEffect, useState} from "react";

export default function OrderApplication() {
    let elements = [
        {
            uuid: "", name: "", url: "", starting_date: new Date(), intervall: 0, repetitions: 0, request_body: "",
            request_header: "", request_method: ""
        },
    ]
    const rows = elements.map((element) => (
            <OpenOrder
                uuid={element.uuid}
                name={element.name}
                url={element.url}
                starting_date={element.starting_date}
                intervall={element.intervall}
                repetitions={element.repetitions}
                request_body={element.request_body}
                request_header={element.request_header}
                request_method={element.request_method}
            />
        )
    )
    const [contentData, setData] = useState(rows);
    useEffect(() => {
        getOrders().then((response) => {
            let temp = response[0].map((element: {
                request_method: string; request_header: string; request_body: string; uuid: string; name: string; scraping_url: string; start_timestamp: number; intervall: number; repetitions: number; }) => (
                    <OpenOrder
                        uuid={element.uuid}
                        name={element.name}
                        url={element.scraping_url}
                        starting_date={new Date(element.start_timestamp * 1000)}
                        intervall={element.intervall}
                        repetitions={element.repetitions}
                        request_body={element.request_body}
                        request_header={element.request_header}
                        request_method={element.request_method}
                    />
                )
            )
            console.log(response)
            setData(temp)
        });
    }, []);
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