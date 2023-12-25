# Sir Francesco

Sir Francesco is the first implementation of a Telegram bot designed to bridge the digital with the analog world. Created by Francesco, with a spirit of connection and giving, this platform allows family and friends to receive and offer actions that make a difference in the world.

While this bot is named after its first creator, Francesco, it is encouraged that when you deploy your version, you rename it appropriately to reflect the person or entity offering the favors. Personalizing the bot's name makes the experience more relatable and direct for those interacting with it.

## Purpose and Goals

This modest platform aims to:

- Foster actions in favor of individuals and communities with a direct and expressed commitment.
- Help recipients understand the spirit behind the offers made.
- Connect two or more people towards a common goal.

## Feedback and Contributions

We value your input and contributions! If you are using this software and have any feedback, suggestions, or would like to contribute, please feel free to open an issue on our GitHub repository or contact us directly.

### Feedback Voluntary Commitment

If you are using this software, we would love to hear how it's being used! Your feedback helps improve the project and guide future development directions. Feel free to open an issue on our GitHub repository to share your experience, send us an email, or just say hi and let us know you're using our software.

### Contributing to the Code

If you're interested in contributing to the code, check out the open issues or submit a pull request with your changes. Every contribution is welcome!

## Installation and Usage

Here, you can insert instructions on how to install and use your project.


### Configuration

To configure the project, create a `config.py` file in the root of the project with the following contents:

```python
# config.py
TELEGRAM_TOKEN=""  # The token received from @BotFather
DATABASE_ID = ""    # The database containing the vouchers
DATABASE_USERS = "" # The database for users
NOTION_AUTH = "secret_"

ENV="test"
if ENV=="test":
    TELEGRAM_TOKEN="override" # Override for testing
    DATABASE_ID = "override"  # Override for production
    DATABASE_USERS = "override"  # Override for production
    NOTION_AUTH = "override"  # Override for production
    #USER_TEST="override" #Override user for testing


## License

This project is released under the [GNU Lesser General Public License v3.0](./LICENSE). Please refer to the license file for more information.
