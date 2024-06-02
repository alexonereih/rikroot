import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pickle
import requests
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--window-size=1920,1080')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10, poll_frequency=1)


#  VVV --- Throttling options (Slow 3G) --- VVV
#
# driver.set_network_conditions(
#     offline=False,
#     latency=5,  # additional latency (ms)
#     download_throughput=250 * 1024,  # maximal throughput
#     upload_throughput=250 * 1024)  # maximal throughput

#  ====================================================================================================================

base_url = 'https://crm.v3.ukrik.com'

def test_ui_login_smoke():

    admin_login = '123'
    admin_password = '123'
    driver.get(base_url)

    # Login page check
    try:
        wait.until(EC.url_to_be(f'{base_url}/login?redirect=%2F'))
    except TimeoutException:
        raise TimeoutException('Error while validating <URL>')


    try:
        wait.until(EC.title_contains('RIK ROOT | Авторизация'))
    except TimeoutException:
        raise TimeoutException('Error while validating <title>')


    # Search locators
    try:
        login_field = wait.until(EC.visibility_of_element_located(('id', 'login.email_input')))
    except TimeoutException:
        raise TimeoutException('Error while searching <Email> field')


    try:
        password_field = wait.until(EC.visibility_of_element_located(('id', 'login.password_input')))
    except TimeoutException:
        raise TimeoutException('Error while searching <Password> field')


    try:
        signin_btn = wait.until(EC.visibility_of_element_located(('id', 'login.submit_btn')))
    except TimeoutException:
        raise TimeoutException('Error while searching <Sign in> button')


    try:
        cancel_btn = wait.until(EC.visibility_of_element_located(('id', 'login.cancel_btn')))
    except TimeoutException:
        raise TimeoutException('Error while searching <Cancel> button')


    # Validating Email field
    login_field.clear()
    login_field.send_keys(admin_login)
    assert login_field.get_attribute('value') == admin_login, 'Error while validating <Email> field'


    # Validating Password field
    password_field.clear()
    password_field.send_keys(admin_password)
    assert password_field.get_attribute('value') == admin_password, 'Error while validating <Password> field'


    # Login verification
    try:
        wait.until(EC.element_to_be_clickable(signin_btn)).click()
    except TimeoutException:
        raise TimeoutException('Error while clicking on <sign in> button')


    # Redirect on CRM
    try:
        wait.until(EC.url_contains(base_url))
        wait.until(EC.title_is('RIK ROOT | Дашборд | Сводка'))
    except TimeoutException:
        raise TimeoutException('Error while validating <main page>')


    # Save cookies
    pickle.dump(driver.get_cookies(), open(os.getcwd() + '/login_cookies.pkl', 'wb'))


