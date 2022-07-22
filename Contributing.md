# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

In general currently we focus on 2 ways of additions in this repository:
- Addition of functionality by enhancing the core signal-ocean sdk library.
- Addition of examples that demostrate the usage of the signal-ocean sdk library.

## Building the solution
### Linux
- Run build.sh, on root folder.

### Windows
- Open bash (requires WSL enabled)
- Run build.sh, on root folder

#### Native Windows build
- No script provided, but steps of `build.sh` can be replayed manually over powershell.

## Building the githubdocs
- Create a new venv.
- Install requirements listed under `.github/workflows`
- Run `mkdocs serve` (builds and deploys locally the github docs page)

## Contributing on the core library
The reasons to change the core library are the following ones:
- Addition\Removal of an API wrapper.
- Edit of an existing API wrapper (endpoints added, removed, updated)
- Cration of help core functions that facilitate API calls and usage

Increase the version, and document your changes by:
    - Updating the version.txt file
    - Creating a new Version x.x.x.md file under docs/releases. This file holds all useful information about that end users of the library should be aware of.
    The versioning scheme we use is [SemVer](http://semver.org/).

Update the mkdocs.yml file if needed


## Contributing on the examples.
Contributions on the examples uses the `signal-ocean` library. If your contribution is paired with a core change, you need to build the library and install the local build of the library (`build.sh` covers this). Otherwise you can use the publicly available library directly.

- Add you example under the proper category on `docs\examples`
    - There is one folder per API
    - If your example uses multiple APIs use the `docs\examples\jupyter\Combined Examples` folder

- Make sure that the example can run on [Colab](https://colab.research.google.com/), as is, only by adding an API keys.
- API keys should never be commited with the examples. Invalidate any accidental addition of api keys from the portal.

## Pull Request Process

1. Create a feature branch with your changes and issue a PR that describes the changes. 
2. Make sure version is increased if needed 
3. Make sure automated build is succesful (merge is not allowed over broken builds)