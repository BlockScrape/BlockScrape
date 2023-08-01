import {useDisclosure} from '@mantine/hooks';
import {Button, Center, Checkbox, Group, Modal, NumberInput, TextInput} from '@mantine/core';
import {DateTimePicker} from '@mantine/dates'
import React from "react";
import {RiAddBoxFill} from "react-icons/ri";
import {useForm} from "@mantine/form";
import {register} from "../../../authentication/user";
import {saveOrder} from "../fetch/orderBackend";

export function OrderModal() {
    const [opened, {open, close}] = useDisclosure(false);
    const form = useForm({
        initialValues: {
            website_name: '',
            url: '',
            starting_date: new Date(),
            intervall_time: 30,
            repetitions: 1,
            termsOfService: false,
        }
    });

    const handleSubmit = (value: ReturnType<(values: { website_name: string; starting_date: Date; intervall_time: number; termsOfService: boolean; url: string; repetitions: number }) => { website_name: string; starting_date: Date; intervall_time: number; termsOfService: boolean; url: string; repetitions: number }>) => {

        if (value.termsOfService) {
            console.log(value)
            saveOrder(value)
        }
    };

    return (
        <>
            <Modal opened={opened} onClose={close} title="Add Order">
                <form onSubmit={form.onSubmit((values) => handleSubmit(values))}>
                    <DateTimePicker
                        withSeconds
                        label="Pick date and time"
                        placeholder="Pick date and time"
                        maw={400}
                        mx="auto"
                        {...form.getInputProps('starting_date')}
                        required
                    />
                    <br/>
                    <TextInput
                        label="Name"
                        placeholder="WebsiteName"
                        {...form.getInputProps('website_name')}
                        required/>
                    <br/>
                    <TextInput
                        label="Url"
                        placeholder="www.temp.de"
                        {...form.getInputProps('url')}
                        required/>
                    <br/>
                    <NumberInput
                        label="Intervall-Time"
                        description="In seconds from 30 to 86400"
                        max={86400}
                        min={30}
                        defaultValue={600}
                        {...form.getInputProps('intervall_time')}
                        required
                    />
                    <br/>
                    <NumberInput
                        label="Repetitions"
                        description="How often should the website be scraped? From 1 to 100"
                        max={100}
                        min={1}
                        defaultValue={10}
                        {...form.getInputProps('repetitions')}
                        required
                    />
                    <br/>
                    <Checkbox
                        label="I agree to sell my soul"
                        {...form.getInputProps('termsOfService')}
                        required
                    />
                    <br/>
                    <Center>
                        <Button type="submit" color="teal">
                            Save Order
                        </Button>
                    </Center>
                </form>
            </Modal>

            <Group position="center">
                <Button onClick={open} variant="outline" color="green" size={"xs"}>
                    {<RiAddBoxFill color="green" size="1.2rem"/>}
                </Button>
            </Group>
        </>
    );
}