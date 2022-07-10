#!/usr/bin/env python
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
    display(copies)


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
                if not check_for_copy(file, file_hash.hexdigest(), digest_map, copies):
                    digest_map[file] = file_hash.hexdigest()
    return copies


def display(copies):
    print("Possible duplicate files are:")
    for i in copies:
        print(i)


@main.command('sort', short_help="sorts files by month or day")
def sort():
    print("blank")


@main.command('copy', short_help="copy files to a separate location")
@click.argument('src', nargs=1)
def sort():
    print("blank")


if __name__ == "__main__":
    main()
