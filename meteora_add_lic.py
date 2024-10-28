import asyncio
from fake_useragent import FakeUserAgent
from playwright.async_api import async_playwright, expect
from settings import EXTENTION_PATH, meteora_website, jup_website, jlp_conract
from add_solflare_wallet import add_solflare_wallet
import api

from telegram_bot import send_message

user_agent = FakeUserAgent().random



async def main(message):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                f"--disable-extensions-except={EXTENTION_PATH}",
                f"--load-extension={EXTENTION_PATH}",
            ],
            user_agent=user_agent
        )

        background = context.service_workers[0]
        if not background:
            background = context.wait_for_event("serviceworker")

        # page = await context.new_page()
        # await page.goto(jup_website)

        page = await context.new_page()
        await page.goto(meteora_website)

        titles = [await p.title() for p in context.pages]

        print(f'Все заголовки {titles}')

        for index, title in enumerate(titles):
            if title == 'Solflare':
                solflare_page = context.pages[index]
            elif title == 'Home | Meteora':
                met_page = context.pages[index]
            elif title == 'Home | Jupiter' or 'Swap | Jupiter':
                jup_page = context.pages[index]

        await add_solflare_wallet(context, solflare_page)
        print('Кошелек импортирован')

        print('Перехожу на метеору')
        await send_message(message, 'Перехожу на метеору')

        await met_page.bring_to_front()
        await met_page.wait_for_load_state(state='domcontentloaded')

        # Нажимаю Connect а метеоре
        connect_wal_in_meteaora_btn = met_page.get_by_role('button').filter(has_text='Connect').first
        await expect(connect_wal_in_meteaora_btn).to_be_attached()
        await connect_wal_in_meteaora_btn.click()


        solflare_schoose = met_page.get_by_role('button').filter(has_text='Solflare')
        await expect(solflare_schoose).to_be_attached()

        wait_page = context.wait_for_event('page')

        await solflare_schoose.click()

        # Подключаю кошель на метеору в новом окне

        new_window = await wait_page
        await new_window.bring_to_front()
        await new_window.wait_for_load_state(state='networkidle', timeout=20000)

        solflare_turn_on = new_window.locator('//html/body/div[2]/div[2]/div/div[3]/div/button[2]')
        await expect(solflare_turn_on).to_be_enabled()
        await solflare_turn_on.click()

        print('Подключил кошелек к метеоре')


        await met_page.bring_to_front()
        await met_page.wait_for_load_state(state='domcontentloaded')

        input_search_token = met_page.locator('//input[@class="flex-1 w-full placeholder:text-sm"]')
        await expect(input_search_token).to_be_attached()
        await input_search_token.fill(jlp_conract)
        await met_page.wait_for_timeout(1500)

        await met_page.keyboard.press("Enter")
        await met_page.wait_for_load_state(state='domcontentloaded')

        await met_page.wait_for_timeout(1000)



        need_pair = met_page.locator('//*[@id="__next"]/div[1]/div[5]/div/div[2]/div[2]/div/div[4]/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div[2]/p')
        await expect(need_pair).to_be_visible()
        pair = await need_pair.inner_text()
        if pair == 'JLP-USDT':
            await need_pair.click()
        else:
            print('Ошибка, не нашел нужную пару')


        # try:
        #     create_pool_btn = met_page.locator('//*[@id="__next"]/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/a')
        #     await expect(create_pool_btn).to_be_visible()
        #     await create_pool_btn.click()
        # except Exception as e:
        #     print('НЕ нашел кнопку')

        await met_page.wait_for_timeout(500)

        try:
            await met_page.wait_for_selector('a[href="/dlmm/C1e2EkjmKBqx8LPYr2Moyjyvba4Kxkrkrcy5KuTEYKRH"]', state='visible')
            goto_jlp_usdt_poll = met_page.locator('a[href="/dlmm/C1e2EkjmKBqx8LPYr2Moyjyvba4Kxkrkrcy5KuTEYKRH"]')
            await expect(goto_jlp_usdt_poll).to_be_attached()
            await goto_jlp_usdt_poll.click()
            print('Першел в пул JLP - USDT')
        except Exception as e:
            print('Не нашел список')

        await met_page.wait_for_load_state(state='domcontentloaded')

        add_position_btn = met_page.locator('span:has-text("Add Position")').first
        await add_position_btn.scroll_into_view_if_needed(timeout=10000)
        await expect(add_position_btn).to_be_visible(timeout=20000)
        await add_position_btn.click()
        print('Нажал Add Position')

        await met_page.wait_for_timeout(500)


        # Input с минимальным price
        input = met_page.locator('input[placeholder="0.00"]').nth(2) #nth(3) для макс
        await met_page.wait_for_selector('input[placeholder="0.00"]', state='visible', timeout=20000)

        await input.scroll_into_view_if_needed(timeout=30000)
        # Проверяем, существует ли элемент
        if await input.count() > 0:
            min_price = await input.input_value()  # Получаем значение из input


        # Input с максимальным price
        input2 = met_page.locator('input[placeholder="0.00"]').nth(3)  # nth(3) для макс
        await met_page.wait_for_selector('input[placeholder="0.00"]', state='visible', timeout=20000)

        await input2.scroll_into_view_if_needed(timeout=30000)
        # Проверяем, существует ли элемент
        if await input2.count() > 0:
            max_price = await input2.input_value()  # Получаем значение из input


        while True:
            data = api.check_pool_activity(min_price, max_price)
            await send_message(message=message, data=data)
            await asyncio.sleep(600)






if __name__ == "__main__":
    asyncio.run(main())