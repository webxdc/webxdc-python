#!/usr/bin/env python3
import argparse
import os
import shutil
import sys

import htmlmin
import lesscpy
from jsmin import jsmin


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="App Builder",
    )
    parser.add_argument(
        "-n",
        "--name",
        default=os.path.basename(os.path.dirname(os.path.abspath(__file__))),
        help="App package's base name",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Bundle webxdc package with debugging tools included",
    )

    return parser


def size_fmt(num: float) -> str:
    suffix = "B"
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)  # noqa
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)  # noqa


def minify_js() -> None:
    if os.path.exists("js"):
        js_files = sorted(
            filename for filename in os.listdir("js") if filename.endswith(".js")
        )
        if not js_files:
            return

        os.makedirs("build/js")

        bundle = False
        with open("index.html", encoding="utf-8") as src:
            if "js/bundle.js" in src.read():
                bundle = True

        if bundle:
            with open(f"build/js/bundle.js", "w", encoding="utf-8") as dest:
                for filename in js_files:
                    with open(f"js/{filename}", encoding="utf-8") as src:
                        if filename.endswith(".min.js"):
                            text = src.read()
                        else:
                            text = jsmin(src.read())
                    dest.write(text)
                    if not text.endswith(";"):
                        dest.write(";")
        else:
            for filename in js_files:
                if filename.endswith(".min.js"):
                    files.append(f"js/{filename}")
                else:
                    with open(f"js/{filename}", encoding="utf-8") as src:
                        with open(
                            f"build/js/{filename}", "w", encoding="utf-8"
                        ) as dest:
                            dest.write(jsmin(src.read()))


def minify_css() -> None:
    if os.path.exists("css"):
        css_files = sorted(
            filename for filename in os.listdir("css") if filename.endswith(".css")
        )
        if not css_files:
            return

        os.makedirs("build/css")

        bundle = False
        with open("index.html", encoding="utf-8") as src:
            if "css/bundle.css" in src.read():
                bundle = True

        if bundle:
            with open(f"build/css/bundle.css", "w", encoding="utf-8") as dest:
                for filename in css_files:
                    with open(f"css/{filename}", encoding="utf-8") as src:
                        if filename.endswith(".min.css"):
                            dest.write(src.read())
                        else:
                            dest.write(lesscpy.compile(src, minify=True, xminify=True))
        else:
            for filename in os.listdir("css"):
                if filename.endswith(".min.css"):
                    files.append(f"css/{filename}")
                else:
                    with open(f"css/{filename}", encoding="utf-8") as src:
                        with open(
                            f"build/css/{filename}", "w", encoding="utf-8"
                        ) as dest:
                            dest.write(lesscpy.compile(src, minify=True, xminify=True))


def minify_html() -> None:
    with open("index.html", encoding="utf-8") as src:
        with open("build/index.html", "w", encoding="utf-8") as dest:
            dest.write(htmlmin.minify(src.read()))

    if os.path.exists("pages"):
        html_files = sorted(
            filename for filename in os.listdir("pages") if filename.endswith(".html")
        )
        if not html_files:
            return

        os.makedirs("build/pages")

        for filename in html_files:
            with open(f"pages/{filename}", encoding="utf-8") as src:
                with open(f"build/pages/{filename}", "w", encoding="utf-8") as dest:
                    dest.write(htmlmin.minify(src.read()))


if __name__ == "__main__":
    args = get_parser().parse_args()
    app_archive = args.name if args.name.endswith(".xdc") else f"{args.name}.xdc"
    files = []

    # CLEAN
    shutil.rmtree("build", ignore_errors=True)
    for name in os.listdir():
        if os.path.isfile(name) and name.endswith(".xdc"):
            os.remove(name)
    os.makedirs("build")

    if args.debug:
        files.append("eruda.js")

    if os.path.exists("assets"):
        shutil.copytree("assets", "build/assets")

    # TRANSCRYPT
    if os.path.exists("app.py"):
        from transcrypt.__main__ import main as transcrypt

        sys.argv = ["transcrypt"]
        if args.debug:
            sys.argv.append("-n")
        sys.argv.append("app.py")
        transcrypt()
        shutil.copytree("__target__", "build/__target__")
        os.remove(f"build/__target__/app.project")

    minify_js()
    minify_css()
    minify_html()

    # ADD METADATA
    for name in ("manifest.toml", "icon.png", "icon.jpg"):
        if os.path.exists(name):
            files.append(name)

    for path in files:
        shutil.copyfile(f"{path}", f"build/{path}")
    project_root = os.path.abspath(".")
    os.chdir("build")
    shutil.make_archive(f"{project_root}/{app_archive}", "zip")
    os.chdir(project_root)
    os.rename(f"{app_archive}.zip", app_archive)

    # for testing:
    if os.path.exists("webxdc.js"):
        shutil.copyfile("webxdc.js", "build/webxdc.js")

    with open(app_archive, "rb") as file:
        size = len(file.read())
    print(f"App saved as: {app_archive} ({size_fmt(size)})")
