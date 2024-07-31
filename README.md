# Unique Universes CJ24's Application

Our application is a shooting minigame, based on precise and calculated shots from your ship to the enemy ship.

## How is the theme represented ?

The minigame relies on the user’s ability to calculate a shot with the help of (a lot of) raw information provided to the user.
 This is the interesting part, the user has to face an information overflow and extract the important data in order to play the game.

## Availables commands

- /shoot - Play the minigame.

![The game](https://media.githubusercontent.com/media/Snipy7374/code-jam-24-universes/main/readme_assets/minigame.png)

- /about - Get information about the application and the team.

![About](https://media.githubusercontent.com/media/Snipy7374/code-jam-24-universes/main/readme_assets/about.png)

# For the developers

This repository is the entry of the unique universes team for the Python Discord Code Jam 2024.

# Docker Usage
## Building

```sh
docker build -t unique-universes -f .docker/Dockerfile .
```

## Running
```sh
docker run --rm -it -e BOT_TOKEN=YOUR_TOKEN_HERE unique-universes
```

# Manual installation
## Installing the dependencies

To install all the required dependencies to run the bot execute these commands:

```shell
pip install poetry
poetry install
```

## Creating the .env file

To be able to execute the bot locally you will need to create and grab the token of a discord bot. To create a bot head to the [discord developer portal]("https://discord.com/developers/applications/") and follow these [instructions to create a bot and copy its token]("https://discordpy.readthedocs.io/en/stable/discord.html").

After having copied the token you need to create a file called `.env` at the root of the project. Then type  `BOT_TOKEN=` and paste the actual bot token after the equal sign. The file should look like this:

```ini
BOT_TOKEN=ExampleOfBotTokenHere
```

## Run project

```sh
python -m src
```

# Setting Up the Dev Env

If you are a team member make sure to read this section, otherwise you can skip this.

> [!NOTE]
> The steps listed here needs to be done only the first time when setting up the project locally.

## Required Python version

This project requires python 3.12 to work. If you don't have it installed proceed to install it from the official python website.

## Creating and activating a venv (virtual environment)

The most preferable way to work on a project is to create a virtual envirnoment where to install the dependencies. This is extremely useful to avoid conflicts between different projects that install dependencies globally.

To create a virtual environment run the following command in your terminal:

```shell
python3 -m venv .venv
```

> [!NOTE]
> If you are on windows and have different python versions installed without a python version manager, you can run the following command to use python 3.12
> `py -3.12 -m venv .venv`

you can replace `.venv` in the commands with a path (e.g `example_folder/.venv`) if needed. If you provide only `.venv` python will create the environment in the same directory where you are running the command.

After having created the venv (virtual environment) you need to activate it.
To enable the venv run the following commands depending on your platform:

```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

To deactivate the venv type `deactivate` in the terminal.

## Pre-commit

Before commiting, make sure to run any pre-commit checks.
Install pre-commit if you haven't done yet:

```sh
pre-commit install
```

## Final words

Now you're ready to go, your local copy of the repository is ready to be ran.
