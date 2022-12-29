# Tauri Webapp Creator

This is a simple python script that similarly to Nativefier creates a webapp given a url.
But instead of using Electron and therefore a resource hungry fully blown Chromium-instance it uses Tauri for a lightweight executable.

## Example Usage
```
./create-webapp.py "Youtube Music" https://music.youtube.com/
```

## Usage
```
usage: create-webapp.py [-h] [-c] [-f] [-w WORK_DIR] [-b BUILD_DIR] [--binary_only]
                        [--arch_install] [--deb_install]
                        name url

Create a lightweight tauri webapp.

positional arguments:
  name                  The name of the app that will be created
  url                   The url of the target site

options:
  -h, --help            show this help message and exit
  -c, --clean           force a clean build
  -f, --force           overwrite destination build directory
  -w WORK_DIR, --work_dir WORK_DIR
                        Overwrite the working directory
  -b BUILD_DIR, --build_dir BUILD_DIR
                        Overwrite the target build directory. Will be ignored if used in
                        combination with --binary_only or --*_install
  --binary_only         Only create a single binary
  --arch_install        Install the created deb bundle using debtap and pacman
  --deb_install         Install the created deb bundle using dpkg
```



## TODOs
 - [x] Add support for some common arguments
 - [ ] Figure out why the AppImages don't work certain tasks, e.g. YoutubeMusic (i.e. figure out how to add the missing gstreamer dependencies)
 - [x] Add arch auto install support
 - [ ] Test debian auto install support
 - [ ] Add binary extraction support
 - [ ] Add support for icons

