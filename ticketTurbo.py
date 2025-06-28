from selenium import webdriver
import json
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium_stealth import stealth
from fake_useragent import UserAgent

stealth_conf = {
    "languages_options": [
        [
            "en-US",
            "en"
        ],
        [
            "en-GB",
            "en"
        ],
        [
            "en-AU",
            "en"
        ],
        [
            "fr-FR",
            "fr"
        ],
        [
            "de-DE",
            "de"
        ],
        [
            "es-ES",
            "es"
        ],
        [
            "it-IT",
            "it"
        ],
        [
            "nl-NL",
            "nl"
        ],
        [
            "pt-PT",
            "pt"
        ],
        [
            "ru-RU",
            "ru"
        ]
    ],
    "vendor_options": [
        "Google Inc.",
        "Mozilla Corporation",
        "Apple Inc.",
        "Opera Software ASA",
        "Microsoft Corporation",
        "Brave Software",
        "Amazon.com, Inc.",
        "Oracle Corporation",
        "Adobe Inc.",
        "IBM Corporation"
    ],
    "platform_options": [
        "Win32",
        "Linux x86_64",
        "MacIntel",
        "FreeBSD amd64",
        "OpenBSD amd64",
        "NetBSD",
        "Linux armv8l",
        "Linux i686",
        "Win64",
        "Linux aarch64"
    ],
    "webgl_vendor_options": [
        "Intel Inc.",
        "NVIDIA Corporation",
        "AMD",
        "Microsoft Corporation",
        "Apple Inc.",
        "Google Inc.",
        "Mozilla",
        "Opera Software",
        "Qualcomm",
        "ARM"
    ],
    "renderer_options": [
        "Intel Iris OpenGL Engine",
        "GeForce GTX 1070/PCIe/SSE2",
        "AMD Radeon R9 M370X OpenGL Engine",
        "ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)",
        "Mesa DRI Intel(R) HD Graphics 6000 (Broadwell GT3)",
        "ANGLE (NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Radeon (TM) RX 470 Graphics Direct3D11 vs_5_0 ps_5_0)",
        "NVIDIA GeForce GT 750M OpenGL Engine",
        "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon(TM) R4 Graphics Direct3D11 vs_5_0 ps_5_0)"
    ]
}


proxies = open('proxies.txt').read().splitlines()
USEPROXY = True

def get_next_proxy(proxy_id):

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL

    if proxy_id:
        next_proxy = proxies[proxy_id % len(proxies)]
    else:
        next_proxy = proxies[0]    

    print(f"[+] Using proxy: {next_proxy}")

    proxy.http_proxy = next_proxy
    proxy.ssl_proxy = next_proxy
    
    capabilities = webdriver.DesiredCapabilities.CHROME
    capabilities['proxy'] = {
        "httpProxy":next_proxy,
        "ftpProxy":next_proxy,
        "sslProxy":next_proxy,
        "noProxy":None,
        "proxyType":"manual",
        "class":"org.openqa.selenium.Proxy",
        "autodetect":False
    }

    # return capabilities #with normal selenium browser
    return next_proxy #with undetected_chromedriver


def generate_random_headers():
    ua = UserAgent()
    user_agent = ua.random
    return user_agent

def generate_random_screen_size(min_width=800, max_width=1920, min_height=600, max_height=1080):
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    return width, height

def generate_options(proxy_id):

    options = Options()
    
    # options.add_argument("--headless")
    # options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')
    # options.add_argument("--disable-infobars")
    # user_agent = generate_random_headers()
    # options.add_argument(f'--user-agent={user_agent}')
    
    width, height = generate_random_screen_size()
    options.add_argument(f"--window-size={width},{height}")
    
    next_proxy = get_next_proxy(proxy_id)
    options.add_argument(f"--proxy-server={next_proxy}")  
    # options.add_argument("--proxy-bypass-list=*")
    
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    # options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-bundled-ppapi-flash")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument('--disable-popup-blocking')

    preferences = {
            "webrtc.ip_handling_policy": "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
    
    #===== arguments with normal selenium browser =========
                    
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)
    # options.add_experimental_option("prefs", preferences)
    
    return options

