import React from 'react';
import {
    BsCashCoin
} from 'react-icons/bs';
import {Link} from "react-router-dom";
import {AiOutlineShoppingCart} from "react-icons/ai";
import {ThemeIcon, UnstyledButton, Group, Text} from '@mantine/core';

interface MainLinkProps {
    icon: React.ReactNode;
    color: string;
    label: string;

    link: string
}

function MainLink({icon, color, label, link}: MainLinkProps) {
    return (
        <UnstyledButton
            sx={(theme) => ({
                display: 'block',
                width: '100%',
                padding: theme.spacing.xs,
                borderRadius: theme.radius.sm,
                color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.black,

                '&:hover': {
                    backgroundColor:
                        theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
                },
            })}
            component={Link}
            to={link}
        >
            <Group>
                <ThemeIcon color={color} variant="light">
                    {icon}
                </ThemeIcon>

                <Text size="sm">{label}</Text>
            </Group>
        </UnstyledButton>
    );
}

const data = [
    {icon: <AiOutlineShoppingCart size="1.2rem"/>, color: 'green', label: 'Your Orders', link: '/orderPage'},
    {icon: <BsCashCoin size="1.2rem"/>, color: 'yellow', label: 'Jegger Coins', link: '/coinPage'},

];

export function MainLinks() {
    const links = data.map((link) => <MainLink {...link} key={link.label}/>);
    return <div>{links}</div>;
}