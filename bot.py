import os
from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyrogram.utils
import pyromod

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            PORT = int(os.environ.get("PORT", 8000))  # Use port 8000 or env PORT
            await web.TCPSite(app, "0.0.0.0", PORT).start()
        print(f"Ara ara~ {me.first_name} has awakened... Mmm, I'm all hot and ready to hunt... ✨️")
        for id in Config.ADMIN:
            try: 
                await self.send_message(id, f"**Mmm~ {me.first_name} is up and dripping with anticipation... Ready to make things messy, darling~?**")                                
            except Exception as e:
                print(f"Oho~ I tried to moan into admin {id}’s ear, but something got in the way... Kinky error: {e}")
        
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**Mmm~ {me.mention} just got turned on all over again... Ready for round two, darling?**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")                                
            except Exception as e:
                print(f"Ara~ I tried to moan into LOG_CHANNEL, but something naughty got in the way... Error: {e}")

    async def stop(self):
        await super().stop()
        print(f"{self.mention} is stopped.")

Bot().run()
