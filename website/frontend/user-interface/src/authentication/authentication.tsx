import {
    TextInput,
    PasswordInput,
    Anchor,
    Paper,
    Title,
    Text,
    Container,
    Group,
    Button
} from '@mantine/core';
import {Link} from 'react-router-dom';
import {login} from "./user";
import {useForm} from '@mantine/form';
import React, {useState} from 'react';

export function AuthenticationForm() {
    const [message, setMessage] = useState('');
    const form = useForm({
        initialValues: {
            username: '',
            password: ''
        },
    });

    const handleSubmit = (value: ReturnType<(values: { password: string; username: string }) => { password: string; username: string }>) => {
        login(value.username, value.password)

    };

    return (
        <Container size={420} my={40}>
            <Title
                align="center"
                sx={(theme) => ({fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 900})}
            >
                Welcome back!
            </Title>
            <Text color="dimmed" size="sm" align="center" mt={5}>
                Do not have an account yet?{' '}
                <Anchor component={Link} to="/RegisterForm">
                    Create Account
                </Anchor>
            </Text>

            <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                <form onSubmit={form.onSubmit((values) => handleSubmit(values))}>
                    <TextInput
                        withAsterisk
                        label="Username"
                        placeholder="username"
                        {...form.getInputProps('username')}
                        required
                    />
                    <PasswordInput label="Password" placeholder="Your password" {...form.getInputProps('password')} required mt="md"/>
                    <Group position="right" mt="md">
                        <Button type="submit">Submit</Button>
                    </Group>
                </form>
            </Paper>
        </Container>
    )
        ;
}