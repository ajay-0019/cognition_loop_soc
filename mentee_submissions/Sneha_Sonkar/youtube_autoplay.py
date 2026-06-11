from playwright.sync_api import sync_playwright

def play_youtube_video():
    # Take the search query directly from the terminal prompt
    query = input("What video would you like to search and play on YouTube? ")
    if not query.strip():
        print("Search query cannot be empty. Exiting.")
        return

    with sync_playwright() as p:
        print("\nLaunching browser...")
        # launch with a slow_mo delay so you can visibly watch the actions happen step-by-step
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        # Create a browser context that matches your screen dimensions
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        print("Navigating to YouTube...")
        page.goto("https://www.youtube.com")
        
        # 1. Handle the Search Bar
        print(f"Searching for: '{query}'...")
        # YouTube's search input tag is named 'search_query'
        search_box = page.locator("input[name='search_query']")
        search_box.wait_for(state="visible")
        
        search_box.fill(query)  # Types the query into the input box
        search_box.press("Enter")  # Simulates hitting the physical Enter key
        
        # 2. Wait for Video Results to Load
        print("Waiting for search results to render...")
        # YouTube video links on the search page use the ID '#video-title'
        first_video = page.locator("#video-title").first
        first_video.wait_for(state="visible", timeout=10000)
        
        video_title = first_video.inner_text()
        print(f"Found video: '{video_title}'! Clicking to play...")
        
        # 3. Click the Video to Play it
        first_video.click()
        print("Video is now loading. Enjoy your watch!\n")
        
        # 4. Challenge Extra: Smart Ad-Skipper Loop
        print("Monitoring for skippable ads... (Press Ctrl+C in terminal to stop early)")
        try:
            # Let the video run for up to 45 seconds while checking for ads every second
            for second in range(45):
                page.wait_for_timeout(1000) # Wait 1 second
                
                # Look for YouTube's native 'Skip Ad' button classes
                skip_button = page.locator(".ytp-skip-ad-button, .ytp-ad-skip-button")
                
                if skip_button.is_visible():
                    print(f"[{second}s] Ad detected! Clicking 'Skip Ad' button automatically...")
                    skip_button.click()
                    break # Exit the monitoring loop once the ad is skipped
                    
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
        except Exception as e:
            print(f"Ad monitoring notice: {e}")

        # Final pause so the browser doesn't snap closed immediately
        print("\nKeeping video playback alive for 15 more seconds...")
        page.wait_for_timeout(15000)
        
        print("Closing automated browser session.")
        browser.close()

if __name__ == "__main__":
    play_youtube_video()