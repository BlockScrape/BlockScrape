import {useDisclosure} from '@mantine/hooks';
import {Modal, Button, Group, TextInput, NumberInput, Checkbox, Center, ThemeIcon} from '@mantine/core';
import {DateTimePicker} from '@mantine/dates'
import React from "react";
import {
    RiAddBoxFill
} from "react-icons/ri";
export function OrderModal() {
    const [opened, {open, close}] = useDisclosure(false);
    return (
        <>
            <Modal opened={opened} onClose={close} title="Add Order">
                <DateTimePicker
                    withSeconds
                    label="Pick date and time"
                    placeholder="Pick date and time"
                    maw={400}
                    mx="auto"
                />
                <br/>
                <TextInput label="Name" placeholder="WebsiteName" required/>
                <br/>
                <TextInput label="Url" placeholder="www.temp.de" required/>
                <br/>
                <NumberInput
                    label="Intervall-Time"
                    description="In seconds from 30 to 86400"
                    max={86400}
                    min={30}
                    defaultValue={600}
                    required
                />
                <br/>
                <NumberInput
                    label="Repetitions"
                    description="How often should the website be scraped? From 1 to 100"
                    max={100}
                    min={1}
                    defaultValue={10}
                    required
                />
                <br/>
                <Checkbox
                    label="I agree to sell my soul" required
                />
                <br/>
                <Center>
                    <Button color="teal">
                        Save Order
                    </Button>
                </Center>

            </Modal>

            <Group position="center">
                <Button onClick={open} variant="outline" color="green" size={"xs"}>
                    {<RiAddBoxFill color="green" size="1.2rem"/>}
                </Button>
            </Group>
        </>
    );
}