import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def fetch_github_trending():
    # URL of the GitHub trending page
    url = "https://github.com/trending"

    # Send a GET request to the URL
    response = requests.get(url)

    # Initialize an empty list to store repository data
    repo_data = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements that contain repository information
        repos = soup.find_all('article', class_='Box-row')

        # Extracting relevant data for each repository
        for repo in repos:
            # Extract repository details
            name_section = repo.find('h2', class_='h3 lh-condensed').a
            name_text = ' '.join(name_section.get_text(strip=True).split())
            repo_url = "https://github.com" + name_section['href']

            language_section = repo.find(
                'span', itemprop='programmingLanguage')
            language = language_section.get_text(
                strip=True) if language_section else 'Unknown'

            stars_section = repo.find(
                'a', href=lambda href: href and '/stargazers' in href)
            stars = stars_section.get_text(strip=True).replace(
                ',', '') if stars_section else '0'

            forks_section = repo.find(
                'a', href=lambda href: href and '/forks' in href)
            forks = forks_section.get_text(strip=True).replace(
                ',', '') if forks_section else '0'

            description_section = repo.find('p', class_='col-9')
            description = description_section.get_text(
                strip=True) if description_section else 'No description'

            # Append repository data to the list
            repo_data.append({
                'name': name_text,
                'url': repo_url,
                'stars': stars,
                'language': language,
                'forks': forks,
                'description': description
            })

    else:
        print("Failed to retrieve data from GitHub Trending page.")
        return None

    return repo_data

def save_to_markdown(data):
    # Create a folder named "Daily" if it doesn't exist
    if not os.path.exists('Daily'):
        os.makedirs('Daily')

    # Generate the filename with the current date
    file_name = datetime.now().strftime("%Y-%m-%d") + ".md"

    # Specify the path to save the file in the "Daily" folder
    file_path = os.path.join('Daily', file_name)

    # Markdown content
    markdown_content = "# All Languages\n\nRepo|Star|Language|Fork|Intro\n-|-|-|-|-\n"
    for repo in data:
        markdown_content += f"[{repo['name']}]({repo['url']})|{repo['stars']}|{repo['language']}|{repo['forks']}|{repo['description']}\n"

    # Write to the markdown file in the "Daily" folder
    with open(file_path, 'w') as file:
        file.write(markdown_content)
    print(f"Markdown file saved as {file_path}")

def save_to_json(data):
    # Create a folder named "Daily" if it doesn't exist
    if not os.path.exists('Daily'):
        os.makedirs('Daily')

    # Generate the filename with the current date
    file_name = datetime.now().strftime("%Y-%m-%d") + ".json"

    # Specify the path to save the file in the "Daily" folder
    file_path = os.path.join('Daily', file_name)

    # Write to the JSON file in the "Daily" folder
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file saved as {file_path}")

if __name__ == '__main__':
    trending_data = fetch_github_trending()
    if trending_data is not None:
        save_to_markdown(trending_data)
        save_to_json(trending_data)
