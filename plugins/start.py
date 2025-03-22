import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, MessageNotModified

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, TUTORIAL_VIDEO_ID, CHANNEL_ID
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private)  # Single handler
async def start_command(client: Client, message: Message):
    """Handles the /start command."""
    user_id = message.from_user.id
    text = message.text

    # --- 1. Handle /start with arguments (File Requests) ---
    if len(text) > 7:  # Check for arguments *first*
        if not await subscribed(client, message):
            # --- Send Tutorial (Unsubscribed, with arguments) ---
            try:
                tutorial_message = await client.get_messages(CHANNEL_ID, TUTORIAL_VIDEO_ID)
                if tutorial_message.video:
                    await client.send_video(
                        chat_id=user_id,
                        video=tutorial_message.video.file_id,
                        caption=tutorial_message.caption,
                        parse_mode=ParseMode.HTML if tutorial_message.caption else None,
                    )
                else:
                    await message.reply_text("Error: The tutorial message is not a video.")
                    return
            except BadRequest as e:
                if "MESSAGE_ID_INVALID" in str(e):
                    await message.reply_text(f"Error: Invalid TUTORIAL_VIDEO_ID ({TUTORIAL_VIDEO_ID}). Check config.")
                else:
                    await message.reply_text(f"Error fetching tutorial: {e}")
                return
            except MessageNotModified:
                print("Tutorial video likely already sent.")
            except Exception as e:
                await message.reply_text(f"Error sending tutorial: {e}")
                return

            # --- Force Subscription (Unsubscribed, with arguments) ---
            buttons = [
                [
                    InlineKeyboardButton(text="📢 Join Channel 1", url=client.invitelink),
                    InlineKeyboardButton(text="🎥 Join Channel 2", url=client.invitelink2),
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Try Again",
                        # Include original arguments in the URL
                        url=f"https://t.me/{client.username}?start={message.command[1]}"
                    )
                ]
            ]
            await message.reply(
                text=FORCE_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username='@' + message.from_user.username if message.from_user.username else None,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True,
                disable_web_page_preview=True
            )
            return  # Stop processing

        # --- Subscribed, with arguments: Process file request ---
        if not await present_user(user_id):
            try:
                await add_user(user_id)
            except:
                pass

        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(reversed(range(end, start + 1)))
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            else:
                return  # Invalid arguments
        except Exception as e:
            await message.reply_text(f"Error decoding arguments: {e}")
            return

        temp_msg = await message.reply("⏳ **Fetching your files...** Please wait.")

        try:
            messages = await get_messages(client, ids)
            await temp_msg.delete()

            for msg in messages:
                caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name)
                           if CUSTOM_CAPTION and msg.document else msg.caption.html if msg.caption else "")
                reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

                try:
                    await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except Exception as e:
                    print(f"Error copying message: {e}")
                    pass
            return

        except Exception as e:
            await message.reply_text("❌ **An error occurred while retrieving your files.** Please try again.")
            print(f"Error getting messages: {e}")
            return

    # --- 2. Handle Plain /start (No Arguments) ---
    else:  # No arguments
        # Show welcome message (for BOTH subscribed and unsubscribed)
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ℹ️ About", callback_data="about"),
                 InlineKeyboardButton("🎬 iBOX TV", url="https://t.me/iBOX_TV")]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username='@' + message.from_user.username if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

# =====================================================================================##

WAIT_MSG = "⏳ **Processing...** Please wait."
REPLY_ERROR = "❌ **Incorrect Usage**\n\nUse this command as a reply to any **Telegram message**."

# =====================================================================================##
# Remove the not_joined and try_again_callback functions

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"📊 **Total Users:** `{len(users)}`")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

        pls_wait = await message.reply("📢 **Broadcasting Message...**\n\nThis might take some time.")

        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = (
            f"📢 **Broadcast Completed**\n\n"
            f"👥 **Total Users:** `{total}`\n"
            f"✅ **Successful:** `{successful}`\n"
            f"🚫 **Blocked Users:** `{blocked}`\n"
            f"🗑️ **Deleted Accounts:** `{deleted}`\n"
            f"⚠️ **Failed Deliveries:** `{unsuccessful}`"
        )

        return await pls_wait.edit(status)
    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
