import requests
import time


def check_pool_activity(min_price, max_price):
    while True:
        response = requests.get('https://dlmm-api.meteora.ag/pair/all_by_groups')
        if response.status_code == 200:
            data = response.json()
            meteora = data['groups']


            for group in meteora:
                for pair in group['pairs']:
                    if pair['address'] == 'C1e2EkjmKBqx8LPYr2Moyjyvba4Kxkrkrcy5KuTEYKRH':
                        jlp_usdt_data = pair

            print(jlp_usdt_data)

            bin_step = jlp_usdt_data['bin_step']
            base_fee = jlp_usdt_data['base_fee_percentage']
            pool_tvl = jlp_usdt_data['liquidity']
            fees_24h = jlp_usdt_data['fees_24h']
            current_price_jlp = jlp_usdt_data['current_price']

            answer = (f'Pool TVL: {pool_tvl} \n'
                      f'Bin-step: {bin_step} \n'
                      f'Base Fee: {base_fee} \n'
                      f'24h Fee: {fees_24h} \n'
                      f'JLP Price: {current_price_jlp}'
                      )

            # print(answer)
            data = (f'MIN PRICE: {min_price}\n'
                    f'MAX PRICE: {max_price}\n'
                    f'-------------------------\n'
                    f'CURRENT PRICE: {current_price_jlp}')
            return data





        else:
            print('Ошибка в запросе к API METEORA')





    # import requests
    # import time
    #
    #
    # def fetch_data():
    #     response = requests.get('https://dlmm-api.meteora.ag/pair/all_by_groups')
    #
    #     if response.status_code == 200:
    #         data = response.json()
    #         meteora = data['groups']
    #
    #         for group in meteora:
    #             for pair in group['pairs']:
    #                 if pair['address'] == 'C1e2EkjmKBqx8LPYr2Moyjyvba4Kxkrkrcy5KuTEYKRH':
    #                     jlp_usdt_data = pair
    #
    #         print(jlp_usdt_data)
    #
    #         bin_step = jlp_usdt_data['bin_step']
    #         base_fee = jlp_usdt_data['base_fee_percentage']
    #         pool_tvl = jlp_usdt_data['liquidity']
    #         fees_24h = jlp_usdt_data['fees_24h']
    #         current_price_jlp = jlp_usdt_data['current_price']
    #
    #         answer = (f'Pool TVL: {pool_tvl} n'
    #                   f'Bin-step: {bin_step} n'
    #                   f'Base Fee: {base_fee} n'
    #                   f'24h Fee: {fees_24h} n'
    #                   f'JLP Price: {current_price_jlp}'
    #                   )
    #
    #         print(answer)
    #     else:
    #         print('Ошибка')
    #
    #
    # # Основной цикл
    # while True:
    #     fetch_data()
    #     time.sleep(300)  # Задержка в 5 минут (300 секунд)
    #

