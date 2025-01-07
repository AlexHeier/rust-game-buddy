import asyncio
import json
import math

from enum import Enum
from typing import Dict
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand, Emoji

def load_servers_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

class MarkerType(Enum):
    Explosion = 2
    CH47 = 4
    CargoShip = 5
    Crate = 6
    PatrolHelicopter = 8

async def convert_to_grid(x_coord, y_coord, socket):
    map = await socket.get_map(False, False, False, False, dict, False)

    cell_size = map.size[0] / 25

    col_index = x_coord / cell_size
    row_index = y_coord / cell_size

    col_letter = chr(int(col_index) + ord('A'))

    row_number = 25 - row_index
    
    return f"{col_letter}{int(row_number)}"

async def getmarkers(old_markers, socket):
    new_markers = []
    markers = await socket.get_markers()
    
    for marker in markers:
        if marker.type in MarkerType._value2member_map_:
            new_markers.append(marker)

    for new_marker in new_markers:
        if new_marker not in old_markers:
            coordinates = await convert_to_grid(new_marker.x, new_marker.y, socket)
            await socket.send_team_message(f"{MarkerType(new_marker.type).name} appeared @ {coordinates}")
        
    return new_markers

async def playerStatus(socket, previous_state):
    # Fetch the latest team info
    team_info = await socket.get_team_info()  # Assuming this is an async call

    # Iterate over each player in the team
    for member in team_info.members:
        player_id = member.steam_id
        current_state = {
            "is_online": member.is_online,
            "is_alive": member.is_alive,
            "x": member.x,
            "y": member.y,
            "death_time": member.death_time,
        }

        # Check if the player has changed online status
        if player_id in previous_state:
            prev_state = previous_state[player_id]
            
            # Check for online/offline status change
            if prev_state["is_online"] != current_state["is_online"]:
                if current_state["is_online"]:
                    await socket.send_team_message(f"Welcome back {member.name} {Emoji.COOL}")
                else:
                    await socket.send_team_message(f"{member.name} went offline! {Emoji.SKULL}")

            # Check if the player died
            if prev_state["is_alive"] != current_state["is_alive"] and not current_state["is_alive"]:
                coordinates = await convert_to_grid(member.x, member.y, socket)
                await socket.send_team_message(f"{Emoji.EYES} {member.name} died @ {coordinates} {Emoji.EXCLAMATION}")
        
        # Update the previous state
        previous_state[player_id] = current_state

    return previous_state

async def connect_server(server_ip, server_port, player_id, player_token):
    options = CommandOptions(prefix="!")
    server_details = ServerDetails(server_ip, server_port, player_id, player_token)
    socket = RustSocket(server_details, command_options=options)
    await socket.connect()

    @Command(server_details)
    async def hi(command: ChatCommand):
        await socket.send_team_message(f"Hi, {command.sender_name}!")

    @Command(server_details)
    async def time(command: ChatCommand):
        time = await socket.get_time()
        await socket.send_team_message(f"The time is {time.time}.")

    @Command(server_details)
    async def daylength(command: ChatCommand):
        time = await socket.get_time()
        await socket.send_team_message(f"The day length is {int(time.day_length)} minutes.")

    @Command(server_details)
    async def commands(command: ChatCommand):
        await socket.send_team_message("!commands, !time, !daylength, !hi, !create, !pop")
    
    @Command(server_details)
    async def pop(command: ChatCommand):
        info = await socket.get_info()
        await socket.send_team_message(f"{info.players} Online - {info.queued_players} in Queue.")

    @Command(server_details)
    async def create(command: ChatCommand):
        await socket.send_team_message("Creating timer for 15min")
        await asyncio.sleep(300)
        await socket.send_team_message("10 min")
        await asyncio.sleep(300)
        await socket.send_team_message("5 min")
        await asyncio.sleep(60)
        await socket.send_team_message("4 min")
        await asyncio.sleep(60)
        await socket.send_team_message("3 min")
        await asyncio.sleep(60)
        await socket.send_team_message("2 min")
        await asyncio.sleep(60)
        await socket.send_team_message("1 min")
        await asyncio.sleep(30)
        await socket.send_team_message("30 sec")
        await asyncio.sleep(10)
        await socket.send_team_message("20 sec")
        await asyncio.sleep(10)
        await socket.send_team_message("10 sec")
        await asyncio.sleep(5)
        await socket.send_team_message("5 sec")
        await asyncio.sleep(1)
        await socket.send_team_message("4 sec")
        await asyncio.sleep(1)
        await socket.send_team_message("3 sec")
        await asyncio.sleep(1)
        await socket.send_team_message("2 sec")
        await asyncio.sleep(1)
        await socket.send_team_message("1 sec")
        await asyncio.sleep(1)
        await socket.send_team_message("ITS READY!!!")

    # Initialize previous_state as a dictionary using player steam_id as keys
    state = await socket.get_team_info()
    previous_state = {member.steam_id: {
        "is_online": member.is_online,
        "is_alive": member.is_alive,
        "x": member.x,
        "y": member.y,
        "death_time": member.death_time,
    } for member in state.members}
    
    old_markers = []
    try:
        while True:
            previous_state = await playerStatus(socket, previous_state)
            old_markers= await getmarkers(old_markers, socket)
            await asyncio.sleep(2)

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