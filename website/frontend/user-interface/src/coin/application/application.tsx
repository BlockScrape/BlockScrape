import {Button, Flex, Group, NumberInput} from '@mantine/core';
import React, {useEffect, useState} from "react";
import {getCoinStatus, updateCoinStatus} from "./fetch/coinBackend";
import {Notifications} from "@mantine/notifications";
import {useForm} from "@mantine/form";

export function CoinApplication() {
    const [contentData, setData] = useState("Unknown");
    useEffect(() => {
        getCoinStatus()
            .then((data) => {
                if (data) {
                    setData(data.toString());
                }
            })
    }, []);
    const form = useForm({
        initialValues: {
            addition: 0
        },
    });

    const handleSubmit = (value: ReturnType<(values: { addition: number }) => { addition: number }>) => {
        updateCoinStatus(value.addition)
    };

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


            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <form onSubmit={form.onSubmit((values) => handleSubmit(values))}>
                    <NumberInput
                        withAsterisk
                        label="Update Coin"
                        {...form.getInputProps('addition')}
                        required
                    />
                    <Group position="right" mt="md">
                        <Button type="submit">Submit</Button>
                    </Group>
                </form>
            </Flex>
            <Notifications/>
        </>
    );
}