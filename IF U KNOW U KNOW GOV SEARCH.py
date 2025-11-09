import requests
from bs4 import BeautifulSoup
import webbrowser
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

HUNTER_API_KEY = "your_hunter_api_key"
NUMVERIFY_API_KEY = "your_numverify_api_key"
HIBP_API_KEY = "your_hibp_api_key"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-GB,en;q=0.9"
}

def validate_email(email):
    print(Fore.RED + "\n[+] Validating Email with Hunter.io...")
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()["data"]
            print(Fore.GREEN + f"  Email: {data.get('email')}")
            print(Fore.GREEN + f"  Result: {data.get('result')}")
            print(Fore.GREEN + f"  Score: {data.get('score')}")
            print(Fore.GREEN + f"  Domain: {data.get('domain')}")
            print(Fore.GREEN + f"  MX Records: {data.get('mx_records')}")
        else:
            print(Fore.RED + "  Error: Could not validate email.")
    except Exception as e:
        print(Fore.RED + f"  Error: {e}")

def hibp_email_check(email):
    print(Fore.PURPLE + "\n[+] Checking HaveIBeenPwned for breaches...")
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "user-agent": "gov-info-search",
        "accept-language": "en-GB,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(Fore.GREEN + f"  Found in {len(breaches)} breach(es):")
            for breach in breaches:
                print(Fore.CYAN + f"    - {breach['Name']} ({breach['BreachDate']})")
        elif response.status_code == 404:
            print(Fore.GREEN + "  No breaches found.")
        else:
            print(Fore.RED + f"  Error: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"  Error: {e}")

def phone_lookup(phone):
    print(Fore.BLUE + "\n[+] Looking up phone via NumVerify...")
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("valid"):
                print(Fore.GREEN + f"  Country: {data['country_name']} ({data['country_code']})")
                print(Fore.GREEN + f"  Location: {data['location']}")
                print(Fore.GREEN + f"  Carrier: {data['carrier']}")
                print(Fore.GREEN + f"  Line Type: {data['line_type']}")
            else:
                print(Fore.RED + "  Invalid phone number.")
        else:
            print(Fore.RED + "  Error: Could not reach NumVerify.")
    except Exception as e:
        print(Fore.RED + f"  Error: {e}")

def vin_lookup(vin):
    print(Fore.YELLOW + "\n[+] Decoding VIN using NHTSA API...")
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin}?format=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()["Results"][0]
            print(Fore.GREEN + f"  Make: {data.get('Make')}")
            print(Fore.GREEN + f"  Model: {data.get('Model')}")
            print(Fore.GREEN + f"  Year: {data.get('ModelYear')}")
            print(Fore.GREEN + f"  Body Class: {data.get('BodyClass')}")
            print(Fore.GREEN + f"  Vehicle Type: {data.get('VehicleType')}")
        else:
            print(Fore.RED + "  Error: Failed to decode VIN.")
    except Exception as e:
        print(Fore.RED + f"  Error: {e}")

def scrape_skymem(email):
    print(Fore.MAGENTA + f"\n[+] Scraping skymem.info for email: {email}")
    url = f"https://www.skymem.info/srch?q={email}&ss=home"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(Fore.RED + "  Skymem search failed.")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        found = False
        for link in links:
            if "mailto:" in link['href'] and email in link['href']:
                print(Fore.GREEN + "  → Found:", link['href'].replace("mailto:", ""))
                found = True
        if not found:
            print(Fore.YELLOW + "  No mentions found.")
    except Exception as e:
        print(Fore.RED + f"  Error during scraping: {e}")

def name_search():
    print(Fore.GREEN + "\n[+] Opening browser for name search...")
    name = input("Enter full name (e.g., john-doe): ").strip().replace(" ", "-")
    state = input("Enter county (e.g., essex): ").strip().lower()
    city = input("Enter city (e.g., london): ").strip().replace(" ", "-").lower()
    
    urls = [
        f"https://www.fastpeoplesearch.com/name/{name}_{city}-{state}",
        f"https://www.searchpeoplefree.com/find/{name}/{state}/{city}",
        f"https://www.peoplesearchnow.com/person/{name}_{city}_{state}",
        f"https://www.truepeoplesearch.com/results?name={name}&citystatezip={city}+{state}",
        f"https://www.spokeo.com/{name}?loaded=1"
    ]
    for url in urls:
        webbrowser.open(url, new=2)

def plate_search():
    print(Fore.GREEN + "\n[+] Opening browser for plate search...")
    plate = input("Enter license plate: ").strip().replace(" ", "")
    state = input("Enter county (e.g., ESSEX): ").strip().upper()

    urls = [
        f"https://www.faxvin.com/license-plate-lookup/result?plate={plate}&state={state}",
        f"https://www.findbyplate.com/UK/{state}/{plate}/"
    ]
    for url in urls:
        webbrowser.open(url, new=2)

def main_menu():
    while True:
        print(Fore.WHITE + "\n========== IF U KNOW U KNOW GOV INFO SEARCH ==========")
        print(Fore.GREEN + "1. Validate Email (Hunter.io)")
        print(Fore.PURPLE + "2. Check Email in Breaches (HIBP)")
        print(Fore.GREEN + "3. Scrape Email Mentions (Skymem)")
        print(Fore.BLUE + "4. Phone Lookup (NumVerify)")
        print(Fore.YELLOW + "5. VIN Lookup (NHTSA)")
        print(Fore.GREEN + "6. Name Search (Web)")
        print(Fore.GREEN + "7. License Plate Search (Web)")
        print(Fore.GREEN + "8. Exit")
        print(Fore.WHITE + "=====================================================")
        choice = input(Fore.GREEN + "Select an option (1–8): ").strip()

        if choice == "1":
            email = input(Fore.GREEN + "Enter email: ").strip()
            validate_email(email)
        elif choice == "2":
            email = input(Fore.GREEN + "Enter email: ").strip()
            hibp_email_check(email)
        elif choice == "3":
            email = input(Fore.GREEN + "Enter email: ").strip()
            scrape_skymem(email)
        elif choice == "4":
            phone = input(Fore.GREEN + "Enter phone number (with country code, e.g., +447900900123): ").strip()
            phone_lookup(phone)
        elif choice == "5":
            vin = input(Fore.GREEN + "Enter VIN number: ").strip()
            vin_lookup(vin)
        elif choice == "6":
            name_search()
        elif choice == "7":
            plate_search()
        elif choice == "8":
            print(Fore.GREEN + "Goodbye.")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()