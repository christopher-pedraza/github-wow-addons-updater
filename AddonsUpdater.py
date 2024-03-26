VERSION = "2.0"

# configparser is used for handling configuration files
import configparser

# requests is used for making HTTP requests
import requests

# shutil and os are used for file and directory operations
import shutil
import os

# So colors are shown in the console
os.system("color")

# Colors used in the print statements
# Colors from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\x1b[1;32;40m"
NORMAL = "\033[0m"
RED = "\033[91m"
TITLE = "\x1b[6;36;40m"
YELLOW = "\033[33m"


def clear():
    # Clear the console. The command depends on the operating system
    os.system("cls" if os.name == "nt" else "clear")
    # "Elite" Font from https://patorjk.com/software/taag/
    print(
        f"""{TITLE}
    ▄▄▄· ·▄▄▄▄  ·▄▄▄▄         ▐ ▄     ▄• ▄▌ ▄▄▄··▄▄▄▄   ▄▄▄· ▄▄▄▄▄▄▄▄ .▄▄▄  
    ▐█ ▀█ ██▪ ██ ██▪ ██ ▪     •█▌▐█    █▪██▌▐█ ▄███▪ ██ ▐█ ▀█ •██  ▀▄.▀·▀▄ █·
    ▄█▀▀█ ▐█· ▐█▌▐█· ▐█▌ ▄█▀▄ ▐█▐▐▌    █▌▐█▌ ██▀·▐█· ▐█▌▄█▀▀█  ▐█.▪▐▀▀▪▄▐▀▀▄ 
    ▐█ ▪▐▌██. ██ ██. ██ ▐█▌.▐▌██▐█▌    ▐█▄█▌▐█▪·•██. ██ ▐█ ▪▐▌ ▐█▌·▐█▄▄▌▐█•█▌
    ▀  ▀ ▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪▀▀ █▪     ▀▀▀ .▀   ▀▀▀▀▀•  ▀  ▀  ▀▀▀  ▀▀▀ .▀  ▀
    {NORMAL}\n"""
    )


# Get the setup values from the config file
def getSetup():
    # Read the config file and get the setup values
    setup_values = dict(config.items("SETUP"))
    return setup_values


# Get the sources' data from the setup values
def getSources(setup_values):
    # Get the number of sources from the setup values
    number_sources = int(setup_values.get("number_sources", 0))
    if number_sources == 0:
        print(
            f"{RED}\nError: The config file is missing the number of sources. Please fix it and try again.{NORMAL}"
        )
        exit(1)

    # Create a list of sources
    sources = []
    for n in range(1, number_sources + 1):
        # Check if the section for the source exists
        if config.has_section(f"SOURCE_{n}") == False:
            print(
                f"{RED}\nError: The config file is missing a section for SOURCE_{n}. Please fix it and try again.{NORMAL}"
            )
            exit(1)
        # Get the source values from the config
        source_values = dict(config.items(f"SOURCE_{n}"))
        # Add the source ID to the source values
        source_values["source_id"] = f"SOURCE_{n}"
        # Add the source to the list of sources
        sources.append(source_values)

    return sources


# Get the categories from the setup values
def getCategories(setup_values):
    categories_str = setup_values.get("categories", "")
    # Remove the spaces of the string and then split it by the comma into a list
    categories = (
        categories_str.replace(" ", "")
        .lower()
        .split(setup_values.get("separator", ","))
    )

    return categories


# Update the current version of the source in the config file
def updateSourceVersion(source_data, new_version):
    # Update the current version in the config file
    config.set(source_data["source_id"], "current_version", new_version)
    # Writing our configuration file
    with open("config.cfg", "w") as configfile:
        config.write(configfile)


