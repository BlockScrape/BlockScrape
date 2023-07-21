import {useState} from 'react';
import {
    AppShell,
    Navbar,
    Header,
    Footer,
    Aside,
    Text,
    MediaQuery,
    Burger,
    useMantineTheme,
} from '@mantine/core';
import {MainLinks} from '../global/_mainLinks';
import {AuthenticationForm} from "../authentication/authentication";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import {getCredentialCookie, setCredentialCookie} from "../authentication/user";

export default function MainPage() {
    const theme = useMantineTheme();
    const [opened, setOpened] = useState(false);
    if (getCredentialCookie() === undefined) {
        return <AuthenticationForm/>
    }

    return (
        <AppShell

            styles={{
                main: {
                    background: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0],
                },
            }}
            navbarOffsetBreakpoint="sm"
            asideOffsetBreakpoint="sm"

            navbar={
                <Navbar p="md" hiddenBreakpoint="sm" hidden={!opened} width={{sm: 200, lg: 300}}>
                    <Text>Navigation</Text>
                    <Navbar.Section grow mt="md">
                        <MainLinks/>
                    </Navbar.Section>
                </Navbar>
            }
            footer={
                <Footer height={60} p="md">
                    Typischer Baba Footer
                </Footer>
            }
            header={
                <Header height={{base: 50, md: 70}} p="md">
                    <div style={{display: 'flex', alignItems: 'center', height: '100%'}}>
                        <MediaQuery largerThan="sm" styles={{display: 'none'}}>
                            <Burger
                                opened={opened}
                                onClick={() => setOpened((o) => !o)}
                                size="sm"
                                color={theme.colors.gray[6]}
                                mr="xl"
                            />
                        </MediaQuery>

                        <Text>Baba Header</Text>
                    </div>
                </Header>
            }

        >
            <Text>Resize app to see responsive navbar in action</Text>
        </AppShell>
    );
}