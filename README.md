# WattMaven Analytics

A simple analytics microservice for PV systems.

## Development

### Setup

Install the following external dependencies:

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Running the application

```bash
# Create the virtual environment
make

# Activate the virtual environment
source .venv/bin/activate

# Install the dependencies
uv sync --all-packages

# Run the application in development mode
make dev
```

## Release

This project uses [Hatch](https://hatch.pypa.io/) for building and releasing.

```bash
# Bump the version
cz bump --major-version-zero

# Push the changes
git push
git push -u origin v<new-version>
```

## License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments

### Licenses

See [LICENSES](./LICENSES) for details.

- [PVAnalytics](https://github.com/pvlib/pvanalytics) - Primarily uses documentation examples and code snippets.
