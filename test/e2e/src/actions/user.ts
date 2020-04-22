import {Page} from 'puppeteer'

export class UserAction{

    public async login(page:Page, username:string, password:string){
        await page.waitFor(3000);

        const usernameInput = await page.waitForSelector('input[type = "text"]');
        await usernameInput.type(username);

        const passwordInput = await page.waitForSelector('input[type = "password"]');
        await passwordInput.type(password);
        
        await page.waitFor(5000);

        const loginBtn = await page.waitForSelector('button[type = "button"]');
        await loginBtn.click();
        
        await page.waitFor(4000);

    }


}