# Copy a file to a destination directory
def copyFile(fileName, destination, category):
    print(
        f"Copying '{BLUE}{fileName}{NORMAL}' to '{BLUE}{category}{NORMAL}' directory",
        end=" ... ",
    )

    # Check if the directory exists, if not, don't copy the file
    if os.path.isdir(destination):
        # Copy the file to the destination
        shutil.copy2(f"downloads/{fileName}", destination)
        print(f"{GREEN}COMPLETE{NORMAL}")
    else:
        print(f"{RED}FAILED{NORMAL}")
        print(
            f"{RED}Directory '{destination}' doesn't exist, couldn't copy '{fileName}'.{NORMAL}"
        )


# Open the directories where the assets were copied
# If the auto_open_directories setup value is set to true, open the directories specified in the directories_to_auto_open setup value
# without asking the user
# Otherwise, ask the user which directory they want to open
def openDirectories(setup_values, categories, silent=False):
    if setup_values.get("auto_open_directories", "false").lower() == "true" and silent:
        # Get the directories to auto open from the setup values, remove spaces, convert to lowercase, and split into a list
        directories = (
            setup_values.get("directories_to_auto_open", "")
            .replace(" ", "")
            .lower()
            .split(setup_values.get("separator", ","))
        )
        # If the list contains an empty string, replace it with the list of categories and append "downloads"
        # An empty list means we should open all directories
        if "" in directories:
            directories = [category for category in categories]
            directories.append("downloads")
        # Iterate over each directory
        for directory in directories:
            # If the directory is "downloads", open it
            if directory == "downloads":
                os.startfile("downloads")
            # Otherwise, get the directory from the setup values and open it if it's not an empty string
            else:
                dir = setup_values.get(directory + "_dir", "")
                os.startfile(dir) if dir != "" else None

    elif not silent:
        # Initialize an empty list to store directories
        dirs = []
        # Print the first option and append the corresponding directory to the list
        print("1) Downloads")
        dirs.append("downloads")
        # Initialize a counter for the options
        i = 2
        # Iterate over each category
        for category in categories:
            # Print the option and append the corresponding directory to the list
            print(f"{i}) {category.capitalize()}")
            dirs.append(setup_values.get(category + "_dir", ""))
            # Increment the counter
            i += 1
        # Print the last two options
        print(f"{i}) All")
        print(f"0) Return to the menu")

        # Ask the user for their choice
        option = input("\nDirectory to open: ")

        # If the user chose to return to the menu, exit the function
        if option == "0":
            return
        # If the user chose to open all directories, iterate over each directory and open it
        elif option == str(i):
            for dir in dirs:
                os.startfile(dir) if dir != "" else None
        # If the user chose a specific directory, open it
        else:
            dir = dirs[int(option) - 1]
            os.startfile(dir) if dir != "" else None


# Open the downloads directory if the auto_open_directories setup value is set to true
def openDownloads(setup_values):
    if setup_values.get("auto_open_directories", "false").lower() == "true":
        os.startfile("downloads")


# Check for updates to the program
def checkForUpdates():
    url = "https://api.github.com/repos/christopher-pedraza/github-wow-addons-updater/releases/latest"

    # Try to make a GET request to the URL
    try:
        # Parse the response as JSON
        data = requests.get(url).json()
    # If a RequestException is raised, print an error message and return an empty list
    except requests.exceptions.RequestException as e:
        print(f"\n\n{RED}Failed to check for updates. Reason:\n{e}{NORMAL}")
        return

    if data.get("message", "") != "Not Found":
        # Get the latest version from the response
        latest_version = data["tag_name"]

        # If the latest version is different from the current version, print a message
        if latest_version != VERSION:
            print(
                f"\n{YELLOW}A new version is available. Current version: {VERSION}. Latest version: {latest_version}.{NORMAL}"
            )
            # Ask the user if they want to download the latest version
            ans = input(f"\nDo you want to download the latest version? (y/n) ")
            # If the user answers "y", download the latest version
            if ans == "y":
                print("\nDownloading the latest version...", end=" ")
                # Make a GET request to the latest release URL
                file_dir = requests.get(data["assets"][0]["browser_download_url"])
                # Write the content of the response to a file
                open(f"AddonsUpdater_{latest_version}.zip", "wb").write(
                    file_dir.content
                )
                print(f"{GREEN}COMPLETE{NORMAL}")
                # Print a message asking the user to replace the current version with the latest version
                print(
                    f"\nReplace the current version of AddonsUpdater with the latest version ({BLUE}{latest_version}{NORMAL}) and run it again."
                )
                # Wait for the user to press Enter
                input("\nPress Enter to exit...")
                # Exit the program
                exit(0)


