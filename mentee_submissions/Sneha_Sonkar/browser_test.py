from playwright.sync_api import sync_playwright

def run_scraper():
    # 1. Start Playwright and launch a visible Chromium browser
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False) # headless=False lets us watch it open!
        page = browser.new_page()
        
        # 2. Navigate to Hacker News
        print("Navigating to Hacker News...")
        page.goto("https://news.ycombinator.com")
        
        # 3. Locate headline links using CSS Selectors
        # On Hacker News, every headline title is inside an <a> tag with class '.titleline'
        print("Extracting headlines...\n")
        headline_elements = page.locator(".titleline > a").all()
        
        # Store extracted data for later interaction
        headlines_data = []
        
        # 4. Loop through the extracted elements and display a numbered list
        for i, element in enumerate(headline_elements[:10], start=1): # Limit to top 10 for readability
            title = element.inner_text()
            link = element.get_attribute("href")
            headlines_data.append({"title": title, "link": link})
            print(f"{i}. {title}")
            
        print("\n" + "="*50 + "\n")
        
        # 5. Interactive Extra: Let the user choose a headline to open
        try:
            choice = input("Enter the number of a headline you want to open in the browser (or press Enter to exit): ")
            if choice.strip().isdigit():
                index = int(choice) - 1
                if 0 <= index < len(headlines_data):
                    selected = headlines_data[index]
                    print(f"\nOpening: {selected['title']}")
                    print(f"URL: {selected['link']}")
                    
                    # Navigate the open browser instance to the chosen link
                    page.goto(selected['link'])
                    
                    # Keep the browser open for 8 seconds so you can look at the article!
                    print("Keeping page open for 8 seconds...")
                    page.wait_for_timeout(8000)
                else:
                    print("Invalid choice number.")
            else:
                print("Exiting.")
        except Exception as e:
            print(f"An interaction error occurred: {e}")
            
        # 6. Clean up and close the browser sessions cleanly
        print("Closing browser...")
        browser.close()

if __name__ == "__main__":
    run_scraper()