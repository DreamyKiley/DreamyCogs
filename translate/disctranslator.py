from googletrans import Translator, LANGUAGES
from redbot.core import commands
from discord import Embed

class DiscTranslator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="translate")
    @commands.cooldown(1, 30, commands.BucketType.user)  # 1 use per 30 seconds per user
    async def translate_text(self, ctx, source_language: str, target_language: str, *, text: str):
        """Translates the given text from source language to target language."""
        if source_language not in LANGUAGES or target_language not in LANGUAGES:
            await ctx.send("Invalid language code. Please use valid 2-letter language codes.")
            return

        translator = Translator()
        try:
            translated = translator.translate(text, src=source_language, dest=target_language)
            translated_text = translated.text
            
            embed = Embed(
                title="Translation Result",
                description=(
                    f"**Original Text:**\n"
                    f"{text}\n\n"
                    f"**Translated Text:**\n"
                    f"{translated_text}\n\n"
                    f"[DreamyCogs](https://github.com/DreamyKiley/DreamyCogs/)\n\n"
                ),
                color=0x50C878  # Emerald Green color
            )
            embed.set_footer(text="Powered by Google Translate")  # EMPTY FOR NOW

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred while translating the text: {e}")

    @commands.command(name="languagecodes")
    async def language_codes(self, ctx):
        """Shows the ISO 639-1 codes of the top 10 most popular languages."""
        # Define the top 10 most popular languages
        top_10_languages = {
            "en": "English",
            "es": "Spanish",
            "zh": "Chinese",
            "hi": "Hindi",
            "ar": "Arabic",
            "pt": "Portuguese",
            "bn": "Bengali",
            "ru": "Russian",
            "ja": "Japanese",
            "de": "German"
        }

        # Create the embed for the top 10 languages
        embed = Embed(
            title="Top 10 Language Codes",
            description="Here are the ISO 639-1 codes for the top 10 most popular languages:",
            color=0x50C878  # Emerald Green color
        )
        
        for code, language in top_10_languages.items():
            embed.add_field(name=language, value=code, inline=True)
        
        # Add footer with the link to the full list of ISO 639-1 codes
        embed.set_footer(text="For a complete list of ISO 639-1 codes, visit https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes")

        await ctx.send(embed=embed)

    @commands.command(name="translatehelp")
    async def translate_help(self, ctx):
        """Provides information on how to use the translation command."""
        help_message = (
            "**Translation Cog Help**\n\n"
            "1. **Translate text:** `!translate <source_language> <target_language> <text>`\n"
            "   - Translates the given text from the source language to the target language. For example, `!translate en es Have a good day`.\n\n"
            "2. **Language Codes:** `!languagecodes`\n"
            "   - Shows the ISO 639-1 codes of the top 10 most popular languages.\n\n"
            "For more information, visit [Created by Kiley W.](https://github.com/DreamyKiley)"
        )
        await ctx.send(help_message)
