import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, TUTORIAL_VIDEO_ID
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


async def send_tutorial(client: Client, chat_id: int):
    """Send the tutorial video to the user before checking for subscription."""
    if TUTORIAL_VIDEO_ID:
        try:
            await client.send_video(
                chat_id=chat_id,
                video=TUTORIAL_VIDEO_ID,
                caption="Here's how to use the bot! 🎥"
            )
        except Exception as e:
            print(f"Error sending tutorial video: {e}")


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass

    # Send tutorial video before proceeding
    await send_tutorial(client, message.chat.id)

    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Wait A Second...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:
            caption = CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "",
                                            filename=msg.document.file_name) if CUSTOM_CAPTION and msg.document else msg.caption.html or ""

            reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡️ ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton('🍁 𝕚𝔹𝕆𝕏 𝕋𝕍', url='https://t.me/iBOX_TV')
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    """Handle users who haven't joined the required channels yet."""
    # Send tutorial video before enforcing subscription
    await send_tutorial(client, message.chat.id)

    buttons = [
        [
            InlineKeyboardButton(text="Join Channel 1", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel 2", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(
                text='Try Again Now🥰',
                url=f"https://t.me/{client.username}?start={message.command[1]}" if len(message.command) > 1 else f"https://t.me/{client.username}"
            )
        ]
    ]

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="<b>Processing ....</b>")
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
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

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)
    else:
        msg = await message.reply("<code>Use this command as a reply to any telegram message without any spaces.</
