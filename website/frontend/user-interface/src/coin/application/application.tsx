import {Flex} from '@mantine/core';
import React, {useEffect, useState} from "react";
import {getCoinStatus} from "./fetch/coinBackend";
import {Notifications} from "@mantine/notifications";

export function CoinApplication() {
    const [contentData, setData] = useState("Unknown");
    useEffect(() => {
        getCoinStatus()
            .then((data) => {
                if (data) {
                    setData(data.coin.toString());
                }
            })
    }, []);


    return (
        <>
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <h2>Your Coin Status</h2>
            </Flex>
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <h3>{contentData} Credit</h3>
            </Flex>
            <Notifications/>
        </>
    );
}