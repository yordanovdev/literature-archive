"""
Web scraping functionality for literature content
"""
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time


class WebScraper:
    """Handles web scraping for literature content"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }
    
    def scrape(self, link):
        """
        Scrape content from a link with error handling.
        
        Args:
            link: URL to scrape
            
        Returns:
            Scraped text content or empty string if failed
        """
        try:
            text = self._scrape_with_playwright(link)
            return text if text else ""
        except Exception as e:
            print(f"     ⚠️  Failed to scrape (continuing anyway): {str(e)[:100]}")
            return ""
    
    def _scrape_with_requests(self, link):
        """
        Try scraping with requests first (faster for static pages).
        
        Args:
            link: URL to scrape
            
        Returns:
            Scraped text content or None if failed
        """
        try:
            response = requests.get(link, timeout=10, headers=self.headers)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator="\n")
            clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

            return clean_text

        except requests.RequestException as e:
            print(f"Requests failed for {link}: {e}")
            return None

    def _scrape_with_playwright(self, link):
        """
        Scrape using Playwright for client-side rendered content.
        
        Args:
            link: URL to scrape
            
        Returns:
            Scraped text content or None if failed
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Set a shorter timeout and try multiple times if needed
                try:
                    # Navigate to the page with reduced timeout
                    page.goto(link, wait_until="domcontentloaded", timeout=15000)
                    
                    # Wait a bit for JavaScript to execute
                    time.sleep(1)
                except Exception as goto_error:
                    print(f"     ⚠️  Navigation timeout/error: {str(goto_error)[:80]}")
                    browser.close()
                    return None
                
                # Get the full page content after JavaScript execution
                content = page.content()
                
                browser.close()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text(separator="\n")
                clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
                
                return clean_text
                
        except Exception as e:
            print(f"Playwright failed for {link}: {e}")
            return None
