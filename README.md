Icon from [max.icons in flaticon.com](https://www.flaticon.com/free-icon/fire_3426195)


The configuration file is composed of two types of sections: General Setup and Sources.

The General Setup section is titled "SETUP" and looks something like this:

```
[SETUP]
number_sources = 3
separator = ,
categories = asset1, asset2
asset1_dir = C:\dir\to\file\a1
asset2_dir = C:\dir\to\file\a2
skip_confirmations = FALSE
auto_open_directories = TRUE
directories_to_auto_open = downloads, asset1
```

Starting with the name of the section, the line "[SETUP]" should remain exactly as it is
as it's the section name and is used in the program to identify the values for the General
Setup.

The first of the values under the title is "number_sources". This value represents the 
number of sources and is directly related to the number of Sources sections below (more
on this later). For example, if you want to download addons from 3 sources, you should set
as the value "3" as it's in the example above.

Following that is the separator string that is going to be used to parse whenever we have
lists of values for attributes (categories, ids). You may specify any character that you
won't use for the list of values in the lists.

Then we have the categories attribute which lets you define the categories' names you will
later use. You may declare 1 or more categories, each one of them separated by the
separator you declared in the previous attrbute. Remember NOT to use the character you
defined as the separator in the names of the categories. Keep these names you have decided
in mind as they will be useful for the configuration of the directories where the assets 
will be stored and for identifying them from the sources.

The next lines contain the directories where the assets that are downloaded from the 
sources will be copied. The name of each variable follows the format: "{category}_dir".
It's important that this category name should be the same as the list in the "categories"
attribute, as well as the id in the sources, which will be discussed later. Basically, if
you have 3 places you want to store things, assign to each one a category name that will
be later used to know what files from the sources should go where. 

Then, there's the "skip_confirmations" attribute. This can take the values "TRUE" or
"FALSE", but it's not case sensitive. When "TRUE", in case the app detects that you already
have the newest version from a source, it won't ask for a confirmation to download it again
and instead will just proceed to downloading the assets. When "FALSE", every time the app
detects that you already have the newest version, it will ask for a confirmation to
download the files.

After that we have two attributes that lets you define whether you want to auto open
the directories you have defined, and which of them you would like to auto open. When
"auto_open_directories" is set to "TRUE", the directories of the categories defined in the
attribute "directories_to_auto_open" will open after downloading or updating the addons.
If no categories are defined in the attribute, or the attribute itself is not included,
but you have auto opening directories set to "TRUE", all directories defined in the SETUP
will auto open. In the case you also want to open the downloads directory after downloading
or updating, you may include it in "directories_to_auto_open" as if it's a category. 

Don't worry if the order of your attributes is not the same as the one in the example, 
as the order doesn't matter. Also, you may have as many directories as you want, not
just 2, the same goes for the number of sources. And lastly, the number of directories
doesn't need to be the same as the number of sources. You could have multiple sources
copying the content to a single directory, or even a single source copying to multiple
directories.

The next sections in the file correspond to all the sources from where you want to 
download content. The number of sections must be equal to the value in "number_sources",
or else, only the first sources up to the value you have given to the attribute will be
considered. If, for instance, you have 5 sections of sources following the SETUP, but
the value given to the attribute "number_sources" is of 2, only the sources "SOURCE_1"
and "SOURCE_2" will be considered. This could be useful in case you don't need a source
anymore, but would like to preserve the current configuration of it in case you need it
in the future, you may make that source your last one and reduce the value of the
attribute (more on this later). 

Each section is roughly structured like this:

```
[SOURCE_1]
source_url = https://github.com/{user}/{repo}
current_version = -1
retail_id = mainline, tbc
classic_id = vanilla
```

We first start once again with the name of the section. The name will ALWAYS start with
the word "SOURCE" followed by an underscore and an index from 1, up to the value of the
attribute "number_sources". If any of the sources from 1, up to the value doesn't exist,
the program won't start and will show you a message indicating the section that you are
missing. In case you don't need that section, just remove the ones that you don't need
reduce the value of "number_sources" to the number of sources you need, and numerate
the sections correctly (for example, for 2 sources, the two sections would be named
"SOURCE_1" and "SOURCE_2"). However, even if you cannot have less sections than the 
number specified by "number_sources", you could have a value lower than the sections
you declared if you don't want to include the last section anymore, but want to keep
the configuration in the file.

The following line contains the url of the source. This needs to be a valid link to a
github repository in the form "https://github.com/{user}/{repo}". Do not add anything
else to the link, as that will most likely break the program. 

Next is the "current_version", which indicates the last version that was donwloaded by
the program. You may ignore this attribute as it autogenerates in case it doesn't exist.
It is used so the program knows whether you already have the newest version available
or not. The first time you run the program it will automatically change the value so
you may leave it with a "-1" as a value, or completely ignore it and let the program
add it by itself.

Lastly are the id attributes. These let the program relate the assets downloaded from
the github repository's latest release with the categories you previously defined in
the SETUP section. The attributes' names should have the following structure: 
"{category_id}". The value of these attributes will be a part of the asset name that
belongs to the category. For example, if we have the files "file1_mainline.zip",
"file2_vanilla.zip" and "something.zip" and we want to target only the first of the
files, we could use as a value "mainline" as only that file contains that word. If, on
the other hand we want to target the first 2 files, we could use the value "file" as 
both of them contain that word, but the file 3 ("something.zip") doesn't contain it, so
it wouldn't be targeted. Also, it's possible to assign multiple ids for the same
attribute, this way, you could copy multiple assets in the same directory even if they
don't share any common word. Returning to the example of the 3 files, if we want to
target the first two files, we could have "mainline, vanilla". In this case, the
separator for the ids would be the same declared in the SETUP section. Also, the ids
aren't case sensitive and don't consider spaces (they will be ignored, so if you had
the id "The Category" it would be read as "thecategory").

In the following example we define two categories, three directories where some assets
will be copied, set the auto deletion of the downloads folder to FALSE, and define 2
sources from which we will download 2 files from the first one, and 1 from the last
one:

```
[SETUP]
number_sources = 2
separator = ,
categories = normal, naevys
normal_dir = D:\Folders\Desktop\normal
backup_dir = D:\Folders\Desktop\backup
naevys_dir = D:\Folders\Desktop\naevys
auto_delete_downloads = FALSE

[SOURCE_1]
source_url = https://github.com/Ludovicus-Maior/WoW-Pro-Guides
current_version = 20240122
normal_id = mainline, vanilla
backup_id = vanilla

[SOURCE_2]
source_url = https://github.com/christopher-pedraza/NAEVYS-updater
current_version = 3.0
naevys_id = naevys
```

In this example, the folder "normal/" will end up with the files having the words
"mainline" and "vanilla", the "backup/" folder with the file with the word "vanilla",
and the folder "naevys" with the file with the "naevys" word.
