import {useDisclosure} from '@mantine/hooks';
import {Button, Center, Checkbox, Group, Modal, NumberInput, Select, TextInput} from '@mantine/core';
import {DateTimePicker} from '@mantine/dates'
import React from "react";
import {RiAddBoxFill} from "react-icons/ri";
import {useForm} from "@mantine/form";
import {saveOrder} from "../fetch/orderBackend";

export function OrderModal() {
    const [opened, {open, close}] = useDisclosure(false);
    const form = useForm({
        initialValues: {
            website_name: '',
            url: '',
            request_method: 'GET',
            request_body: '',
            request_header: '',
            starting_date: new Date(),
            intervall_time: 30,
            repetitions: 1,
            termsOfService: false,
        }
    });

    const handleSubmit = (value: ReturnType<(values: {website_name: string, url: string, request_method: string, request_body: string, request_header: string, starting_date: Date, intervall_time: number, repetitions: number, termsOfService: boolean}) => {website_name: string, url: string, request_method: string, request_body: string, request_header: string, starting_date: Date, intervall_time: number, repetitions: number, termsOfService: boolean}>) => {

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
                        placeholder="Date and Time is in UTC"
                        mx="auto"
                        {...form.getInputProps('starting_date')}
                        required
                    />
                    <TextInput
                        label="Name"
                        placeholder="WebsiteName"
                        {...form.getInputProps('website_name')}
                        required/>
                    <TextInput
                        label="Url"
                        placeholder="www.temp.de"
                        {...form.getInputProps('url')}
                        required/>
                    <Select
                        label="Request Method"
                        placeholder="Pick your request method"
                        data={[
                            {value: 'GET', label: 'GET'},
                            {value: 'POST', label: 'POST'},
                            {value: 'PUT', label: 'PUT'},
                            {value: 'DELETE', label: 'DELETE'},
                            {value: 'PATCH', label: 'PATCH'},
                            {value: 'OPTIONS', label: 'OPTIONS'},
                            {value: 'HEAD', label: 'HEAD'}
                        ]}
                        {...form.getInputProps('request_method')}
                        required
                    />
                    <TextInput
                        label="Request Header"
                        placeholder="Put your header"
                        {...form.getInputProps('request_header')}/>
                    <TextInput
                        label="Request Body"
                        placeholder="Put your body"
                        {...form.getInputProps('request_body')}
                        />
                    <NumberInput
                        label="Intervall-Time"
                        description="In seconds from 30 to 86400"
                        max={86400}
                        min={30}
                        defaultValue={600}
                        {...form.getInputProps('intervall_time')}
                        required
                    />
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
                    <Center>
                        <p>Be sure you have enough coins. Every repetition need one coin</p>
                    </Center>
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