import requests
import os
import argparse
from bs4 import BeautifulSoup
import builtwith
import socket

print("""
#                 ______                    _____                                 ______
#  ___      _________  /_     ____  ___________(_)__   __________________________ ___  /
#  __ | /| / /  _ \_  __ \    _  / / /_  __ \_  /__ | / /  _ \_  ___/_  ___/  __ `/_  / 
#  __ |/ |/ //  __/  /_/ /    / /_/ /_  / / /  / __ |/ //  __/  /   _(__  )/ /_/ /_  /  
#  ____/|__/ \___//_.___/     \__,_/ /_/ /_//_/  _____/ \___//_/    /____/ \__,_/ /_/   
#                                                                                       
    """)
# Function to print text in green color
def print_green(text):
    print("\033[92m" + text + "\033[0m")

# Function to print text in red color
def print_red(text):
    print("\033[91m" + text + "\033[0m")

# Function to print text in cyan color
def print_cyan(text):
    print("\033[96m" + text + "\033[0m")

def scrape_website(url):
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and extract information from the webpage using Beautiful Soup's functions.
        # For example, let's say you want to find all the links on the page:
        links = soup.find_all('a')

        link_list = [link.get('href') for link in links]

        return link_list

    else:
        return []

def check_website_files(url):
    # Define a list of file names to check
    files_to_check = ['robots.txt', 'sitemap.xml', '.DS_Store']

    # Initialize an empty list to store the results
    results = []

    for file_name in files_to_check:
        file_url = f"{url}/{file_name}"
        response = requests.head(file_url)
        if response.status_code == 200:
            results.append(f"Found: {file_name}")
        else:
            results.append(f"Not Found: {file_name}")

    return results

def check_search_engine_cache(url):
    # Construct the Google cache URL
    google_cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"

    # Send an HTTP GET request to the Google cache URL
    response = requests.get(google_cache_url)

    # Check if the request was successful
    if response.status_code == 200:
        return f"Google Cache: {google_cache_url}"
    else:
        return "Google Cache not found"

def identify_technologies(url):
    try:
        technologies = builtwith.builtwith(url)

        if technologies:
            return technologies
        else:
            return "No specific technologies identified."

    except Exception as e:
        return f"Error: {e}"

# Function to check commonly used application and administrative URLs
def check_common_urls(url):
    try:
        common_urls = [
            "/admin",
            "/admin/login",
            "/login",
            "/dashboard",
            "/wp-admin",
            "/login.php",
            "/wp-login.php",
            "/admin.php",
            "/user",
            "/cpanel",
            "/phpmyadmin",
        ]

        results = []

        for common_url in common_urls:
            full_url = f"{url}{common_url}"
            response = requests.head(full_url, allow_redirects=True)  # Follow redirects
            if response.status_code == 200:
                results.append(f"Found: {full_url}")
            else:
                results.append(f"Not Found: {full_url}")

        return results

    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Web Scraping, URL Checks, and Technology Identification")
    parser.add_argument("url", help="The URL of the website to check and scrape")

    args = parser.parse_args()

    website_links = scrape_website(args.url)
    file_check_results = check_website_files(args.url)
    google_cache_result = check_search_engine_cache(args.url)
    technology_info = identify_technologies(args.url)

    if website_links is not None:
        print_cyan("Links found on the website:")
        for link in website_links:
            if link is not None:
                print(link)
    else:
        print_red("Failed to retrieve the web page. Please check the URL and try again.")

    print_cyan("File Check Results:")
    for result in file_check_results:
        if "Not Found" in result:
            print_red(result)
        else:
            print(result)

    print_green("Google Cache Result:")
    print(google_cache_result)

    print_cyan("Identified Technologies:")
    print(technology_info)

    # Display the results of the check_common_urls function
    common_url_results = check_common_urls(args.url)
    if common_url_results:
        print_cyan("Commonly used application and administrative URLs:")
        for result in common_url_results:
            print(result)

if __name__ == "__main__":
    main()
