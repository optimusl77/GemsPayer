# Discord Gems Bot

## 📌 Overview
This is a **Discord bot** designed to automate gem balance checking and payments on TrySMP (Trymp.net). The bot periodically retrieves gem balances and automatically transfers them when detected. It also includes useful server commands like channel management and interval settings.

## 🚀 Features
- **Automatic gem balance checking** (`/gems balance`)
- **Auto-payment of gems** when detected
- **Channel registration** for automated monitoring (`!setchannel`)
- **Customizable interval** for balance checks (`!time`)
- **List registered channels** (`!listchannels`)
- **Prevent self-triggering** to avoid infinite loops

## 🛠️ Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/your-repo/discord-gems-bot.git
cd discord-gems-bot
```

### **2. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3. Configure Your Bot**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new bot and get the **TOKEN**
3. Replace the `TOKEN` in `bot.py`

### **4. Run the Bot**
```sh
python bot.py
```


## 🔄 Auto-Restart on Disconnect
To keep the bot online 24/7, consider running it with a process manager like **PM2**:
```sh
pm2 start bot.py --name "GemsBot" --interpreter python3
```

## 📌 Notes
- The bot **ignores messages** that contain `You have sent` to prevent infinite payment loops.
- Only channels **added with `!setchannel add`** will receive `/gems balance` requests.
- The interval for gem checking is **60 seconds by default**, but can be changed with `!time`.

## 📞 Support
If you encounter any issues, feel free to open an issue on the GitHub repository or contact me over Discord (optimuscraft_).

---
**Developed by Lean** 🎮
