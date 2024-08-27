#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from string import Template


def run_docfx(command, config_file_path):
    subprocess.run(["dotnet", "docfx", command, "--logLevel", "Warning", config_file_path])


def generate_metadata(version):
    print(f"Generate metadata for {version}...")
    with open(os.path.join("docfx", "docfx-template-metadata.json"), "r") as template_file:
        template = Template(template_file.read())
    docfx_config_file_path = "tmp-docfx.json"
    with open(docfx_config_file_path, "w") as docfx_config_file:
        docfx_config_file.write(template.substitute(version=version))
    run_docfx("metadata", docfx_config_file_path)
    os.remove(docfx_config_file_path)
    print("Done.")


def generate_site(version):
    print(f"Generate site for {version}...")
    with open(os.path.join("docfx", "docfx-template-build.json"), "r") as template_file:
        template = Template(template_file.read())
    docfx_config_file_path = os.path.join("tmp", f"docfx-{version}.json")
    with open(docfx_config_file_path, "w") as docfx_config_file:
        docfx_config_file.write(template.substitute(version=version))
    run_docfx("build", docfx_config_file_path)
    print("Done.")


if __name__ == "__main__":
    subprocess.run(["dotnet", "tool", "restore"], capture_output=True)

    if not os.path.isdir("tmp"):
        os.makedirs("tmp")

    versions = [ version for version in os.listdir("src") if os.path.isdir(os.path.join("src", version)) ]

    for version in versions:
        generate_metadata(version)
        generate_site(version)
