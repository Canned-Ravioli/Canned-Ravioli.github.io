import praw

# Set up Reddit API credentials
reddit = praw.Reddit(client_id='ApEB_aSOx7ULJsLALc4iHA',
                     client_secret='Q2cxz1qS6un7SYMich6njin8t2F9wA',
                     user_agent='CoolScript/1.0 by PickledRavioli135',
                     check_for_async=False)  # Add this line to disable async checking

# Function to display and ask the user to choose a subreddit
def choose_subreddit(subreddits):
    if not subreddits:
        print("No subreddits found. Exiting.")
        return None

    print("Subreddits found:")
    for i, subreddit in enumerate(subreddits, 1):
        print(f"{i}. {subreddit.display_name}")

    while True:
        try:
            choice = int(input("Enter the number of the subreddit you want to get posts from: "))
            if 1 <= choice <= len(subreddits):
                return subreddits[choice - 1]
            else:
                print("Invalid choice. Please enter a number within the provided range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to ask the user for sorting method
def get_sorting_method():
    while True:
        sorting_method = input("Enter sorting method (hot, new, top, rising, controversial): ").lower()
        if sorting_method in ['hot', 'new', 'top', 'rising', 'controversial']:
            return sorting_method
        else:
            print("Invalid sorting method. Please enter hot, new, top, rising, or controversial.")

# Function to ask the user for the number of posts
def get_number_of_posts():
    while True:
        try:
            num_posts = int(input("Enter the number of posts to generate: "))
            if num_posts > 0:
                return num_posts
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

# Main loop
while True:
    search_query = input("Enter a search query: ")

    # Search for subreddits
    subreddits = list(reddit.subreddits.search(search_query, limit=35, params={'include_over_18': 'true'}))

    random_subreddit = choose_subreddit(subreddits)

    if not random_subreddit:
        break

    sorting_method = get_sorting_method()
    num_posts = get_number_of_posts()

    # Retrieve posts from the chosen subreddit
    posts = getattr(random_subreddit, sorting_method)(limit=num_posts)

    # Store media URLs in a list
    media_urls = []

    for post in posts:
        if post.media and post.media.get('type') == 'image':
            # For single images
            media_urls.append(post.url)
        elif post.media and post.media.get('type') == 'gallery':
            # For galleries
            try:
                gallery = post.media_metadata
                media_urls.extend(f"https://preview.redd.it/{item['id']}.{item['e']}" for item in gallery.values())
            except AttributeError:
                media_urls.append(post.url)
        elif post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            media_urls.append(post.url)
        elif hasattr(post, 'url_overridden_by_dest') and post.url_overridden_by_dest:
            media_urls.append(post.url_overridden_by_dest)
        elif post.url:
            media_urls.append(post.url)

    # Output the links in the desired format
    formatted_links = [f"[{link}]," for link in media_urls]

    # Display the formatted links
    print("Formatted links:")
    for formatted_link in formatted_links:
        print(formatted_link)

    user_input = input("Do you want to try another subreddit? (yes/no): ").lower()

    if user_input != 'yes':
        break
