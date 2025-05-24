from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import nest_asyncio
import json
from openai import OpenAI

nest_asyncio.apply()
load_dotenv()

with open("src/keys.json", "r") as f:
    keys = json.load(f)
api_key = keys["open_ai_api"]


client = OpenAI(api_key=api_key)

class MCP_ChatBot:

    def __init__(self):
        self.session: ClientSession = None
        self.available_tools: List[dict] = []

    async def process_query(self, query: str):
        messages = [{'role': 'user', 'content': query}]
        functions = self.available_tools
        process_query = True

        while process_query:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=functions,
                tool_choice="auto",
                max_tokens=2024,
            )

            response_message = response.choices[0].message

            if response_message.content:
                print(response_message.content)

            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    print(f"Calling tool {tool_name} with args {arguments}")

                    # Await async tool call
                    result = await self.session.call_tool(tool_name, arguments=arguments)

                    # Append result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content
                    })
            else:
                process_query = False

    async def chat_loop(self):
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                await self.process_query(query)
                print("\n")

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def connect_to_server_and_run(self):
        server_params = StdioServerParameters(
            command="uv",
            args=["run", "src/research_server.py"],
            env=None,
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                await session.initialize()

                response = await session.list_tools()
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])

                self.available_tools = [{
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                } for tool in tools]

                await self.chat_loop()