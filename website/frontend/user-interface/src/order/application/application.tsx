import {Table} from '@mantine/core';
import {OpenOrder} from "./open/openOrder";

export default function OrderApplication() {
    const elements = [
        {uuid: "asdasdfasdf", name: "web1", url: "www.jegger.com", starting_date: new Date(1690710324000), intervall: 20, repetitions: 5},
        {
            uuid: "asdasdfasdfe",
            name: "web2",
            url: "https://api.open-meteo.com/v1/forecast?latitude=48.6831104&longitude=10.1226181&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&current_weather=true&timezone=Europe%2FBerlin",
            starting_date: new Date(1690710324000),
            intervall: 2000,
            repetitions: 5000
        },
        {uuid: "asdasdfasdfa", name: "web3", url: "www.jegger.com", starting_date: new Date(1690710324000), intervall: 20, repetitions: 5},
        {uuid: "asdasdfasdfg", name: "web4", url: "www.jegger.com", starting_date: new Date(1690710324000), intervall: 20, repetitions: 5},
        {uuid: "asdasdfasdfj", name: "web5", url: "www.jegger.com", starting_date: new Date(1690710324000), intervall: 20, repetitions: 5}
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
    return (
        <Table highlightOnHover withBorder>
            <thead>
            <tr>
                <th>Name</th>
                <th>Starting Date</th>
                <th>Intervall</th>
                <th>Repetitions</th>
            </tr>
            </thead>
            <tbody>{rows}</tbody>
        </Table>
    )
        ;
}