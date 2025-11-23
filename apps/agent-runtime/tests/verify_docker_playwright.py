from playwright.sync_api import sync_playwright
import os

def verify_playwright():
    print("Starting Playwright verification...")
    os.makedirs("screenshots", exist_ok=True)
    
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Navigating to example.com...")
        page.goto("http://example.com")
        
        print("Taking screenshot...")
        page.screenshot(path="screenshots/docker_proof.png")
        
        browser.close()
        print("Verification complete. Screenshot saved to screenshots/docker_proof.png")

if __name__ == "__main__":
    verify_playwright()
