import {BrowserRouter, Routes, Route} from "react-router-dom";

import {AuthenticationForm} from "./authentication/authentication";
import {RegisterForm} from "./authentication/Register/register";
import React from "react";
import MainPage from "./main/main";
import OrderPage from "./order/order";
import CoinPage from "./coin/coin";
import Impressum from "./footer/impressum";
import NotFound from "./global/404/404";
import {ColorScheme, ColorSchemeProvider, MantineProvider} from "@mantine/core";
import {useLocalStorage} from "@mantine/hooks";


export default function App() {
    const [colorScheme, setColorScheme] = useLocalStorage<ColorScheme>({
    key: 'mantine-color-scheme',
    defaultValue: 'light',
    getInitialValueInEffect: true,
  });

  const toggleColorScheme = (value?: ColorScheme) =>
    setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'));
    return (
        <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
            <MantineProvider theme={{colorScheme}} withGlobalStyles withNormalizeCSS>
                <BrowserRouter>
                    <Routes>
                        <Route index element={<MainPage/>}/>
                        <Route path="/authenticationForm" element={<AuthenticationForm/>}/>
                        <Route path="/registerForm" element={<RegisterForm/>}/>
                        <Route path="/orderPage" element={<OrderPage/>}/>
                        <Route path="/coinPage" element={<CoinPage/>}/>
                        <Route path="/impressum" element={<Impressum/>}/>
                        <Route path="*" element={<NotFound/>}/>
                    </Routes>
                </BrowserRouter>
            </MantineProvider>
        </ColorSchemeProvider>
    )
        ;
}
