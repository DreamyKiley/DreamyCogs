### **Requires "googletrans" to be installed**
```pip install googletrans==4.0.0-rc1```

![translate_prev](https://github.com/user-attachments/assets/86ba669a-c3b1-4df4-a95e-358422566a06))

# Translator Cog

A cog for Redbot that provides translation services using Google Translate. Users can translate text between different languages and view language codes for popular languages.

## Features

- **Translate Text:** Translates text from a source language to a target language.
- **Language Codes:** Provides ISO 639-1 codes for the top 10 most popular languages.
- **Help Command:** Provides instructions on how to use the translation commands.

## Commands

### `!translate <source_language> <target_language> <text>`
Translates the given text from the source language to the target language.
- **Parameters:**
  - `<source_language>`: The ISO 639-1 code of the source language.
  - `<target_language>`: The ISO 639-1 code of the target language.
  - `<text>`: The text to be translated.
- **Example:** `!translate en es Have a good day`

### `!languagecodes`
Shows the ISO 639-1 codes of the top 10 most popular languages.

## Installation

1. **Download the repo with [Redbot](https://github.com/Cog-Creators/Red-DiscordBot)**
   ```[p]repo add DreamyCogs https://github.com/DreamyKiley/DreamyCogs```

2. **Install the cog**
   ```[p]cog install DreamyCogs translate```

3. **Load the cog**
   ```[p]load translate```

## Example

Here’s how the command works:

1. **Run the Command:**
   - Use `!translate <source_language> <target_language> <text>` to translate text.
   - Use `!languagecodes` to view the top 10 language codes.

2. **View the Translation:**
   - The bot will send an embed message with the original and translated text.

3. **View Language Codes:**
   - The bot will send an embed message with the ISO 639-1 codes of popular languages.

## Support

For support or more information, visit [DreamyCogs GitHub](https://github.com/DreamyKiley).