def get_driver(proxy_id):

    options = generate_options(proxy_id)
    
    # if USEPROXY:
    #     capabilities = get_next_proxy(proxy_id)
    #     for key, value in capabilities.items():
    #         options.set_capability(key, value)
        
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # … inside get_driver() before uc.Chrome()
    driver = uc.Chrome(options=options, version_main=132)
    #driver = uc.Chrome(options=options)
    
    languages = random.choice(stealth_conf['languages_options'])
    vendor = random.choice(stealth_conf['vendor_options'])
    platform = random.choice(stealth_conf['platform_options'])
    webgl_vendor = random.choice(stealth_conf['webgl_vendor_options'])
    renderer = random.choice(stealth_conf['renderer_options'])
    
    stealth(driver,
            languages=languages,
            vendor=vendor,
            platform=platform,
            webgl_vendor=webgl_vendor,
            renderer=renderer,
            fix_hairline=True,
        )
 
    return driver

def human_typing(element: WebElement, text: str, min_delay: float = 0.05, max_delay: float = 0.25):
   
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def reject_cookies_if_present(driver, timeout=10):
    try:
        # Wait until the 'Reject All' button is located or timeout expires
        reject_all_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
        )
        reject_all_button.click()
        print("Clicked 'Reject All' on the cookies pop-up.")
    except:
        # If the button isn't found within the timeout, we assume it's not there
        print("'Reject All' button was not found within the timeout period.")


def account_login(driver, email, password):
    
    print("[+] Logging in...")
    driver.get("https://www.ticketmaster.fr/en/identification")
    
    reject_cookies_if_present(driver)
    
    #print page source
    # print(driver.page_source)
    
    email_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )
    human_typing(email_element, email)

    password_element = driver.find_element(By.ID, "login-password")
    human_typing(password_element, password)

    login_button = driver.find_element(By.CLASS_NAME, "btn.btn-special.btn-wide.btn-large")
    login_button.click()
    
    wait = input("Press Enter to continue...")
    
def fetch_event_price(driver, event_url):
    # Open the event URL in a new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(event_url)
    
    price = "Not Available"
    for i in range(10):
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, ".event-header-price-offer-price")
            price = price_element.text.strip().split("\n")[-1]  # Extracting the last line which contains the price
            break
        except:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, "p.event-result-pricing span.price")
                price = price_element.text.strip().split("\n")[-1]  # Extracting the last line which contains the price
                break
            except:
                pass
        
        time.sleep(1)    
            
    # Close the current tab and switch back to the original one
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print(f"[+] Fetched price for {event_url}: {price}")
    
    return price 

def scrape_events_data(driver, category_link):
    
    print(f"[+] Scraping events from: {category_link}")
    driver.get(category_link)
    # print(driver.page_source)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'side-events-best-sellers')))
    events_section = driver.find_elements(By.XPATH, "//section[@class='side-events-best-sellers']/ul/li")
    
    events_data = []
    
    for event in events_section:
        # Extracting the text from the 'first' span which contains title, place, and date
        full_text = event.find_element(By.CLASS_NAME, "first").text.strip()
        print("Full Text: ", full_text)
        lines = full_text.split('\n')
        
        # Assuming 'title' and 'place' are always present before 'date'
        title = lines[0] if len(lines) > 0 else ""
        place = lines[1] if len(lines) > 1 else ""
        
        # The 'date' may follow 'place' if it exists
        date_text = lines[2] if len(lines) > 2 else "Date Not Available"
        
        url = event.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        print(f"[+] Scraping event: {title}")
        
        # Assuming fetch_event_price function as previously described
        price = fetch_event_price(driver, url)
        
        events_data.append({
            "title": title,
            "place": place,
            "date": date_text,
            "url": url,
            "price": price
        })
    
    print(f"[+] Scraped {len(events_data)} events.")
    return events_data

def test():
    driver = get_driver(0)

    try:
        email = "ericwelsson@gmail.com"
        password = "MmZz@#15678"
        account_login(driver, email, password)
        
        test_category= 'https://www.ticketmaster.fr/en/theatre/comedie'
        events_data = scrape_events_data(driver, test_category)
        
        with open('events_data.json', 'w') as f:
            json.dump(events_data, f, indent=4)
        
    except Exception as e:
        print(f"[-] Error: {e}")     

    wait = input("Press Enter to continue...")
    driver.quit()


if __name__ == "__main__":
    test()