#! python3

import requests
import pyautogui
import time
import datetime
import xml.etree.ElementTree as ET

#! Neomanager's password
neo_pass = 'not_the_real_password'

# Get the exchange rates and set them to the dictionary
def get_exchange_rates(xml_url, currency_codes):
    # Fetch XML data from the BNR url
    response = requests.get(xml_url)
    if response.status_code != 200:
        print(f'Failed to fetch XML. Status code: {response.status_code}')
        return None
    # Parse XML content, considering the namespace
    root = ET.fromstring(response.content)
    ns = {'xmlns': 'http://www.bnr.ro/xsd'}
    # Find the Body element
    body_element = root.find('.//xmlns:Body', namespaces=ns)
    if body_element is None:
        print('Body element not found in XML.')
        return None
    # Initialize dictionary to store exchange rates, among the ones that are fixed values decided by the company
    bnr_rates = {
    'EUR': '4.4',
    'GBP': '5.2',
    'USD': '3.2'
}
    # Find the Rate elements within the Body for the specified currency codes
    for rate_element in body_element.iter('{http://www.bnr.ro/xsd}Rate'):
        currency_code = rate_element.get('currency')
        if currency_code in currency_codes:
            bnr_rates[currency_code] = rate_element.text
    return bnr_rates

# URL of the XML containing exchange rates
xml_url = 'https://www.bnr.ro/nbrfxrates.xml'

# List of currency codes to retrieve exchange rates for
currency_codes = ['BGN', 'HUF']

# Get the exchange rates and set them to bnr_rates dictionary
bnr_rates = get_exchange_rates(xml_url, currency_codes)

# Account for the HUF currency format exception
bnr_rates['HUF'] = str(round(float(bnr_rates['HUF'])/100, 4))

# Rearrange values in the order that Neomanager has them
desired_order_list = ['BGN', 'EUR', 'HUF', 'GBP', 'USD']
reordered_rates = {k: bnr_rates[k] for k in desired_order_list}

# Press same key multiple times in a row
def multiple_key_press(key, times):
  for i in range(times):
    pyautogui.press(key)

# Current date
current_date = datetime.datetime.now().strftime("%d%m%Y")

# Send keyboard input to complete field and then enter to move to the next field
def input_rate_in_neomanager(exchange_rate):
    pyautogui.typewrite(exchange_rate)
    pyautogui.press('enter')
    pyautogui.typewrite(exchange_rate)
    multiple_key_press('enter', 2)

# # Start Neomanager and input exchange rates
# Click Neomanager's password input field
pyautogui.click(982, 538)
# Input Neomanager's password
pyautogui.typewrite(neo_pass)
# Click Neomanager's login button
pyautogui.press('enter')
# Pause execution until Neomanager starts
time.sleep(6)
# Take into account the Neomanager's backup notification
pyautogui.press('enter')
# Move Neomanager's window to the half left of the screen
pyautogui.hotkey('win', 'left')
time.sleep(1)
pyautogui.press('esc')
# Select Menu bar -> Parametri -> Cursuri
pyautogui.press(['alt', 'p', 'c', 'c', 'enter'])
# Select the date field
multiple_key_press('left', 2)
# Input the current date
pyautogui.typewrite(current_date)
# Move to and click Aplica button
multiple_key_press('enter', 3)
# Move to first rate
pyautogui.press(['down', 'enter'])
# Input all rates in neomanager
for rate in reordered_rates.values():
    input_rate_in_neomanager(rate)
# Confirm rates form inputs
multiple_key_press('enter', 2)
# Close exchange window
pyautogui.hotkey('alt', 't')
time.sleep(2)
# Go to vanzari and open Factura si aviz
pyautogui.press(['alt', 'v', 'z'])

# Display the position of the mouse live (for development help)
# pyautogui.displayMousePosition()