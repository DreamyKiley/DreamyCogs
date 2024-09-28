# Message Logger Cog

A cog for Redbot that logs message deletions and edits in a designated channel. Admins can configure which channels, roles, and users to include or exclude from logging, as well as set the log channel.

## Features

- **Log Deletions and Edits:** Logs messages when they are deleted or edited.
- **Configuration:** Admins can set which channel will receive the logs and control which channels, roles, and users are excluded from logging.
- **Commands:**
  - `!logchannel [channel]`: Set the channel where logs will be sent. (Admin only)
  - `!log [items]`: Toggle inclusion or exclusion of specific channels, roles, or users from logging. (Admin only)
  - `!loghelp`: Provides information on how to use the logging commands.

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
   ```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
   ```[p]cog install DreamyCogs messagelogger```

3. **Load the cog**
   ```[p]load messagelogger```

## Configuration

The cog uses the `Config` class to store logging settings:
- **Log Channel:** The channel where logs are sent.
- **Excluded Channels:** Channels excluded from logging.
- **Excluded Roles:** Roles whose messages are excluded from logging.
- **Excluded Users:** Users whose messages are excluded from logging.

## Commands

### `!logchannel [channel]`
Set the channel where message logs will be sent. This command is available only to admins.

### `!log [items]`
Toggle inclusion or exclusion of specific channels, roles, or users from message logging. You can specify channels with `#channel`, roles with `@role`, or users with `@username`. This command is available only to admins.

## Example

Here’s how the cog works:

1. **Set the Log Channel:**
   - Use `!logchannel #channel` to specify where logs will be sent.

2. **Toggle Logging:**
   - Use `!log #channel1 @role1 @username1` to include or exclude specific items from logging.

3. **View Logs:**
   - When a message is deleted or edited, the bot sends an embed with the details to the configured log channel.

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
