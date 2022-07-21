#!/usr/bin/env python
import datetime

import click
import os
import shutil
import hashlib

ext = (".jpeg", ".png", ".py", ".docx", ".pdf")

@click.group()
def main():
    pass


@main.command('move', short_help="moves files to given destination")
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
def move(src, dst):
    print(f"Moving  files from {src} to {dst}...")
    print("\n")
    abs_source = os.path.abspath(src)
    abs_destination = os.path.abspath(dst)
    for file in os.listdir(src):
        abs_file = os.path.join(abs_source, file)
        if file.startswith('.'):
            continue
        else:
            shutil.move(abs_file, abs_destination)
    print("Complete")


@main.command('purge', short_help="cleans given directory of any duplicate files")
@click.argument('dir', nargs=1)
def purge(dir):
    print(f"Cleaning now...")
    print("\n")
    copies = calculate_digests(dir)
    delete_files(copies)


def check_for_copy(file, file_hash, digest_map, copies):
    if file_hash not in digest_map.values():
        return False
    elif file_hash in digest_map.values():
        copies.append(file)
        return True


def calculate_digests(dir):
    digest_map = {}
    copies = []
    abs_directory = os.path.abspath(dir)
    for file in os.listdir(dir):
        abs_file = os.path.join(abs_directory, file)
        if os.path.isdir(abs_file):
            continue
        elif file.lower().endswith(ext):
            block_size = 1048
            file_hash = hashlib.md5()
            with open(abs_file, "rb") as f:
                chunk = f.read(block_size)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(block_size)
                if not check_for_copy(abs_file, file_hash.hexdigest(), digest_map, copies):
                    digest_map[file] = file_hash.hexdigest()
    return copies


def delete_files(copies):
    for c in copies:
        print(f"Deleting {c}")
        os.remove(c)


@main.command('sort', short_help="sorts files by month or day")
@click.argument('dir', nargs=1)
def sort(dir):
    abs_directory = os.path.abspath(dir)
    make_folders(abs_directory, map_files(dir, abs_directory))


def checking_same_dates(datestamp, library):
    if datestamp not in library:
        library.append(datestamp)


def convert_to_standard_format(datestamp):
    standard_date = datetime.datetime.fromtimestamp(datestamp)
    shortened = standard_date.strftime('%Y-%m-%d')
    return shortened


def map_files(dir, abs_directory):
    library = {}
    ordered_datestamps = []
    for file in os.listdir(dir):
        abs_file = os.path.join(abs_directory, file)
        stat = os.stat(abs_file)
        og_datestamp = stat.st_mtime
        checking_same_dates(convert_to_standard_format(og_datestamp), ordered_datestamps)
    ordered_datestamps = sorted(ordered_datestamps)
    for i in ordered_datestamps:
        library[i] = []
    for file in os.listdir(dir):
        abs_file = os.path.join(abs_directory, file)
        stat = os.stat(abs_file)
        og_datestamp = stat.st_ctime

        for key in library:
            if convert_to_standard_format(og_datestamp) == str(key):
                library[key].append(abs_file)
    return library


def make_folders(abs_directory, library):
    for key in library:
        path = os.path.join(abs_directory, key)
        os.mkdir(path)
        for item in library[key]:
            shutil.move(item, path)


@main.command('copy', short_help="copy files to a separate location")
@click.argument('src', nargs=1)
def copy():
    print("blank")


if __name__ == "__main__":
    main()
