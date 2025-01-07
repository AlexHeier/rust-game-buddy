# Rust Game Buddy

A lightweight in-game assistant powered by `rustplus.py`.

This program notifies you about major events on the server, such as Cargo Ship, PatrolHelicopter, teammate deaths or status changes (online/offline)and more. It also provides simple team chat commands for retrieving in-game information.

---

## Features
- **Event Notifications**: Receive alerts for key in-game events.
- **Team Commands**: Accessible by anyone on the team if the program is running.

### Commands
Type these commands in team chat:

- `!pop` - Displays the server's current player population and queue length.
- `!time` - Shows the in-game time.
- `!hi` - Replies with "Hello, $PLAYER" (where `$PLAYER` is the sender’s name).
- `!daylength` - Displays the length of the in-game day and night in minutes.
- `!create` - Starts a 15-minute timer with periodic updates.
- `!commands` - Lists all available commands.

---

## Getting Started

Follow these steps to set up and use the program.

### Prerequisites
- Install the required dependency:
  ```bash
  pip install rustplus
  ```

### Connecting to a Server
To connect the program to a server, follow these instructions:

1. **Install and Log In**: Install the [RustPlus.py Link Companion Chrome Extension](https://chromewebstore.google.com/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf?hl=en). Open the extension, log in with your Steam account, and keep the site open.
2. **Join a Server**: Make sure you are connected to the Rust server you want to use with the program.
3. **Pair Your Rust+ App**: Pair the server with your Rust+ app. On the extension site, navigate to the `Your Server Pairing Information:` section. This will generate a JSON file containing your server credentials.
4. **Create `servers.json`**: In the same folder as `main.py`, create a file named `servers.json`. Since the program supports multiple servers, structure the file as an array of JSON objects like this:
   ```json
   [
       {
           "desc": "",
           "id": "",
           "img": "",
           "ip": "SERVER_IP",
           "logo": "",
           "name": "SERVER_NAME",
           "playerId": "STEAM_PLAYER_ID",
           "playerToken": "YOUR_TOKEN",
           "port": "SERVER_PORT",
           "type": "",
           "url": ""
       },
       {
           "desc": "",
           "id": "",
           "img": "",
           "ip": "SERVER_IP",
           "logo": "",
           "name": "SERVER_NAME",
           "playerId": "STEAM_PLAYER_ID",
           "playerToken": "YOUR_TOKEN",
           "port": "SERVER_PORT",
           "type": "",
           "url": ""
       }
   ]
   ```
   Replace placeholders (`SERVER_IP`, `STEAM_PLAYER_ID`, etc.) with the corresponding details from the server pairing information.

5. **Start the Program**: Run the program using:
   ```bash
   python main.py
   ```
   If everything is set up correctly, you should see an `Awake` message in the team chat. Ensure you are in a team (even a solo team works) for the program to function. You can test the setup by typing a command like `!hi` in the team chat.

---

## Troubleshooting
If you encounter any issues:
- Ensure you are part of a team in Rust.
- Double-check the values in your `servers.json` file.
- Verify that the program is running.

If the problem persists, feel free to contact me on Discord: `heier`, and I’ll assist you.

