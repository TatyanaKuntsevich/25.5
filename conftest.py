import pytest
@pytest.fixture

def chrome_options(chrome_options):
    chrome_options.binary_location = '/QA/Test/chromedriver.exe'
    #chrome_options.add_extension('/QA/Test/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options

def driver_args():
    return ['--log-level=LEVEL']

def chrome_options(chrome_options):
    chrome_options.set_headless(True)
    return chrome_options