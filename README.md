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


## Fortune Wheel Feature

### How Does It Work?

- Users initiate the fortune wheel by sending the `/fortunewheel` or `/fortune` command.
- Once the user spins the wheel, a random voucher from those available to the user is selected.
- Details of the selected voucher are then presented to the user, offering a unique and engaging experience.

This game adds an element of surprise and fun, engaging users interactively and providing them with the chance to discover new deals and rewards.




### Contributing to the Code

If you're interested in contributing to the code, check out the open issues or submit a pull request with your changes. Every contribution is welcome!

## Installation and Usage

Here, you can insert instructions on how to install and use your project.


# Configuration

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
```
## Configuring Bot Commands via @BotFather

To enhance the user experience and make it easier for users to interact with Sir Francesco, you can configure the bot commands with descriptions and emojis. This provides a quick guide and visual cues for users when they start typing '/' in the chat. Here's how you can set them up via @BotFather:

### Step-by-Step Guide:

1. **Open @BotFather:** Start a chat with [@BotFather](https://t.me/botfather) on Telegram.

2. **Select Your Bot:** Send the `/mybots` command, then select the bot you are configuring, which is Sir Francesco in this case.

3. **Go to Bot Settings:** Choose 'Bot Settings' from the options provided by @BotFather.

4. **Set Commands:** Select 'Edit Command' and enter the list of commands you want to set for your bot.

### Command List:

Copy and paste the following command list into the @BotFather chat when prompted:

''' 
start - 🚀 Embark on a journey with Sir Francesco!
fortune - 🎡 Spin the wheel of fortune!
info - ℹ️ Curious about Sir Francesco?
'''

These commands and descriptions will now appear in the command list for users interacting with Sir Francesco. It's a great way to guide users and make the bot feel more friendly and accessible.

### Note:

- You can always modify, add, or delete commands later by revisiting the @BotFather and adjusting your bot's settings.
- Make sure the commands are up-to-date with the actual functionality of your bot to avoid any confusion for the users.

# License

This project is released under the [GNU Lesser General Public License v3.0](./LICENSE). Please refer to the license file for more information.
