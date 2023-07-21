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

export function RegisterForm() {
    return (
        <Container size={420} my={40}>
            <Title
                align="center"
                sx={(theme) => ({fontFamily: `Greycliff CF, ${theme.fontFamily}`, fontWeight: 900})}
            >
                Wohooooo NEW USER!!!
            </Title>

            <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                <TextInput label="First Name" placeholder="John/Jane" required/>
                <TextInput label="Last Name" placeholder="Doe" required/>
                <TextInput label="Username" placeholder="username" required/>
                <TextInput label="Email" placeholder="john@doe.de" required/>
                <PasswordInput label="Password" placeholder="Your password" required mt="md"/>

                <Group position="apart" mt="lg">
                </Group>
                <Button fullWidth mt="xl">
                    Register
                </Button>
            </Paper>
        </Container>
    );
}