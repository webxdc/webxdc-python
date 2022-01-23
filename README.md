# Webxdc development with Python

This is an example project to show how to develop webxdc apps with Python.

## Requirements

This project depends on:
- [Python](https://python.org/)
- [Transcrypt](https://www.transcrypt.org/)

Check their documentation to know how to install them.

## Building

To convert your Python code to JavaScript, execute:

```sh
python -m transcrypt app.py
```

## Testing

After building, you are ready to test the app. The project comes with an
small simulator that allows to test your app in your browser, to do it
just go to the root of the project and run this command:

```sh
python -m http.server
```

then open in your browser the URL that is displayed in the shell.

## Packaging

To use the app in Delta Chat, you need to package it in a `.xdc` archive,
the `create-xdc.sh` script helps you to do that:

```sh
./create-xdc.sh
```
