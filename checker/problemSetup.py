from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import shutil
from dotenv import load_dotenv
import json
import requests
import zipfile

# === SETTINGS ===
BASE_URL = "https://grader.nattee.net"
LOGIN_URL = BASE_URL
ROOT_DIR = os.path.dirname(__file__)

CONFIG_DIR = os.path.join(ROOT_DIR, "config.json")
with open(CONFIG_DIR, "r") as fin:
    config = json.load(fin)

PROBLEM_CAT = config["py"]["problem_cat"]

ORDER_DIR = os.path.join(ROOT_DIR, "../order.txt")
with open(ORDER_DIR, "r") as f:
    for line in f:
        if PROBLEM_CAT in line:
            PROBLEM_TARGET = next(f, None).strip()
            break

PROBLEM_PATH = f"../{PROBLEM_CAT}/{PROBLEM_TARGET}"
PROBLEM_DIR = os.path.join(ROOT_DIR, PROBLEM_PATH)
DOWNLOAD_TEMP_DIR = os.path.join(ROOT_DIR, "temp")
ZIP_PATH = os.path.join(DOWNLOAD_TEMP_DIR, "problem.zip")
os.makedirs(DOWNLOAD_TEMP_DIR, exist_ok=True)

load_dotenv()
NAME = os.getenv("NAME")
PASSWORD = os.getenv("PASSWORD")

# === CHROME OPTIONS ===
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # modern headless
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_TEMP_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_setting_values.automatic_downloads": 1
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# === 1. LOGIN ===
print("Waiting for login page...")
driver.get(LOGIN_URL)
print("logging in...")
time.sleep(2)
driver.find_element(By.ID, "login").send_keys(NAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.NAME, "commit").click()
print("logged in!")
time.sleep(3)


# === 2. GET THE PROBLEM FILES ===
print(f"Extracting problem: {PROBLEM_TARGET}")
problem_cells = driver.find_elements(
    By.CSS_SELECTOR,
    'tbody[data-controller="problem-name"] tr td:nth-of-type(2)'
)

testcase_name = None
problem_number = None
isProblem = False
for td in problem_cells:
    strong = td.find_element(By.TAG_NAME, "strong")
    problem_name = problem_name = strong.parent.execute_script(
        "return arguments[0].childNodes[0].textContent.trim();", strong
    ).strip().lower().replace(" ", "")
    if problem_name == PROBLEM_TARGET.lower().strip().replace(" ", ""):
        print("Problem found!")
        isProblem = True
        # extract testcase name
        testcase_name = td.find_element(
            By.CSS_SELECTOR,
            "div.text-muted.font-monospace"
        ).text.strip()
        
        # extract problem num
        read_link = td.find_element(
            By.CSS_SELECTOR,
            'a[href*="download/statement"]'
        ).get_attribute("href")
        problem_number = int(read_link.split("/")[4])

        # Try to get file link
        file_elems = td.find_elements(
            By.CSS_SELECTOR,
            'a[href*="download/attachment"]'
        )

        file_link = file_elems[0].get_attribute("href") if file_elems else None
        break

if testcase_name:
    print(f"Testcase name: {testcase_name}")
else:
    print("Testcase not found...")

if problem_number:
    print(f"Problem Num: {problem_number}")
else:
    print("Problem num not found")

config["py"]["problem_num"] = problem_number
config["cpp"]["test_case"] = testcase_name

if file_link:
# === 3. DOWNLOAD AND EXTRACT THE FILES ===
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])

    print("Downloading the zipfile...")
    r = session.get(file_link)
    with open(ZIP_PATH, "wb") as f:
        f.write(r.content)

    # Check if the file is a valid zip
    is_zip = zipfile.is_zipfile(ZIP_PATH)

    if is_zip:
        print("Extracting the zip file...")
        os.makedirs(PROBLEM_DIR, exist_ok=True)
        try:
            with zipfile.ZipFile(ZIP_PATH, 'r') as z:
                for file in z.namelist():
                    # Select only .cpp and .h
                    if file.endswith(".cpp") or file.endswith(".h"):
                        file_type = ".cpp" if file.endswith(".cpp") else ".h"
                        print(f"{file_type} found!")
                        extracted_path = z.extract(file, "temp_extract")

                        base_name = os.path.basename(file)
                        dest_path = os.path.join(PROBLEM_DIR, base_name)
                        
                        print(f"Moving {file_type} file to {dest_path}...")
                        shutil.move(extracted_path, dest_path)

            config["cpp"]["path"] = PROBLEM_PATH + "/main.cpp"
        except Exception as e:
            print(f"Error extracting zip: {e}")

    else:
        print("File is not a zip — treating it as a .cpp file.")
        # New file path = parent/probdir.cpp   (no folder created)
        new_cpp_path = PROBLEM_DIR + ".cpp"

        print(f"Renaming {ZIP_PATH} → {new_cpp_path}")
        shutil.move(ZIP_PATH, new_cpp_path)

        # Update config and STOP (do not delete the file)
        config["cpp"]["path"] = PROBLEM_PATH + ".cpp"

    # CLEANUP ZIP FILE
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    # CLEANUP temp_extract folder
    if os.path.exists("temp_extract"):
        shutil.rmtree("temp_extract")



    with open(CONFIG_DIR, "w") as fout:
        json.dump(config, fout, indent=2)
    print("New config for this problem have been saved!")

    print("Problem setup done!")

elif isProblem:
    open(f"{PROBLEM_DIR}.cpp", "w").close()
    config["cpp"]["path"] = PROBLEM_PATH + ".cpp"

    with open(CONFIG_DIR, "w") as fout:
        json.dump(config, fout, indent=2)
    print("New config for this problem have been saved!")

    print("Problem setup done!")
    
else:
    print("Problem not found...")