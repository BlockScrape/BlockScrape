import React, {useState} from 'react';
import {
    ActionIcon,
    Anchor,
    AppShell,
    Burger,
    Flex,
    Footer,
    Group,
    Header,
    MediaQuery,
    Navbar,
    Text,
    useMantineColorScheme,
    useMantineTheme,
} from '@mantine/core';
import {MainLinks} from '../global/_mainLinks';
import {AuthenticationForm} from "../authentication/authentication";
import {Link} from "react-router-dom";
import {getCredentialCookie, logout} from "../global/constants/constants";
import {OrderModal} from "./application/add/addOrder";
import OrderApplication from "./application/application";
import {AiOutlineShoppingCart} from "react-icons/ai";
import {Notifications} from "@mantine/notifications";
import {IconMoonStars, IconSun} from "@tabler/icons-react";

export default function OrderPage() {
    const theme = useMantineTheme();
    const [opened, setOpened] = useState(false);
    const {colorScheme, toggleColorScheme} = useMantineColorScheme();
    const dark = colorScheme === 'dark';
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

                        <Flex
                            gap="md"
                            justify="right"
                            align="flex-start"
                            direction="row"
                            wrap="wrap"
                        >
                            <div>
                                <Anchor component={Link} to="/" unstyled={true}>
                                    BlockScrape
                                </Anchor>
                            </div>


                        </Flex>
                        <div style={{marginLeft: "auto"}}>
                            <Flex
                                gap="md"
                                justify="right"
                                align="flex-start"
                                direction="row"
                                wrap="wrap"
                            >
                                <Anchor onClick={() => logout()}>
                                    Logout
                                </Anchor>

                                <ActionIcon
                                    variant="outline"
                                    color={dark ? 'yellow' : 'blue'}
                                    onClick={() => toggleColorScheme()}
                                    title="Toggle color scheme"
                                >
                                    {dark ? <IconSun size="1.1rem"/> : <IconMoonStars size="1.1rem"/>}
                                </ActionIcon>
                            </Flex>
                        </div>
                    </div>
                </Header>
            }

        >
            <Flex
                mih={50}
                gap="md"
                justify="center"
                align="flex-start"
                direction="row"
                wrap="wrap"
            >
                <Group>
                    <h1 color="teal">Your Orders</h1>
                    {<AiOutlineShoppingCart size="2rem"/>}
                </Group>


            </Flex>
            <br/>
            <br/>
            <OrderApplication/>
            <br/>
            <br/>
            <OrderModal/>
            <Notifications/>
        </AppShell>
    );
}

