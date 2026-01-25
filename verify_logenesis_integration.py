import asyncio
import os
import time
from datetime import datetime
from playwright.async_api import async_playwright

async def verify_logenesis_integration():
    """
    Automated Verification Script for Logenesis Integration.
    1. Open PWA (Localhost)
    2. Activate Input (Ctrl+Enter)
    3. Type "create circle"
    4. Wait for manifestation and capture screenshot
    """

    # Updated URL to point to the mounted static file
    TARGET_URL = "http://localhost:8000/static/index.html"
    OUTPUT_DIR = "verification"

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    async with async_playwright() as p:
        print(f"[*] Launching Browser for Verification...")
        browser = await p.chromium.launch(headless=True) # Headless for CI/Sandbox
        page = await browser.new_page()

        # 1. Navigate
        print(f"[*] Navigating to {TARGET_URL}")
        try:
            await page.goto(TARGET_URL, timeout=10000)
        except Exception as e:
            print(f"[!] Error connecting to server: {e}")
            await browser.close()
            return

        # Wait for Canvas
        await page.wait_for_selector("canvas", state="visible")
        print("[*] Canvas loaded.")

        # Capture Idle State
        await page.screenshot(path=f"{OUTPUT_DIR}/01_idle_state.png")
        print("[*] Captured Idle State.")

        # 2. Activate Input Layer (Ctrl+Enter)
        print("[*] Toggling Input Layer (Ctrl+Enter)...")
        await page.keyboard.press("Control+Enter")

        # 3. Input Command
        INPUT_SELECTOR = "#cmd-input"
        try:
            await page.wait_for_selector(INPUT_SELECTOR, state="visible", timeout=2000)
            print("[*] Input box visible.")

            print("[*] Inputting command: 'create circle'...")
            await page.fill(INPUT_SELECTOR, "create circle")
            await page.press(INPUT_SELECTOR, "Enter")

        except Exception as e:
            print(f"[!] Input UI not found or error: {e}")
            print("[*] Attempting direct WebSocket injection fallback...")
            # Fallback if UI interaction fails
            await page.evaluate("""
                if(app && app.ws && app.ws.readyState === 1) {
                    app.sendText("create circle");
                } else {
                    console.error('App/Socket not ready');
                }
            """)

        # 4. Wait for Manifestation
        print("[*] Waiting for manifestation (3s)...")
        await asyncio.sleep(3)

        # 5. Capture Result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{OUTPUT_DIR}/02_manifest_circle_{timestamp}.png"
        await page.screenshot(path=screenshot_path)
        print(f"[*] Verification Screenshot saved: {screenshot_path}")

        await browser.close()
        print("[*] Verification Complete.")

if __name__ == "__main__":
    asyncio.run(verify_logenesis_integration())
