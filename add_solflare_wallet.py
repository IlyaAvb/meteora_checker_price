import asyncio
from playwright.async_api import async_playwright, expect, BrowserContext, Page

from METEORA.settings import meteora_website
from privat import seedka, pass_for_wallet

async def add_solflare_wallet(context: BrowserContext, page: Page):

    await page.bring_to_front()

    #У меня уже есть кошелек
    i_have_wal_btn = page.locator('//button[@data-id="i_already_have_wallet_button"]')
    await expect(i_have_wal_btn).to_be_visible()
    await i_have_wal_btn.click()

#     Ввод сидки
    counter = 0
    for seed_word in seedka:
        input_seed = page.locator(f'//input[@id="mnemonic-input-{counter}"]')
        await input_seed.fill(seed_word)
        counter += 1


#     Кликаю продолжить
    continue_btn = page.get_by_role('button').last
    await expect(continue_btn).to_be_enabled()
    await continue_btn.click()

# Ввод пароля
    input_pass1 = page.locator('//*[@id=":r1:"]')
    input_pass2 = page.locator('//*[@id=":r2:"]')
    await expect(input_pass1).to_be_attached()
    await input_pass1.type(pass_for_wallet)
    await input_pass2.type(pass_for_wallet)

#     Далее
    wal_continue_btn = page.locator('//*[@id="root"]/div/div[2]/div/div[2]/form/div[2]/button[2]')
    await expect(wal_continue_btn).to_be_enabled()
    await wal_continue_btn.click()


    await page.wait_for_timeout(6000)

    next_button = page.locator('//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div/button[1]')
    await expect(next_button).to_be_visible()
    await next_button.click()

    continue_btn = page.locator('//*[@id="root"]/div/div[1]/div[2]/div[2]/button')
    await expect(continue_btn).to_be_visible()
    await continue_btn.click()

    goto_wallet = page.locator('//*[@id="root"]/div/div[2]/div/div[2]/button[2]')
    await expect(goto_wallet).to_be_visible()
    await goto_wallet.click()

    # await page.wait_for_timeout(1000)
    #
    #
    # # Проверяю баланс на кошельке
    # balance_wallet = page.locator('//*[@id="root"]/div[2]/div/div[1]/div/div[1]/div[1]/div/h2/button')
    # await expect(balance_wallet).to_be_visible()
    # balance = await balance_wallet.inner_text()
    # print(f'Балик на кошельке: {balance}')





