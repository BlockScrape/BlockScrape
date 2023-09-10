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
    useMantineColorScheme, Modal
} from '@mantine/core';
import {Link} from 'react-router-dom';
import {login} from "./user";
import {useForm} from '@mantine/form';
import React, {useState} from 'react';
import {Notifications} from "@mantine/notifications";
import {IconSun, IconMoonStars} from '@tabler/icons-react';
import {useDisclosure} from "@mantine/hooks";
import VerifyMFA from "./mfa/verify";
import DoMfa from "./mfa/doMfa";


export function AuthenticationForm() {
    const {colorScheme, toggleColorScheme} = useMantineColorScheme();
    const [mfaData, setMfaData] = useState((<Text>Loading...</Text>));
    const [opened, {open, close}] = useDisclosure(false);
    const dark = colorScheme === 'dark';
    const form = useForm({
        initialValues: {
            username: '',
            password: ''
        },
    });

    const handleSubmit = (value: ReturnType<(values: { password: string; username: string }) => {
        password: string;
        username: string
    }>) => {
        setMfaData((<Text>Loading...</Text>))
        login(value.username, value.password)
            .then((data) => {
                if (data) {
                    if (data.otp_verified === true) {
                        setMfaData(<DoMfa username={value.username} password={value.password}/>)
                    } else {
                        setMfaData(<VerifyMFA username={value.username} google_otp_auth={data.otp_google_auth}
                                              otp_secret={data.otp_key} close={close}/>)
                    }
                }
            })
            .then(
                open
            )

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
                <Modal opened={opened} onClose={close} title="MFA Login">
                    {mfaData}
                </Modal>
            </Container>
            <Notifications/>
        </>
    )
        ;
}