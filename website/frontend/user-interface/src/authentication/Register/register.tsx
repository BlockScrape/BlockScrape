import {
    TextInput,
    PasswordInput,
    Anchor,
    Paper,
    Title,
    Text,
    Container,
    Group,
    Button, Checkbox,
} from '@mantine/core';
import {DatePickerInput} from '@mantine/dates';
import {useForm} from "@mantine/form";
import {useState} from 'react';
import {doUtcDate} from "../../global/constants/constants";
import {register} from "../user";



export function RegisterForm() {
    const form = useForm({
        initialValues: {
            first_name: '',
            last_name: '',
            birthdate: new Date(),
            username: '',
            email: '',
            password: '',
            termsOfService: false,
        },

        validate: {
            email: (data) => (/^\S+@\S+$/.test(data) ? null : 'Invalid email'),
        },
    });

    const handleSubmit = (value: ReturnType<(values: { first_name: string, last_name: string, birthdate: Date, username: string, email: string, password: string, termsOfService: boolean }) =>
        { first_name: string, last_name: string, birthdate: Date, username: string, email: string, password: string, termsOfService: boolean }>) => {

        if (value.termsOfService) {
            register(value)
        }
    };

    return (
        <Container size={420} my={40}>
            <Title
                align="center"
                sx={(theme) => ({fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 900})}
            >
                Wohooooo NEW USER!!!
            </Title>

            <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                <form onSubmit={form.onSubmit((values) => handleSubmit(values))}>
                    <TextInput
                        label="First Name"
                        placeholder="John/Jane"
                        {...form.getInputProps('first_name')}
                        required/>
                    <TextInput
                        label="Last Name"
                        placeholder="Doe"
                        {...form.getInputProps('last_name')}
                        required/>
                    <DatePickerInput
                        label="Your Birthday"
                        placeholder="Pick your birthday"
                        {...form.getInputProps('birthdate')}
                        mx="auto"
                        maw={400}/>
                    <TextInput
                        label="Username"
                        placeholder="username"
                        {...form.getInputProps('username')}
                        required/>
                    <TextInput
                        withAsterisk
                        label="Email"
                        placeholder="your@email.com"
                        {...form.getInputProps('email')}
                        required/>
                    <PasswordInput
                        label="Password"
                        placeholder="Your password"
                        {...form.getInputProps('password')}
                        required/>
                    <Checkbox
                        mt="md"
                        label="I agree to sell my soul"
                        {...form.getInputProps('termsOfService', {type: 'checkbox'})}
                        required/>
                    <Group position="right" mt="md">
                        <Button type="submit">Submit</Button>
                    </Group>
                </form>
            </Paper>
        </Container>
    );
}