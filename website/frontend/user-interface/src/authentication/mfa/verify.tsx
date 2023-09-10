import {useForm} from "@mantine/form";
import {verify_mfa} from "../user";
import {Button, Center, Container, Group, Text, TextInput} from "@mantine/core";
import QRCode from "react-qr-code";
import React, {useState} from "react";
import {notifications} from "@mantine/notifications";
import {IconCheck} from "@tabler/icons-react";

export default function VerifyMFA(value: {
    username: string,
    google_otp_auth: string,
    otp_secret: string,
    close: any
}) {
    console.log(value.username)
    const mfa_checker_form = useForm({
        initialValues: {
            username: value.username,
            mfa_key: ''
        },
    });

    const handleMfaChecker = (internal_value: ReturnType<(values: { username: string; mfa_key: string }) => {
        username: string;
        mfa_key: string
    }>) => {
        verify_mfa(internal_value.username, internal_value.mfa_key)
            .then(
                value.close
            ).then(() => {
                notifications.show({
                    id: "register-okay",
                    withCloseButton: true,
                    title: "Okay",
                    message: "MFA Validated",
                    icon: <IconCheck/>,
                    color: "green"
                });
            }
        )
    }

    const [showCredentials, setCredentials] = useState(true)

    return (
        <>
            <Center>
                <Text>
                    Click the Show Button to see your MFA Credentials
                </Text>
            </Center>
            <br/>
            <Container hidden={showCredentials}>
                <div style={{background: 'white', padding: '16px'}}>
                    <QRCode
                        size={256}
                        style={{height: "auto", maxWidth: "100%", width: "100%"}}
                        value={value.google_otp_auth}
                        viewBox={`0 0 256 256`}
                    />
                </div>
                <Center>
                    <Text>
                        Secret Key:
                    </Text>
                </Center>
                <Center>
                    <Text>{value.otp_secret}</Text>
                </Center>
                <br/>
            </Container>
            <Center>
                <Button onClick={() => {
                    setCredentials(!showCredentials)
                }}>
                    Show Credentials
                </Button>
            </Center>
            <br/>
            <Center>
                <Text>
                    For Validation insert your MFA Key
                </Text>
            </Center>
            <form onSubmit={mfa_checker_form.onSubmit((mfa_values) => handleMfaChecker(mfa_values))}>
                <TextInput
                    withAsterisk
                    label="MFA Key"
                    {...mfa_checker_form.getInputProps('mfa_key')}
                    required
                />
                <Group position="right" mt="md">
                    <Button type="submit">Submit</Button>
                </Group>
            </form>
        </>
    )
}