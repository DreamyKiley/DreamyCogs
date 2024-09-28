# Leveling Cog

A leveling system cog for Redbot that allows users to gain XP and level up by sending messages. Admins can modify XP and levels, toggle the leveling feature, and view the server's leaderboard.

## Features

- **Leveling System:** Users gain XP and level up by sending messages.
- **XP Calculation:** XP is awarded twice per minute.
- **Commands:**
  - `!level [user]`: Check the level and XP of a user.
  - `!levelmsg`: Toggle level-up notifications on or off for yourself.
  - `!leaderboard`: View the top 10 users on the leveling leaderboard.
  - `!setyxp <user> <amount>`: Modify a user's XP. (Admin only)
  - `!setlevel <user> <level>`: Set a user's level and reset their XP to 0. (Admin only)
  - `!setprestige <user> <prestige>`: Set a user's prestige. (Admin only)
  - `!togglelevels`: Enable or disable the leveling feature. (Admin only)
  - `!levelmsgdel <s>`: Set the time (in seconds) after which level-up messages will auto-delete. (Admin only)
<sub>set to 0 to disable</sub>

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
```[p]cog install DreamyCogs levels```

3. **Load the cog**
```[p]load levels```

## Configuration

The cog uses the `Config` class to store leveling data and settings:
- **Level Data:** Tracks each user's level and XP.
- **Last Message Timestamp:** Ensures XP is awarded only twice per minute.
- **Leveling Enabled:** Toggle leveling on or off for the server.

## Commands

### `!level [user]`
Check the level and XP of a user. If no user is specified, it shows the level and XP of the command author.

### `!leaderboard`
Displays the top 10 users on the leaderboard for the server.

### `!modifyxp <user> <amount>`
Add or remove XP from a specified user. This command is only available to admins.

### `!modifylevel <user> <level>`
Set a user's level and reset their XP to 0. This command is only available to admins.

### `!toggleleveling`
Enable or disable the leveling feature for the server. This command is only available to admins.

## Customization

- **XP Award:** Currently fixed at 10 XP per message. Can be adjusted in the code.
- **Level XP Calculation:** Uses an exponential formula to determine XP needed for each level. Default multiplier is `1.15`.

## Example

Here’s an example of how the cog works:

1. A user sends a message.
2. The cog checks if leveling is enabled and if the XP can be awarded.
3. The user gains XP and may level up if they accumulate enough XP.
4. Admins can use commands to modify XP, set levels, and toggle the leveling system.

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