# Дашборд | Сводка
def test_ui_dashboard():

    try:
        wait.until(EC.url_contains(base_url))
        wait.until(EC.title_is('RIK ROOT | Дашборд | Сводка'))
        wait.until(EC.visibility_of(driver.find_element('id', 'line-char3t')))
        wait.until(EC.visibility_of(driver.find_element('id', 'pie-chart')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Дашборд | Сводка> page')


# Выплаты | Расчет
def test_ui_tenants_income():
    driver.get(f'{base_url}/tenantsIncome')
    try:
        wait.until(EC.url_contains(f'{base_url}/tenantsIncome'))
        wait.until(EC.element_to_be_clickable(('xpath', '//span[text()=" Рассчитать всех "]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Выплаты | Расчет> page')


# Выплаты | Расчет V2
def test_ui_tenants_income_v2():
    driver.get(f'{base_url}/tenantsIncomeV2')
    try:
        wait.until(EC.url_contains(f'{base_url}/tenantsIncomeV2'))
        wait.until(EC.presence_of_element_located(('xpath', '//div[@class="el-tabs__item is-top is-active"]')))
        # wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="Сумма:"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Выплаты | Расчет V2> page')


# Смены
def test_ui_schedule():
    driver.get(f'{base_url}/shedule')
    try:
        wait.until(EC.url_contains(f'{base_url}/shedule'))
        wait.until(EC.presence_of_element_located(('xpath', '//div[@class="table-top-dates__item"][1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Выплаты | Расчет V2> page')


# Ежемесячный отчет
def test_ui_report_consolidated():
    driver.get(f'{base_url}/report/consolidated')
    try:
        wait.until(EC.url_contains(f'{base_url}/report/consolidated'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="ИТОГО"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Ежемесячный отчет> page')


    # Ежемесячный отчет по Т.О.
def test_ui_report_tech_inspection_report():
    driver.get(f'{base_url}/report/techInspectionReport')
    try:
        wait.until(EC.url_contains(f'{base_url}/report/techInspectionReport'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="ИТОГО"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Ежемесячный отчет по Т.О.> page')


    # Водители
def test_ui_tenants_info():
    driver.get(f'{base_url}/tenantsInfo')
    try:
        wait.until(EC.url_contains(f'{base_url}/tenantsInfo'))
        details_driver_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(details_driver_btn))
        wait.until(EC.element_to_be_clickable(details_driver_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Водители> page')


    # Реестр должников по балансам
def test_ui_debtors_by_balance():
    driver.get(f'{base_url}/debtors_by_balances')
    try:
        wait.until(EC.url_contains(f'{base_url}/debtors_by_balances'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="Итого"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Реестр должников по балансам> page')

    # Реестр по депозитам
def test_ui_driver_deposit_debts():
    driver.get(f'{base_url}/driver_deposit_debts')
    try:
        wait.until(EC.url_contains(f'{base_url}/driver_deposit_debts'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="Итого"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Реестр по депозитам> page')

    # Резерв
def test_ui_tenants_candidates_info():
    driver.get(f'{base_url}/tenantsCandidatesInfo')
    try:
        wait.until(EC.url_contains(f'{base_url}/tenantsCandidatesInfo'))
        create_candidate_btn = 'xpath', '(//button[@class="el-button el-button--default is-circle el-popover__reference"])'
        wait.until(EC.visibility_of_element_located(create_candidate_btn))
        wait.until(EC.element_to_be_clickable(create_candidate_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Резерв> page')


    # Реестр по доплатам ------------- ПЛОХИЕ ПРОВЕРКИ, ПЕРЕПИСАТЬ
def test_ui_driver_surcharge():
    driver.get(f'{base_url}/driverSurcharge')
    try:
        wait.until(EC.url_contains(f'{base_url}/driverSurcharge'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[@style="display: none;"])[1]')))
        # preloader = 'xpath', '//div[@class="el-loading-parent--relative"]'
        # wait.until(EC.visibility_of_element_located(preloader))
        # wait.until(EC.invisibility_of_element_located(preloader))

    except TimeoutException:
        raise TimeoutException('Error while validating <Реестр по доплатам> page')


    # Реестр по выплатам
def test_ui_driver_give_out_amount():
    driver.get(f'{base_url}/driverGiveOutAmount')
    try:
        wait.until(EC.url_contains(f'{base_url}/driverGiveOutAmount'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[text()="Итого"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Реестр по выплатам> page')


    # Реестр должников  ------------- ПЛОХИЕ ПРОВЕРКИ, ПЕРЕПИСАТЬ
def test_ui_open_transactions_debts():
    driver.get(f'{base_url}/OpenTransactionsDebts')
    try:
        wait.until(EC.url_contains(f'{base_url}/OpenTransactionsDebts'))
        wait.until(EC.presence_of_element_located(('xpath', '(//div[@style="display: none;"])[1]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Реестр должников> page')


    # Автопарк
def test_ui_carpark():
    driver.get(f'{base_url}/carpark')
    try:
        wait.until(EC.url_contains(f'{base_url}/carpark'))
        details_auto_btn = 'xpath', '(//button[@class="el-button el-button--info el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(details_auto_btn))
        wait.until(EC.element_to_be_clickable(details_auto_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Автопарк> page')


    # Парки
def test_ui_local_park():
    driver.get(f'{base_url}/localCarPark')
    try:
        wait.until(EC.url_contains(f'{base_url}/localCarPark'))
        details_park_btn = 'id', 'parks.more_btn_0'
        wait.until(EC.visibility_of_element_located(details_park_btn))
        wait.until(EC.element_to_be_clickable(details_park_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Парки> page')


     # Договоры ----------- TPA TATA


    # Собственники авто
def test_ui_investors():
    driver.get(f'{base_url}/investors')
    try:
        wait.until(EC.url_contains(f'{base_url}/investors'))
        details_investors_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(details_investors_btn))
        wait.until(EC.element_to_be_clickable(details_investors_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Собственники авто> page')


    # Т.О Заявки
def test_ui_tech_inspection():
    driver.get(f'{base_url}/techInspection')
    try:
        wait.until(EC.url_contains(f'{base_url}/techInspection'))
        wait.until(EC.presence_of_element_located(('xpath', '//h2[text()=" Заявки без снятия с линии "]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Т.О Заявки> page')


    # Т.О. Ремонты
def test_ui_tech_inspection_reports():
    driver.get(f'{base_url}/techInspection/repairs')
    try:
        wait.until(EC.url_contains(f'{base_url}/techInspection/repairs'))
        wait.until(EC.presence_of_element_located(('xpath', '//div[@class="current-tech-inspection"]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Т.О. Ремонты> page')


    # Т.О. История
def test_ui_tech_inspection_history():
    driver.get(f'{base_url}/techInspection/history')
    try:
        wait.until(EC.url_contains(f'{base_url}/techInspection/history'))
        wait.until(EC.presence_of_element_located(('xpath', '//div[@class="tech-inspection-history"]')))

    except TimeoutException:
        raise TimeoutException('Error while validating <Т.О. История> page')


    # Склад | Поставщики
    # driver.get(f'{base_url}/parts/providers')
    #
    # try:
    #     wait.until(EC.url_contains(f'{base_url}/parts/providers'))
    #     edit_provider_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
    #     wait.until(EC.visibility_of_element_located(edit_provider_btn))
    #     wait.until(EC.element_to_be_clickable(edit_provider_btn))
    #     print('🟢 Склад | Поставщики - PASSED')
    #
    # except TimeoutException:
    #     print('🔴 Склад | Поставщики - FAILED')
    #     raise TimeoutException('Error while validating <Склад | Поставщики> page')
    #
    # # Склад | Склад
    # driver.get(f'{base_url}/parts/storage')
    #
    # try:
    #     wait.until(EC.url_contains(f'{base_url}/parts/storage'))
    #     wait.until(EC.presence_of_element_located(('xpath', '//button[@class="el-button el-button--primary el-button--mini is-round"][1]')))
    #     print('🟢 Склад | Поставщики - PASSED')
    #
    # except TimeoutException:
    #     print('🔴 Склад | Поставщики - FAILED')
    #     raise TimeoutException('Error while validating <Склад | Поставщики> page')
    #
    # # Склад | Заказы
    # driver.get(f'{base_url}/parts/orders')
    #
    # try:
    #     wait.until(EC.url_contains(f'{base_url}/parts/orders'))
    #     edit_order_btn = 'xpath', '(//button[@class="el-button el-button--default el-button--small is-circle"])[1]'
    #     wait.until(EC.visibility_of_element_located(edit_order_btn))
    #     wait.until(EC.element_to_be_clickable(edit_order_btn))
    #
    #     details_order_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
    #     wait.until(EC.visibility_of_element_located(details_order_btn))
    #     wait.until(EC.element_to_be_clickable(details_order_btn))
    #
    #     print('🟢 Склад | Заказы - PASSED')
    #
    # except TimeoutException:
    #     print('🔴 Склад | Заказы - FAILED')
    #     raise TimeoutException('Error while validating <Склад | Заказы> page')
    #
    # # Склад | Позиции
    # driver.get(f'{base_url}/parts/items')
    #
    # try:
    #     wait.until(EC.url_contains(f'{base_url}/parts/items'))
    #     edit_item_btn = 'xpath', '(//button[@class="el-button el-button--primary el-button--mini is-round"][1]'
    #     wait.until(EC.visibility_of_element_located(edit_item_btn))
    #     wait.until(EC.element_to_be_clickable(edit_item_btn))
    #     print('🟢 Склад | Позиции - PASSED')
    #
    # except TimeoutException:
    #     print('🔴 Склад | Позиции - FAILED')
    #     raise TimeoutException('Error while validating <Склад | Позиции> page')

    # Склад | Списания
    # Склад | Заявки на пеермещение
    # Склад | История перемещений
    # Склад | Движение по складу





    # Склад | Категории
def test_ui_parts_categories():
    driver.get(f'{base_url}/parts/categories')
    try:
        wait.until(EC.url_contains(f'{base_url}/parts/categories'))
        edit_category_btn = 'xpath', '(//button[@class="el-button el-button--default el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(edit_category_btn))
        wait.until(EC.element_to_be_clickable(edit_category_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Склад | Категории> page')


    # Склад | Запчасти
def test_ui_parts_parts():
    driver.get(f'{base_url}/parts/parts')
    try:
        wait.until(EC.url_contains(f'{base_url}/parts/parts'))
        edit_parts_btn = 'xpath', '(//button[@class="el-button el-button--primary el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(edit_parts_btn))
        wait.until(EC.element_to_be_clickable(edit_parts_btn))
    except TimeoutException:
        raise TimeoutException('Error while validating <Склад | Запчасти> page')


    # Штрафы
def test_ui_fines():
    driver.get(f'{base_url}/fines')
    try:
        wait.until(EC.url_contains(f'{base_url}/fines'))
        preloader_off = 'xpath', '(//div[@style="display: none;"])[1]'
        wait.until(EC.presence_of_element_located(preloader_off))

    except TimeoutException:
        raise TimeoutException('Error while validating <Штрафы> page')


     # ЭДО | Оферта
def test_ui_offer():
    driver.get(f'{base_url}/offer')
    try:
        wait.until(EC.url_contains(f'{base_url}/offer'))
        preloader_off = 'xpath', '(//div[@style="display: none;"])[1]'
        wait.until(EC.presence_of_element_located(preloader_off))
        create_offer_btn = 'xpath', '(//button[@class="el-button el-button--default is-circle el-popover__reference"])[1]'
        wait.until(EC.visibility_of_element_located(create_offer_btn))
        wait.until(EC.element_to_be_clickable(create_offer_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Штрафы> page')


    # Администраторы
def test_ui_admins():
    driver.get(f'{base_url}/admins')
    try:
        wait.until(EC.url_contains(f'{base_url}/admins'))
        edit_admins_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(edit_admins_btn))
        wait.until(EC.element_to_be_clickable(edit_admins_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Администраторы> page')


    # Роли
def test_ui_roles():
    driver.get(f'{base_url}/roles')
    try:
        wait.until(EC.url_contains(f'{base_url}/roles'))
        edit_role_btn = 'xpath', '(//button[@class="el-button el-button--warning el-button--mini is-round"])[1]'
        wait.until(EC.visibility_of_element_located(edit_role_btn))
        wait.until(EC.element_to_be_clickable(edit_role_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Роли> page')


    # Ключи CRM
def test_ui_crm_keys():
    driver.get(f'{base_url}/crm/keys')
    try:
        wait.until(EC.url_contains(f'{base_url}/crm/keys'))
        preloader_off = 'xpath', '(//div[@style="display: none;"])[1]'
        wait.until(EC.presence_of_element_located(preloader_off))
        edit_key_btn = 'xpath', '(//button[@class="el-button el-button--text"])[1]'
        wait.until(EC.visibility_of_element_located(edit_key_btn))
        wait.until(EC.element_to_be_clickable(edit_key_btn))

    except TimeoutException:
        raise TimeoutException('Error while validating <Ключи CRM> page')




