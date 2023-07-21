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
} from '@mantine/core';
import {Link} from 'react-router-dom';
import {RegisterForm} from "./Register/register";
import {setCredentialCookie} from "./user";

export function AuthenticationForm() {
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
                <TextInput label="Email" placeholder="john@doe.de" required/>
                <PasswordInput label="Password" placeholder="Your password" required mt="md"/>
                <Group position="apart" mt="lg">
                </Group>
                <Button fullWidth mt="xl" onClick={() => setCredentialCookie("hi", 23)}>
                    Sign in
                </Button>
            </Paper>
        </Container>
    );
}