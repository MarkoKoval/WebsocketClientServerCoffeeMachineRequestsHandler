import asyncio
import websockets

coffee_names = ["Latte", "Cappuccino", "Mochaccino", "Espresso", "Macchiato"]
coffee_additionals = ["Milk", "Sour", "Cognac"]

USERS = []



async def register(websocket):
	if USERS:
		await websocket.send("Try Later Coffee Machine Is Used Now")
	USERS.append(websocket)
	await websocket.send(possible_coffee_choises())

async def unregister(websocket):
	USERS.remove(websocket)

def possible_coffee_choises():
	coffee_names_ = " ".join([  "{} {}".format(str(c), i) for c, i in enumerate(coffee_names, 1)])
	coffee_additionals_ = " ".join([ "{} {}".format( str(c),i) for c, i in enumerate(coffee_additionals, 1)])
	return "Choose maximum 2 Numbers of Available coffees types {} and Available coffees additionals {}".format( coffee_names_,coffee_additionals_)

async def response(websocket, path):
	await register(websocket)

	async for message in websocket:
		print(f"Message ' {message} ' from the client {websocket}")
		if message == 'Got it':
			await websocket.send("Thanks for order")
			await unregister(websocket)
		try:
			selected_numbers = [ int(x) for x in message.split(' ') ]
			if len(selected_numbers) > 2 or selected_numbers == []:
				await websocket.send(possible_coffee_choises() + "\n Send Correct order format for example - 1 1")
			else:
				result = "Enter Correct Data!"
				global coffee_names
				global coffee_additionals
				if len(selected_numbers) == 1 and selected_numbers[0] < len(coffee_names) + 1:
					result = coffee_names[selected_numbers[0]-1] + " is done send 'Got it' to confirm"
				elif len(selected_numbers) == 2 and selected_numbers[0] < len(coffee_names) + 1 and selected_numbers[1] < len(coffee_additionals) + 1:
					result = coffee_names[selected_numbers[0]-1] + " with " + coffee_additionals[selected_numbers[1]-1]  + " is done send 'Got it' to confirm"
				await websocket.send(result)
		except Exception as E:
			await websocket.send(possible_coffee_choises() + "\n Send Correct order format for example - 1 1")


start_server = websockets.serve(response, 'localhost', 1234,  ping_interval=1000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()