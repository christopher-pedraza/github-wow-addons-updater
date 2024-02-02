import configparser
import requests
import shutil
import os
import time

os.system("color")

# Colors from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\x1b[1;32;40m"
NORMAL = "\033[0m"
RED = "\033[91m"
TITLE = "\x1b[6;36;40m"
YELLOW = "\033[33m"


def clear(doDelay=False):
    time.sleep(5) if doDelay else None
    os.system("cls" if os.name == "nt" else "clear")
    # Elite Font from https://patorjk.com/software/taag/
    print(
        f"""{TITLE}
    ▄▄▄· ·▄▄▄▄  ·▄▄▄▄         ▐ ▄     ▄• ▄▌ ▄▄▄··▄▄▄▄   ▄▄▄· ▄▄▄▄▄▄▄▄ .▄▄▄  
    ▐█ ▀█ ██▪ ██ ██▪ ██ ▪     •█▌▐█    █▪██▌▐█ ▄███▪ ██ ▐█ ▀█ •██  ▀▄.▀·▀▄ █·
    ▄█▀▀█ ▐█· ▐█▌▐█· ▐█▌ ▄█▀▄ ▐█▐▐▌    █▌▐█▌ ██▀·▐█· ▐█▌▄█▀▀█  ▐█.▪▐▀▀▪▄▐▀▀▄ 
    ▐█ ▪▐▌██. ██ ██. ██ ▐█▌.▐▌██▐█▌    ▐█▄█▌▐█▪·•██. ██ ▐█ ▪▐▌ ▐█▌·▐█▄▄▌▐█•█▌
    ▀  ▀ ▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪▀▀ █▪     ▀▀▀ .▀   ▀▀▀▀▀•  ▀  ▀  ▀▀▀  ▀▀▀ .▀  ▀
    {NORMAL}\n"""
    )


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
        source_values["source_id"] = f"SOURCE_{n}"
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


def updateSourceVersion(source_data, new_version):
    config.set(source_data["source_id"], "current_version", new_version)
    # Writing our configuration file to 'example.ini'
    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def getReleaseAssets(source_data):
    # Get the source URL
    url = source_data["source_url"]
    # Replace the GitHub URL with the API URL and append the endpoint for the latest release
    url = (
        url.replace("https://github.com/", "https://api.github.com/repos/")
        + "/releases/latest"
    )

    try:
        data = requests.get(url).json()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(
            f"\n\n{RED}Failed to get the latest release for {source_data['source_url']}. Reason:\n{e}{NORMAL}"
        )
        return []

    updateSourceVersion(source_data, data["tag_name"])
    if data["tag_name"] == source_data["current_version"]:
        ans = input(
            f"{YELLOW}\nLatest release already downloaded for {source_data['source_url']}. Do you still want to download it? (y/n) {NORMAL}"
        )
        if ans == "n":
            return []

    # Make a GET request to the URL and get the assets from the response JSON
    return data["assets"]


def getCategoriesNames(categories, source_data):
    # Initialize a list to hold the category names
    categories_names = {}
    for value in source_data:
        for category in categories:
            # If the category is in the value, add the source data value to the category names
            if category.lower() in value.lower():
                categories_names[category.lower()] = source_data[value].lower()
    return categories_names


def copyFile(fileName, destination):
    print("Copying '" + fileName + "'", end=" ... ")

    # Check if the directory exists, if not, don't copy the file
    if os.path.isdir(destination):
        # Copy the file to the destination
        shutil.copy2(f"downloads/{fileName}", destination)
        print(f"{GREEN}FINISHED{NORMAL}")
    else:
        print(f"{RED}FAILED{NORMAL}")
        print(
            f"{RED}Directory '{destination}' doesn't exist, couldn't copy '{fileName}'.{NORMAL}"
        )


def downloadReleaseAssets(setup_values, assets, categories_names, doCopy):
    for asset in assets:
        for category in categories_names:
            # If the category is in the asset name, set the flag to download the asset
            if categories_names[category] in asset["name"].lower():
                # Print the name of the file being downloaded
                print("\nDownloading '" + asset["name"] + "'", end=" .")
                # Make a GET request to the asset download URL
                file_dir = requests.get(asset["browser_download_url"])
                print(".", end="")
                # Write the content of the response to a file
                open("downloads/" + asset["name"], "wb").write(file_dir.content)
                print(". ", end="")
                print(f"{GREEN}FINISHED{NORMAL}")
                copyFile(
                    asset["name"], setup_values[category + "_dir"]
                ) if doCopy else None


def getReleases(setup_values, sources_values, categories, doCopy):
    os.mkdir("downloads") if not os.path.exists("downloads") else None
    for source_data in sources_values:
        # Get the release assets for the source
        assets = getReleaseAssets(source_data)
        # Get the category names for the source
        categories_names = getCategoriesNames(categories, source_data)
        # Download the release assets
        downloadReleaseAssets(setup_values, assets, categories_names, doCopy)


def cleanDownloads():
    for filename in os.listdir("downloads"):
        file_path = os.path.join("downloads", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


# Initialize a config parser
config = configparser.ConfigParser()
# Read the configuration from a file
# Handle errors in case a section is repeated
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


# Get the setup values from the config
setup_values = getSetup()
# Get the categories from the setup values
categories = getCategories(setup_values)
# Get the sources from the setup values
sources_values = getSources(setup_values)

exit_value = ""
while exit_value != "0":
    clear()
    print("1. Update Addons")
    print("2. Download Latest Addons")
    print("0. Exit")
    exit_value = input("\nOption: ")
    clear()

    if exit_value == "1":
        getReleases(setup_values, sources_values, categories, doCopy=True)
        cleanDownloads() if setup_values[
            "auto_delete_downloads"
        ].lower() == "true" or input(
            "\n\nDo you want to clean the downloads folder? (y/n) "
        ) == "y" else None
    elif exit_value == "2":
        getReleases(setup_values, sources_values, categories, doCopy=False)

    input(
        "\n=================================================================================\n\nPress Enter to return to the menu..."
    ) if exit_value != "0" else None
