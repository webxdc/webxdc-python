# Webxdc development with Python

This is a template project to develop Webxdc apps with the Python programming language!

## Requirements

To transpile Python code into JavaScript, [Transcrypt](https://www.transcrypt.org/) is
used, to install it and also other tools to minify/optimize the final webxdc, run:

```sh
 python -m pip install -r ./requirements.txt
```

## Building

To package your Webxdc:

```sh
python ./build.py
```

The output is a file with `.xdc` extension.

## Testing

After building, you can test the app. The project comes with an
small simulator that allows to test your app in your browser, to do it
just go to the root of the project and run:

```sh
python -m http.server
```

then open in your browser the URL that is displayed in the shell.

## Releasing

To automatically build and create a new GitHub release with your `.xdc` file:

```
git tag v1.0.1
git push origin v1.0.1
```

## Try it now!

### GitHub Template

[Create a repo from this template on GitHub](https://github.com/webxdc/webxdc-python/generate).
