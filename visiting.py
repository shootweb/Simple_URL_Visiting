import threading
import time
import sys
from urllib.parse import urlencode, urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Global flags
paused = False
quit_flag = False

def input_thread():
    global paused, quit_flag
    while not quit_flag:
        try:
            cmd = input("Command (p: pause, c: continue, q: quit): ").strip().lower()
            if cmd == 'q':
                quit_flag = True
                break
            elif cmd == 'p':
                paused = True
                print("Paused. Enter 'c' to continue.")
            elif cmd == 'c':
                paused = False
                print("Resumed.")
        except (EOFError, KeyboardInterrupt):
            quit_flag = True
            break

def read_urls_from_file(file_path):
    """Read URLs from a text file, one per line."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def encode_query_params(url):
    """URL encode the query parameters of a given URL."""
    parsed = urlparse(url)
    if not parsed.query:
        return url
    query_params = parse_qs(parsed.query)
    encoded_query = urlencode(query_params, doseq=True)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{encoded_query}"

# File containing URLs (one per line)
url_file = "urls.txt"

# Read URLs from file
urls = read_urls_from_file(url_file)

# Set up Chrome options (non-headless for viewing)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(options=chrome_options)

# Start the input thread
input_thread_obj = threading.Thread(target=input_thread, daemon=True)
input_thread_obj.start()

print("Starting to open websites. Use the input prompt to pause/continue/quit.")

try:
    for url in urls:
        if quit_flag:
            break
        # Encode query parameters
        encoded_url = encode_query_params(url)
        print(f"Opening: {encoded_url}")
        driver.get(encoded_url)
        remaining = 4.0
        while remaining > 0 and not quit_flag:
            if paused:
                time.sleep(0.1)
            else:
                time.sleep(0.1)
                remaining -= 0.1
        if quit_flag:
            break
finally:
    print("Closing browser.")
    driver.quit()
    sys.exit(0 if not quit_flag else 1)
