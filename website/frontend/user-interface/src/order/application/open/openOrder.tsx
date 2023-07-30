import {Modal, Button, Group, TextInput, NumberInput, Checkbox, Center, ThemeIcon, Flex} from '@mantine/core';
import {useDisclosure} from '@mantine/hooks';
import {RiDeleteBin2Fill, RiEdit2Fill} from "react-icons/ri";
import React from "react";

function deleteOrder() {
    console.log("YOOO")
}


export function OpenOrder(value: { uuid: string, name: string, url: string, starting_date: Date, intervall: number, repetitions: number }) {
    const [opened, {open, close}] = useDisclosure(false);
    return (
        <>
            <Modal opened={opened} onClose={close} title={value.name}>
                <p style={{wordWrap: "break-word"}}>{value.url}</p>
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
                    <Button onClick={() => deleteOrder()} variant="outline" color="red">
                        {<RiDeleteBin2Fill size="1.2rem"/>}
                    </Button>
                </Flex>
            </Modal>
            <tr onClick={open}>
                <td>{value.name}</td>
                <td>{value.starting_date.toString()}</td>
                <td>{value.intervall}</td>
                <td>{value.repetitions}</td>
            </tr>
        </>
    );
}