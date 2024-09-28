# CmdCleaner Cog

The `CmdCleaner` cog for Redbot automatically deletes specific commands from chat and allows server admins to manage which commands should be blocked or unblocked.

## Features

- **Automatic Command Deletion:** Deletes specific commands from chat after 1 second.
- **Command Management:**
  - **Block/Unblock Commands:** Admins can block or unblock commands using `!cmdc`.
  - **List Blocked Commands:** Admins can list all currently blocked commands with `!cmdclist`.

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
   ```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
   ```[p]cog install YourRepo cmdcleaner```

3. **Load the cog**
   ```[p]load cmdcleaner```

## Commands

- `!cmdc <command1> <command2> ...`: Block or unblock commands in the server. Example: `!cmdc hug cuddle`
- `!cmdclist`: List all currently blocked commands, excluding predefined commands like `sys` and `weather`.
- `!cmdcdelall`: A quick and dirty way to clear the blocked commands."

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
