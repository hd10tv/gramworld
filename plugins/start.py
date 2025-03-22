import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, MessageNotModified

from bot import Bot
from config import ADMINS, OWNER_ID, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, TUTORIAL_VIDEO_ID
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private)  # Single handler
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # --- Send Tutorial if NOT Subscribed ---
    if not await subscribed(client, message):
        try:
            await client.send_video(
                chat_id=user_id,
                video=int(TUTORIAL_VIDEO_ID),  # Ensure it's an integer
                caption="Here's the tutorial video!",
            )
        except MessageNotModified:
            print("Tutorial video likely already sent (previous attempt).")
        except Exception as e:
            await message.reply_text(f"Error sending tutorial: {e}")
            # Don't return; we want to send force-sub message too

        # Send force subscription message (unsubscribed users)
        buttons = [
            [
                InlineKeyboardButton(text="Join Channel 1", url=client.invitelink),
                InlineKeyboardButton(text="Join Channel 2", url=client.invitelink2),
            ],
            [
                InlineKeyboardButton(
                    text='Try Again Now🥰',
                    callback_data="try_again"  # Use callback data
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
        return  # IMPORTANT: Return after force-sub + tutorial (if not subscribed)


    # --- User IS Subscribed: Original logic ---
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass

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
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
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
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

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
        return  # Return after sending files

    else:  # plain /start
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
        return
    
@Bot.on_callback_query(filters.regex(r"^try_again$"))
async def try_again_callback(client: Client, callback_query: CallbackQuery):
    """Handles the 'Try Again' callback query."""
    if await subscribed(client, callback_query):
        await callback_query.answer("Subscribed! Now processing...", show_alert=True)
        await handle_file_request(client, callback_query)
    else:
        await callback_query.answer("You still need to subscribe.", show_alert=True)


async def handle_file_request(client: Client, callback_query: CallbackQuery):
    """Handles file request after 'Try Again'."""
    original_start_command = callback_query.message.reply_to_message.text if callback_query.message.reply_to_message else None

    if original_start_command and len(original_start_command) > 7:
        try:
            base64_string = original_start_command.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")

            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else [i for i in range(start, end -1, -1)]
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            else:
                return
        except Exception as e:
            print(f"Decoding error: {e}")
            return

        temp_msg = await callback_query.message.reply("Wait...")
        try:
            messages = await get_messages(client, ids)
            await temp_msg.delete()
            for msg in messages:
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(
                    msg.document) else ("" if not msg.caption else msg.caption.html)
                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

                try:
                    await msg.copy(chat_id=callback_query.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                   reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(chat_id=callback_query.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                   reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except Exception as e:
                    print(f"Copy error: {e}")
                    pass
                return

        except Exception as e:
            await callback_query.message.reply_text("Error!")
            print(f"Get messages error: {e}")
            return
    else:
        # Handle plain /start
        reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡️ ᴀʙᴏᴜᴛ", callback_data = "about"),
                InlineKeyboardButton('🍁 𝕚𝔹𝕆𝕏 𝕋𝕍', url='https://t.me/iBOX_TV')
            ]
        ]
        )
        await callback_query.message.reply_text(text=START_MSG.format(
                first=callback_query.from_user.first_name,
                last=callback_query.from_user.last_name,
                username=None if not callback_query.from_user.username else '@' + callback_query.from_user.username,
                mention=callback_query.from_user.mention,
                id=callback_query.from_user.id  # Use callback_query.from_user.id here
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True)
        return
#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
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
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
