import configparser
import requests

# Initialize a config parser
config = configparser.RawConfigParser()
# Read the configuration from a file
config.read("config.cfg")


def getSetup():
    # Read the config file and get the setup values
    setup_values = dict(config.items("SETUP"))
    return setup_values


def getSources(setup_values):
    # Get the number of sources from the setup values
    number_sources = int(setup_values["number_sources"])

    # Create a list of sources
    sources = []
    for n in range(1, number_sources + 1):
        # Get the source values from the config
        source_values = dict(config.items(f"SOURCE_{n}"))
        # Add the source to the list of sources
        sources.append(source_values)

    return sources


def getCategories(setup_values):
    # Initialize a list to hold the categories
    categories = []
    for value in setup_values:
        # If the value ends with "_dir", it's a category
        if value.endswith("_dir"):
            # Add the category to the list, removing the "_dir" part
            categories.append(value[:-4])
    return categories


def getReleaseAssets(source_data):
    # Get the source URL
    url = source_data["source_url"]
    # Replace the GitHub URL with the API URL and append the endpoint for the latest release
    url = (
        url.replace("https://github.com/", "https://api.github.com/repos/")
        + "/releases/latest"
    )
    # Make a GET request to the URL and get the assets from the response JSON
    assets = requests.get(url).json()["assets"]
    return assets


def getCategoriesNames(categories, source_data):
    # Initialize a list to hold the category names
    categories_names = []
    for value in source_data:
        for category in categories:
            # If the category is in the value, add the source data value to the category names
            if category in value:
                categories_names.append(source_data[value])
    return categories_names


def downloadReleaseAssets(assets, categories_names):
    for asset in assets:
        # Initialize a flag to determine whether to download the asset
        should_download = False
        for category in categories_names:
            # If the category is in the asset name, set the flag to download the asset
            if category in asset["name"]:
                should_download = True
                break

        if should_download:
            # Print the name of the file being downloaded
            print("Downloading '" + asset["name"] + "'", end=" .")
            # Make a GET request to the asset download URL
            file_dir = requests.get(asset["browser_download_url"])
            print(".", end="")
            # Write the content of the response to a file
            open(asset["name"], "wb").write(file_dir.content)
            print(". ", end="")
            print("Finished.")


def getReleases(sources_values, categories):
    for source_data in sources_values:
        # Get the release assets for the source
        assets = getReleaseAssets(source_data)
        # Get the category names for the source
        categories_names = getCategoriesNames(categories, source_data)
        # Download the release assets
        downloadReleaseAssets(assets, categories_names)


# Get the setup values from the config
setup_values = getSetup()
# Get the categories from the setup values
categories = getCategories(setup_values)
# Get the sources from the setup values
sources_values = getSources(setup_values)
# Get the releases for the sources
getReleases(sources_values, categories)
