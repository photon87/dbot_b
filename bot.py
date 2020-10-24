import asyncio
import random
import discord


class MyClient(discord.Client):

    def __init__(self):
        super().__init__()
        self.token = ''
        self.load_token()

        self.server_id = 769190994360533023

        self.commands_string = "```This is a list of commands:\nHello```"

        self.in_contest = False
        self.contest_time_left = -1
        self.contest_time = -1
        self.contest_entries = []

    def load_token(self):
        with open("token.txt", "r") as file:
            self.token = file.readline()

    async def contest(self, message):
        for role in message.author.roles:
            if str(role) == "Admin":
                if self.in_contest:
                    return
                numbers = []
                self.contest_time = -1
                self.contest_time_left = -1
                for word in message.content.split():
                    if word.isdigit():
                        numbers.append(int(word))
                if len(numbers) == 1:
                    self.in_contest = True
                    self.contest_time = numbers[0]
                    await message.channel.send(f"New contest started for the next {self.contest_time} seconds\nType !enter to enter.")
                    self.contest_time_left = self.contest_time
                    while self.contest_time_left > 0:
                        await asyncio.sleep(1)
                        self.contest_time_left -= 1
                        await message.channel.send(f"{self.contest_time_left}")
                    await message.channel.send(f"Time is up! {len(self.contest_entries)} entries.")
                    self.in_contest = False
                    if len(self.contest_entries) > 0:
                        await asyncio.sleep(1)
                        await message.channel.send(f"The winner is , {random.choice(self.contest_entries)}!!")
                    self.contest_entries = []
                    await message.channel.send("Contest is over.")
            else:
                if self.in_contest:
                    await message.channel.send(f"A contest is currently running with {self.contest_time_left} seconds left")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.find("!hello") != -1:
            await message.channel.send("Hi")

        elif message.content.find("!commands") != -1:
            await message.channel.send(self.commands_string)

        elif message.content.find("!enter") != -1:
            if self.in_contest:
                a = message.author.name
                if a not in self.contest_entries:
                    self.contest_entries.append(a)
                    await message.channel.send(f"{a} entered")
                else:
                    await message.channel.send(f"{a} already entered")
            else:
                await message.channel.send("No contest currently running...")

        elif message.content.find("!contest") != -1:
            await self.contest(message)

        elif message.content.find("!mood") != -1:
            moods = ["I'm okay.", "I had a rough day.", "I'm doing great!",
                     "I'm doing fine...", "Try my !roll command", "Just stubbed my toe, but okay."]
            response = random.choice(moods)
            await message.channel.send(response)

        elif message.content.find("!users") != -1:
            id = client.get_guild(self.server_id)
            await message.channel.send(f"# of Members: {id.member_count}")

        elif message.content.find("!list") != -1:
            lst = ""
            for member in client.get_guild(self.server_id).members:
                # yield member
                lst += str(member) + ", "
                await message.channel.send(f"{lst}")

        elif message.content.find("!test") != -1:
            await message.channel.send(f"Testing 1... 2... 3...")

        elif message.content.find("!matt") != -1:
            await message.channel.send(f"MattCam down, please try again later.")

        elif message.content.find("!alert") != -1:
            await message.channel.send(f"This incident has been reported to the authorities.")

        elif message.content.find("!dance") != -1:
            await message.channel.send(file=discord.File('dance.gif'))

        elif message.content.find("!roll") != -1:
            numbers = []
            rand = -1
            for word in message.content.split():
                if word.isdigit():
                    numbers.append(int(word))
            if len(numbers) == 1:
                rand = random.randint(1, numbers[0])
                await message.channel.send(f"You rolled: {rand}")
            elif len(numbers) > 1:
                await message.channel.send(f"Too many numbers!")
            else:
                await message.channel.send(f"Please enter a number with your roll...")


if __name__ == "__main__":
    client = MyClient()
    client.run(client.token)