# Get the assets (JSON data with the name of the files in the assets of a release as well as the link to download them)
# from the latest release of a source
def getReleaseAssets(setup_values, source_data):
    # Get the source URL
    url = source_data.get("source_url", "")
    # If the URL is empty, print an error message and return an empty list
    if url == "":
        print(
            f"{RED}\nError: The source URL for the source {source_data['source_id']} is empty.{NORMAL}"
        )
        return []
    # Replace the GitHub URL with the API URL and append the endpoint for the latest release
    url = (
        url.replace("https://github.com/", "https://api.github.com/repos/")
        + "/releases/latest"
    )

    # Try to make a GET request to the URL
    try:
        # Parse the response as JSON
        data = requests.get(url).json()
    # If a RequestException is raised, print an error message and return an empty list
    except requests.exceptions.RequestException as e:
        print(
            f"\n\n{RED}Failed to get the latest release for {source_data['source_url']}. Reason:\n{e}{NORMAL}"
        )
        return []

    # Update the current version of the source in the config file
    updateSourceVersion(source_data, data["tag_name"])

    # If the latest version is the same as the current version, ask the user if they still want to download it
    if (
        data["tag_name"] == source_data.get("current_version", "")
        and not setup_values.get("skip_confirmations", "false").lower() == "true"
    ):
        ans = input(
            f"{YELLOW}\nLatest release already downloaded for {source_data['source_url'].replace('https://github.com/','')}."
            + f"\nDo you still want to download it? (y/n) {NORMAL}"
        )
        # If the user answers "n", return an empty list
        if ans == "n":
            return []

    # Return the assets from the latest release
    # From the dictionary just return the values inside the key "name" and "browser_download_url" which are the name
    # of the file and the link to download it
    assets = []
    for asset in data["assets"]:
        assets.append(
            {
                "name": asset["name"],
                "browser_download_url": asset["browser_download_url"],
            }
        )
    return assets


# Get the ids associated with the categories (fragment of the name of the files that will let the program
# identify to which directory it should be copied) of the source
def getCategoriesIDs(categories, source_data, setup_values):
    categories_ids = {}

    for category in categories:
        category = category.lower()
        category_ids = category + "_id"
        # The source may not have an id for a category, in this case, the source doesn't have any
        # files that will be copied to the directory associated to the category
        if category_ids in source_data:
            categories_ids[category] = (
                source_data[category_ids]
                .replace(" ", "")
                .lower()
                .split(setup_values.get("separator", ","))
            )
    return categories_ids


# Download the release assets in case the file hasn't been downloaded yet
def downloadReleaseAssets(assets, categories_names, assets_ref, downloaded_assets):
    # Store in a set to prevent downloading the same file twice
    categories_ids = set(
        (category, id) for category, ids in categories_names.items() for id in ids
    )
    for asset in assets:
        for category, id in categories_ids:
            # Check whether the file has already been downloaded and if the id is in the name of the file
            if id in asset["name"].lower():
                # Add the asset to the reference
                assets_ref.add((asset["name"], category))
                # If the asset has already been downloaded, skip it
                if asset["name"] in downloaded_assets:
                    continue
                # Print the name of the file being downloaded
                print(f"\nDownloading '{BLUE}{asset['name']}{NORMAL}'", end=" .")
                # Make a GET request to the asset download URL
                file_dir = requests.get(asset["browser_download_url"])
                print(".", end="")
                # Write the content of the response to a file
                open("downloads/" + asset["name"], "wb").write(file_dir.content)
                print(". ", end="")
                print(f"{GREEN}COMPLETE{NORMAL}")
                downloaded_assets.add(asset["name"])


