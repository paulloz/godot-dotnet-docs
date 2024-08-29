#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import subprocess

from string import Template


BUILD_DIR = "site"
TMP_DIR = "tmp"


def apply_version_template(template_file_path, result_file_path, version):
    with open(template_file_path, "r") as template_file:
        template = Template(template_file.read())
    with open(result_file_path, "w") as result_file:
        result_file.write(template.substitute(version=version))


def run_docfx(command, *args):
    if command == "metadata" or command == "build":
        args += ( "--logLevel", "Warning" )
    subprocess.run(["dotnet", "docfx", command, *args])


def generate_metadata(version):
    print(f"Generate metadata for {version}...")
    docfx_config_file_path = "tmp-docfx.json"
    apply_version_template(os.path.join("docfx", "docfx-template-metadata.json"), docfx_config_file_path, version)
    run_docfx("metadata", docfx_config_file_path)
    os.remove(docfx_config_file_path)
    print("Done.")


def generate_site(version):
    print(f"Generate site for {version}...")
    docfx_config_file_path = os.path.join(TMP_DIR, f"docfx-{version}.json")
    apply_version_template(os.path.join("docfx", "docfx-template-build.json"), docfx_config_file_path, version)
    run_docfx("build", docfx_config_file_path)
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("build.py")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--metadata", action="store_true")
    parser.add_argument("--build", action="store_true")

    args = parser.parse_args()

    subprocess.run(["dotnet", "tool", "restore"], capture_output=True)

    if args.metadata or args.build:
        if not os.path.isdir(TMP_DIR):
            os.makedirs(TMP_DIR)

        versions = [ version for version in os.listdir("src") if os.path.isdir(os.path.join("src", version)) ]

        if args.metadata:
            for version in versions:
                generate_metadata(version)

        if args.build:
            for version in versions:
                generate_site(version)

    if args.serve:
        if os.path.isdir(BUILD_DIR):
            try:
                run_docfx("serve", BUILD_DIR)
            except KeyboardInterrupt:
                pass
        else:
            print(f"Cannot serve {BUILD_DIR}/ directory, because it does not exist.")
