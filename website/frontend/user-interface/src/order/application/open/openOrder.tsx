import {Modal, Button, Flex} from '@mantine/core';
import {useDisclosure} from '@mantine/hooks';
import {RiDeleteBin2Fill} from "react-icons/ri";
import React from "react";
import {deleteOrder} from "../fetch/orderBackend";

function deleteThisOrder(uuid: string) {
    deleteOrder(uuid)
}


export function OpenOrder(value: { uuid: string, name: string, url: string, starting_date: Date, intervall: number, repetitions: number
                                    request_method: string, request_body: string, request_header: string}) {
    const [opened, {open, close}] = useDisclosure(false);
    return (
        <>
            <Modal opened={opened} onClose={close} title={value.name}>
                <p style={{wordWrap: "break-word"}}>{value.uuid}</p>
                <p style={{wordWrap: "break-word"}}>{value.url}</p>
                <Flex gap="xs">
                    <p>Method: </p>
                    <p>{value.request_method}</p>
                </Flex>
                <Flex gap="xs">
                    <p>Header: </p>
                    <p>{value.request_header}</p>
                </Flex>
                <Flex gap="xs">
                    <p>Body: </p>
                    <p>{value.request_body}</p>
                </Flex>
                <p>{value.starting_date.toString()}</p>
                <Flex gap="xs">
                    <p>Repetitions: </p>
                    <p>{value.repetitions}</p>
                </Flex>
                <Flex gap="xs">
                    <p>Intervall: </p>
                    <p>{value.intervall}</p>
                </Flex>
                <Flex
                    mih={50}
                    gap="md"
                    justify="center"
                    align="flex-start"
                    direction="row"
                    wrap="wrap"
                >
                    <Button onClick={() => deleteThisOrder(value.uuid)} variant="outline" color="red">
                        {<RiDeleteBin2Fill size="1.2rem"/>}
                    </Button>
                </Flex>
            </Modal>
            <tr onClick={open} key={value.uuid}>
                <td>{value.name}</td>
                <td>{value.starting_date.toString()}</td>
                <td>{value.intervall}</td>
                <td>{value.repetitions}</td>
            </tr>
        </>
    );
}