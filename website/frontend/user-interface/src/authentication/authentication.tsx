import {
    TextInput,
    PasswordInput,
    Anchor,
    Paper,
    Title,
    Text,
    Container,
    Group,
    Button,
    ActionIcon,
    useMantineColorScheme
} from '@mantine/core';
import {Link} from 'react-router-dom';
import {login} from "./user";
import {useForm} from '@mantine/form';
import React from 'react';
import {Notifications} from "@mantine/notifications";
import {IconSun, IconMoonStars} from '@tabler/icons-react';

export function AuthenticationForm() {
    const { colorScheme, toggleColorScheme } = useMantineColorScheme();
    const dark = colorScheme === 'dark';
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
        <>
            <ActionIcon
                variant="outline"
                color={dark ? 'yellow' : 'blue'}
                onClick={() => toggleColorScheme()}
                title="Toggle color scheme"
            >
                {dark ? <IconSun size="1.1rem"/> : <IconMoonStars size="1.1rem"/>}
            </ActionIcon>
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
                        <PasswordInput label="Password" placeholder="Your password" {...form.getInputProps('password')}
                                       required mt="md"/>
                        <Group position="right" mt="md">
                            <Button type="submit">Submit</Button>
                        </Group>
                    </form>
                </Paper>

            </Container>
            <Notifications/>
        </>
    )
        ;
}