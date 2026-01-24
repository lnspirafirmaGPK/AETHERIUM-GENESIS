from playwright.sync_api import sync_playwright
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        filepath = os.path.abspath("gunui/living_interface.html")
        url = f"file://{filepath}"

        print(f"Loading {url}")
        page.goto(url)

        # Initial State Check
        page.wait_for_selector("#intent-tag")
        state_text = page.inner_text("#intent-tag")
        print(f"Initial State: {state_text}") # Should be NIRODHA

        # Perform 3-Tap Ritual
        print("Performing Ritual...")
        # We need to target the body or canvas, simulating taps
        # The event listener is on window
        for i in range(3):
            page.mouse.click(100, 100)
            page.wait_for_timeout(200) # Small delay between taps

        # Wait for Awakening
        page.wait_for_timeout(1000)

        # Check State
        state_text = page.inner_text("#intent-tag")
        print(f"Post-Ritual State: {state_text}") # Should be AWAKE

        # Check Log for First Breath
        terminal_text = page.inner_text("#terminal")
        print(f"Terminal Log:\n{terminal_text}")

        if "FIRST_BREATH" in terminal_text or "MEMORY_RECALLED" in terminal_text:
            print("Awakening Log found.")

        # Check Narrative (Phi)
        phi_text = page.inner_text("#phi-val")
        print(f"Narrative: {phi_text}") # Should be MANIFESTATION (since awake sets phi=0.85)

        # RELOAD TO TEST MEMORY
        print("--- Reloading Page ---")
        page.reload()

        # Initial State Check (Should be back to NIRODHA)
        state_text = page.inner_text("#intent-tag")
        print(f"Reload State: {state_text}")

        # Perform Ritual Again
        print("Performing Ritual (Round 2)...")
        for i in range(3):
            page.mouse.click(100, 100)
            page.wait_for_timeout(200)

        page.wait_for_timeout(1000)

        # Check Log for MEMORY
        terminal_text = page.inner_text("#terminal")
        print(f"Terminal Log (Round 2):\n{terminal_text}")

        if "MEMORY_RECALLED" in terminal_text:
            print("SUCCESS: Memory Recalled found!")
        else:
            print("FAILURE: Memory Recalled NOT found.")

        # Screenshot
        page.screenshot(path="/home/jules/verification/gunui_memory.png")
        print("Screenshot saved to /home/jules/verification/gunui_memory.png")

        browser.close()

if __name__ == "__main__":
    run_verification()
