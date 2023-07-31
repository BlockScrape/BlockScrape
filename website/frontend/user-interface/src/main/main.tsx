import React, {useState} from 'react';
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
    Anchor,
    Center,
    Flex
} from '@mantine/core';
import {MainLinks} from '../global/_mainLinks';
import {AuthenticationForm} from "../authentication/authentication";
import {BrowserRouter, Routes, Route, Link} from "react-router-dom";
import {getCredentialCookie} from "../global/constants/constants";

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
                    <Flex
                        mih={50}
                        gap="md"
                        justify="center"
                        align="flex-start"
                        direction="row"
                        wrap="wrap"
                    >
                        <div>
                            <Anchor component={Link} to="/impressum">
                                Impressum
                            </Anchor>
                        </div>
                        <div>
                            <Anchor href="https://github.com/BlockScrape">
                                GitHub
                            </Anchor>
                        </div>
                        <div>
                            &copy;  2023 BlockScrape
                        </div>
                    </Flex>
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
    )
        ;
}