import requests
from bs4 import BeautifulSoup

def search_danbooru(tag):
    # Danbooru URL for searching images with the given tag
    url = f"https://danbooru.donmai.us/posts?tags={tag}"

    # Send an HTTP GET request
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find image links on the page
        image_links = [a['href'] for a in soup.find_all('a', class_='directlink')]

        return image_links
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return []

if __name__ == "__main__":
    # Get user input for the tag
    user_input = input("Enter the tag for image search on Danbooru: ")

    # Search Danbooru and get image links
    result = search_danbooru(user_input)

    # Output the resulting links
    if result:
        print("Resulting links:")
        for link in result:
            print(link)
    else:
        print("No results found.")
