import {useForm} from "@mantine/form";
import {login_mfa} from "../user";
import {Button, Center, Group, Text, TextInput} from "@mantine/core";
import React from "react";


export default function DoMfa(value: {
    username: string,
    password: string
}) {
    console.log(value.username)
    const mfa_form = useForm({
        initialValues: {
            username: value.username,
            password: value.password,
            mfa_key: ''
        },
    });

    const handleMfaSubmit = (internal_value: ReturnType<(values: {
        password: string;
        username: string;
        mfa_key: string
    }) => {
        password: string;
        username: string;
        mfa_key: string
    }>) => {
        login_mfa(internal_value.username, internal_value.password, internal_value.mfa_key)
    }

    return (<>
        <Center>
            <Text>
                Insert your MFA Key
            </Text>
        </Center>
        <form onSubmit={mfa_form.onSubmit((mfa_values) => handleMfaSubmit(mfa_values))}>
            <TextInput
                withAsterisk
                label="MFA Key"
                {...mfa_form.getInputProps('mfa_key')}
                required
            />
            <Group position="right" mt="md">
                <Button type="submit">Submit</Button>
            </Group>
        </form>
    </>)
}