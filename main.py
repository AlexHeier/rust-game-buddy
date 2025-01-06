import asyncio
import os
import json
from rustplus import RustSocket, ServerDetails
from dotenv import load_dotenv

load_dotenv()

def load_servers_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

async def handle_team_chat(socket, last_message):
    teamChat = await socket.get_team_chat()
    if teamChat:
        latest_message = teamChat[-1]
        last_message = await handle_new_message(latest_message, last_message, socket)
    return last_message

async def handle_new_message(latest_message, last_message, socket):
    if latest_message.message != last_message:
        message = latest_message.message

        if message.startswith("!commands"):
            await socket.send_team_message(f"!commands, !time, !daylength")
        
        if message.startswith("!time"):
            time = await socket.get_time()
            await socket.send_team_message(f"The time is {time.time}")
        
        if message.startswith("!daylength"):
            time = await socket.get_time()
            await socket.send_team_message(f"The day length is {time.day_length} min")

        return latest_message.message
    return last_message

async def connect_server(server_ip, server_port, player_id, player_token):
    server_details = ServerDetails(server_ip, server_port, player_id, player_token)
    socket = RustSocket(server_details)
    await socket.connect()

    last_message = None
    try:
        while True:
            last_message = await handle_team_chat(socket, last_message)
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        print("\nShutting down")

    await socket.disconnect()

async def main():
    servers = load_servers_from_json('servers.json')
    tasks = []

    for server in servers:
        server_ip = server['ip']
        server_port = server['port']
        player_id = server['playerId']
        player_token = server['playerToken']
        
        tasks.append(asyncio.create_task(connect_server(server_ip, server_port, player_id, player_token)))
    
    await asyncio.gather(*tasks)

asyncio.run(main())
