import { test, expect } from '@playwright/test';  

test('홈페이지 타이틀 확인', async({page}) =>{
    await page.goto('/');
    await expect(page).toHaveTitle(/마켓컬리/);
} )