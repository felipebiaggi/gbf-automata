# Granblue Fantasy Automata

Granblue Fantasy Automata is a bot inspired by FGO Automata, designed for automating repetitive tasks. It consists of a server responsible for processing the game's logic and directly interacting with the interface, and a browser extension for Chromium-based browsers that monitors DOM mutations and transmits relevant events to the server.

## How to Run

1. Navigate to `chrome://extensions/` and enable **Developer mode**.  
2. Select the **extension** folder using the **Load unpacked** option. After this, the extension will be installed in your browser.  

In **Granblue Fantasy**, ensure that the game screen height is at least **700px**, and configure the following options in the browser:

- **Bottom Menu:** On  
- **Automatic Resizing:** Off  
- **Window Size:** Medium  

In **Display Settings**, make sure none of the options are enabled.

In **Miscellaneous**, enable the following options:

- **AP Auto-Restore**
- **EP Auto-Restore**
- **AAP Auto-Restore**

**Note:** In the current version, it's not possible to automatically choose the team and summon. Therefore, configure **Auto Pick** for the team you wish to use.  

Next, in the **`settings.toml`** file, populate:  
- `url` with the address of the battle you want to automate.  
- `runs` with the number of times you want to repeat the battle.  

## Running the Bot

To run the bot, you will need to install **Poetry**. You can install Poetry by following the instructions on the [official website](https://python-poetry.org/docs/#installation).  

Once Poetry is installed, execute the following commands:

```console
$ poetry install
$ poetry shell
$ python -m gbf_automata
```

## Upcoming

- [ ] **Automatic CAPTCHA Detection and Alerts:** Implement automatic CAPTCHA detection with notifications via Discord or Web Notifications.
- [ ] **Team Selection:** Implement functionality for automatic team selection.
- [ ] **Enable Pre-Battle Auto Attack:** Add an option to enable Auto Attack before the battle begins.
- [ ] **Battle Logic for Using Skills and Items:** Implement logic to automatically use skills and items such as **Green Potion**, **Blue Potion**, and **Elixir** during the battle.


