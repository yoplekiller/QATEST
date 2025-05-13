import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
    timeout: 30000,
    retries: 0,
    use: {
        headless: true,
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
        baseURL: 'BASE_URL'
    },
    reporter: [['list'],
     ['allure-playwright'], 
     ['html', { outputFolder: 'playwright-report', open: 'never' }]
    ],
});