#!/usr/bin/env python3

from os import path, mkdir , chdir, system
from subprocess import Popen
from shutil import rmtree, copytree
from argparse import ArgumentParser


def create_html_file(target_url, dest_file):
    with open(dest_file, "w+") as file:
        file.writelines(f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Refresh" content="0; url='{target_url}'" />
    <title>Redirecting</title>
  </head>
  <body>
    <h1>Redirecting</h1>
  </body>
</html>
""")


def create_tauri_src(working_dir, app_name):
    chdir(working_dir)
    cmd = f"cargo tauri init --ci --dist-dir ../html --dev-path ../html --window-title '{app_name}' --app-name '{app_name}' --before-build-command '' --before-dev-command ''"
    p = Popen([cmd], shell=True) 

    p.wait()
    return p.returncode


def create_tauri_app(working_dir, dest_dir, args):
    chdir(path.join(working_dir, "src-tauri"))

    # Fix the bundle identifier
    filedata = None
    with open("tauri.conf.json", "r") as file:
        filedata = file.read()

    old_identifier = "com.tauri.dev"
    new_identifier = f"com.{args.name.replace(' ', '.')}"
    filedata = filedata.replace(old_identifier, new_identifier)

    with open("tauri.conf.json", "w") as file:
        file.writelines(filedata)

    # Build the app
    p = Popen(['cargo tauri build'], shell=True)

    p.wait()

    if not args.arch_install and not args.deb_install:
        # Copy binaries into destination directory
        if path.exists(dest_dir): 
            if args.force:
                rmtree(dest_dir)
            else:
                print("Build directory already exists... Aborting")
                exit(1)
        if args.binary_only:
            # TODO: Add support for this (How do I detect the proper file in /target/release/)
            print("This option is currently not supported")
            exit(1)
        else:
            copytree('target/release/bundle/', dest_dir)
    elif args.arch_install:
        deb_path = './target/release/bundle/deb/*.deb'
        cmd = f"debtap -Q {deb_path}"
        print(f"Executing '{cmd}'")
        system(cmd)
        tar_path = './target/release/bundle/deb/*.pkg.tar.zst'
        cmd = f"sudo pacman -U {tar_path}"
        print(f"Executing '{cmd}'")
        system(cmd)
    elif args.deb_install:
        # TODO: Test this
        deb_path = './target/release/bundle/deb/*.deb'
        cmd = f"sudo dpkg {deb_path}"
        print(f"Executing '{cmd}'")
        system(cmd)

    return p.returncode


def main(args):
    build_dir = path.realpath(args.build_dir)

    # Create the working_directory
    print("Creating working directory")
    working_dir = path.join(args.work_dir, args.name)
    if not path.exists(working_dir):
        mkdir(working_dir)
    elif args.clean:
        rmtree(working_dir)
        mkdir(working_dir)

    # Ensure tauri-cli is installed
    print("Ensuring tauri-cli is installed")
    p = Popen(['cargo install tauri-cli'], shell=True)
    p.wait()

    # Create the index.html file in the working directory
    print("Creating redirect html")
    html_dir = path.join(working_dir, "html")
    if not path.exists(html_dir):
        mkdir(html_dir)
    create_html_file(args.url, path.join(html_dir,"index.html"))

    # Create the tauri src folder followed by the app
    print("Creating tauri src folder")
    create_tauri_src(working_dir, args.name)
    print("Building tauri app")
    create_tauri_app(working_dir, build_dir, args)


if __name__ == "__main__":
    parser = ArgumentParser(description='Create a lightweight tauri webapp.')
    parser.add_argument('name', type=str, help='The name of the app that will be created')
    parser.add_argument('url', type=str, help='The url of the target site')
    parser.add_argument('-c', '--clean', dest='clean', action='store_true',
                        help='force a clean build')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='overwrite destination build directory')
    parser.add_argument('-w', '--work_dir', dest='work_dir', action='store', type=str, default="/tmp/",
                        help='Overwrite the working directory')
    parser.add_argument('-b', '--build_dir', dest='build_dir', action='store', type=str, default="./build/",
                        help='Overwrite the target build directory. Will be ignored if used in combination with --binary_only or --*_install')
    parser.add_argument('--binary_only', dest='binary_only', action='store_true', default=False,
                        help='Only create a single binary')
    parser.add_argument('--arch_install', dest='arch_install', action='store_true', default=False,
                        help='Install the created deb bundle using debtap and pacman')
    parser.add_argument('--deb_install', dest='deb_install', action='store_true', default=False,
                        help='Install the created deb bundle using dpkg')

    args = parser.parse_args()
    main(args)
