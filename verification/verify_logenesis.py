from playwright.sync_api import sync_playwright, expect
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Go to testbed
    print("Navigating to testbed...")
    page.goto("http://localhost:8001/light_testbed.html")

    # Select Logenesis
    print("Selecting Logenesis mode...")
    page.select_option("#mode", "logenesis")

    # Test 1: Analyze (Should show Cyan particles)
    print("Sending 'analyze structure' command...")
    page.fill("#voiceInput", "analyze structure")
    page.click("#btnSend")

    # Wait for logs to appear to confirm receipt
    # The log div is #log. We can check if it contains "Logenesis Response"
    # But visual check via sleep is okay for screenshot generation
    time.sleep(2)
    page.screenshot(path="verification/1_logenesis_awake.png")
    print("Screenshot 1 taken.")

    # Test 2: Sleep (Should fade to black)
    print("Sending 'go to sleep' command...")
    page.fill("#voiceInput", "go to sleep")
    page.click("#btnSend")

    time.sleep(2)
    page.screenshot(path="verification/2_logenesis_nirodha.png")
    print("Screenshot 2 taken.")

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
