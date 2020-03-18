import asyncio
import websockets

async def client_requests():
	async with websockets.connect("ws://localhost:1234", ping_interval=1000) as socket:
		FirstIteration = True
		while True:
			try:
				start_message = await socket.recv() if FirstIteration else None
				if start_message:
					print(start_message)
				if FirstIteration and start_message == "Try Later Coffee Machine Is Used Now" :
					await socket.close()
					return
				FirstIteration = False

				msg = input("Send message: ")
				await socket.send(msg)
				result = await socket.recv()
				if result == "Try Later":
					print("Sorry Coffee Machine is used now try later")
					await socket.close()
					return
				elif result == "Thanks for order":
					print("System says Thanks for order")
					await socket.close()
					return
				print(result)
			except Exception as E:
				print("reconnect...")
				socket = await websockets.connect("ws://localhost:1234", ping_interval=1000)

asyncio.get_event_loop().run_until_complete(client_requests())