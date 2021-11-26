# Godot C# API

Unofficial web version of Godot's C# API documentation (https://paulloz.github.io/godot-csharp-api/).

## How to use this repository

Should I be unable to maintain this, here's a quick rundown of how to generate the documentation and build the website.

1. Install [DocFX](https://dotnet.github.io/docfx/)
1. Drop the API files inside `src/<version>/`
1. Add the corresponding **metadata** entry in the [`docfx.json` file](https://github.com/paulloz/godot-csharp-api/blob/main/docfx.json#L3-L12)
1. Add the corresponding **build** entry in the [`docfx.json` file](https://github.com/paulloz/godot-csharp-api/blob/main/docfx.json#L16-L20)
1. Add the corresponding link in the [`toc.yml` file](https://github.com/paulloz/godot-csharp-api/blob/main/toc.yml#L3-L4)
1. Run `docfx metadata`
1. Run `docfx build`

The whole website should now be built under `docs/`. You can preview it locally using `docfx serve docs/`. If you want to use the official Godot documentation logo, you'll also have to retrieve it from [there](https://github.com/godotengine/godot-design/).

## License

See the [index.md](https://github.com/paulloz/godot-csharp-api/blob/main/index.md) file for license details.
