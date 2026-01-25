from playwright.sync_api import sync_playwright
import time

def verify_gunui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Load the page
        page.goto("http://localhost:8000/gunui/index.html")
        time.sleep(2) # Wait for canvas init

        # 2. Inject Visual Params (Vortex, Purple)
        page.evaluate("""
            handleAetherMessage({
                type: 'VISUAL_PARAMS',
                params: {
                    base_shape: 'vortex',
                    color_palette: '#FF00FF',
                    turbulence: 0.5
                }
            })
        """)

        time.sleep(2) # Wait for particles to morph

        # 3. Screenshot
        page.screenshot(path="verification/gunui_vortex.png")
        browser.close()

if __name__ == "__main__":
    verify_gunui()