# Gets the route to the directories stated in the setup section and links it to the category it belongs to
def getDirectories(setup_values, categories):
    directories = {}
    for category in categories:
        if category + "_dir" in setup_values:
            directories[category] = setup_values.get(category + "_dir")
    return directories


def downloadAssets(
    assets_ref, downloaded_assets, setup_values, categories, sources_values
):
    print(
        f"""\n\n\t\t\t{CYAN}                    
\t\t\t\t========================
\t\t\t\t   DOWNLOADING ADDONS
\t\t\t\t========================
{NORMAL}\n\n"""
    )
    for source_data in sources_values:
        # Get the ids associated with the categories (fragment of the name of the files that will
        # let the program identify to which directory it should be copied)
        categories_ids = getCategoriesIDs(categories, source_data, setup_values)
        # Get the release assets for the source
        assets = getReleaseAssets(setup_values, source_data)
        # Download the release assets
        downloadReleaseAssets(assets, categories_ids, assets_ref, downloaded_assets)


def copyAssets(assets_ref, directories):
    print(
        f"""\n\n\t\t\t{CYAN}                    
\t\t\t\t========================
\t\t\t\t   COPYING TO FOLDERS
\t\t\t\t========================
{NORMAL}\n\n"""
    )

    for asset, category in assets_ref:
        if category in directories:
            copyFile(asset, directories.get(category), category)


def init():
    clear()
    checkForUpdates()

    # Get the setup values from the config
    setup_values = getSetup()
    # Get the categories from the setup values
    categories = getCategories(setup_values)
    # Get the sources from the setup values
    sources_values = getSources(setup_values)
    # Get the directories where the assets should be copied
    directories = getDirectories(setup_values, categories)

    exit_value = ""
    while exit_value != "0":
        clear()
        print("1. Update Addons")
        print("2. Download Latest Addons")
        print("3. Open directories")
        print("0. Exit")
        exit_value = input("\nOption: ")
        clear()

        assets_ref = set()
        downloaded_assets = set()

        if exit_value == "1":
            downloadAssets(
                assets_ref, downloaded_assets, setup_values, categories, sources_values
            )
            copyAssets(assets_ref, directories)
            openDirectories(setup_values, categories, silent=True)
        elif exit_value == "2":
            downloadAssets(
                assets_ref, downloaded_assets, setup_values, categories, sources_values
            )
            openDownloads(setup_values)
        elif exit_value == "3":
            openDirectories(setup_values, categories, silent=False)

        (
            input(
                "\n================================================================================="
                + "\n\nPress Enter to return to the menu..."
            )
            if exit_value != "0" and exit_value != "3"
            else None
        )


# Initialize a config parser
config = configparser.ConfigParser()
# Read the configuration from a file and handle any errors
try:
    config.read("config.cfg")
except configparser.DuplicateSectionError as dse:
    print(
        f"{RED}\nError: The config file has a repeated section. Please fix it and try again. Error message:\n{dse}{NORMAL}"
    )
    exit(1)
except configparser.MissingSectionHeaderError as mshe:
    print(
        f"{RED}\nError: The config file is missing a section header. Please fix it and try again. Error message:\n{mshe}{NORMAL}"
    )
    exit(1)
except configparser.ParsingError as pe:
    print(
        f"{RED}\nError: The config file has a parsing error. Please fix it and try again. Error message:\n{pe}{NORMAL}"
    )
    exit(1)
except configparser.Error as e:
    print(
        f"{RED}\nError: The config file has an error. Please fix it and try again. Error message:\n{e}{NORMAL}"
    )
    exit(1)

init()
