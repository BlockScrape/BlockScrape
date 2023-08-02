import React, {useEffect, useState} from 'react';
import {getUser} from "./fetch/userBackend";
import {Notifications} from '@mantine/notifications';
import {Flex} from "@mantine/core";

export function WelcomeApplication() {
    const [contentData, setData] = useState("Unknown");
    useEffect(() => {
        getUser()
            .then((data) => {
                if (data) {
                    let name = data.first_name + " " + data.last_name;
                    console.log(name)
                    setData(name)
                } else {
                }
            })
    }, []);

    return (<>
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <h1>Welcome</h1>
            </Flex>
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <h2>{contentData}</h2>
            </Flex>
            <Notifications/>
        </>
    );
}