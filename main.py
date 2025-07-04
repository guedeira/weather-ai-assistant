# main.py
import json
from src.clients.openai_client import OpenAIClient
from src.clients.weather_client import WeatherClient
from src.config.settings import DEBUG

def main():
    ai_client = OpenAIClient()
    weather_client = WeatherClient()

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a specific city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city name, e.g., São Paulo",
                        },
                    },
                    "required": ["city"],
                },
            },
        }
    ]

    print('Assistente de Clima (digite "/sair" ou pressione Ctrl+C para encerrar)\n')

    try:
        while True:
            user_input = input('Você: ')
            if user_input.lower() == '/sair':
                print('Até logo!')
                break

            messages = [
                {
                    "role": "system",
                    "content": """
                    You are a weather assistant that speaks in Brazilian Portuguese.
                    Your goal is to provide temperature, weather conditions, and make a useful recommendation.
                    Recommend warm clothing if the temperature is below 15°C.
                    Recommend taking an umbrella if there is rain in the weather description.
                    Always provide temperature in degrees Celsius.
                    """
                },
                {"role": "user", "content": user_input}
            ]

            response = ai_client.create_chat_completion(messages, tools=tools, tool_choice="auto")

            if not response:
                print("\nAssistente: Desculpe, não consegui processar sua solicitação.")
                continue

            response_message = response.choices[0].message

            if response_message.tool_calls:
                if DEBUG:
                    print(f"\n[DEBUG] Model wants to call a tool: {response_message.tool_calls[0].function.name}")
                    print(f"[DEBUG] Arguments: {response_message.tool_calls[0].function.arguments}")

                messages.append(response_message)
                available_functions = {"get_weather": weather_client.get_weather}

                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions.get(function_name)
                    if function_to_call:
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(city=function_args.get("city"))
                        
                        if DEBUG:
                            print(f"[DEBUG] Tool response: {json.dumps(function_response, ensure_ascii=False)}")

                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": json.dumps(function_response, ensure_ascii=False),
                            }
                        )
                    else:
                        print(f"Error: Function {function_name} not found.")

                final_response = ai_client.create_chat_completion(messages)
                if final_response:
                    print(f'\nAssistente: {final_response.choices[0].message.content.strip()}\n')
                else:
                    print('\nAssistente: Não consegui processar os dados do clima.\n')
            else:
                print(f'\nAssistente: {response_message.content.strip()}\n')
    except KeyboardInterrupt:
        print("\n\nAté logo!")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")


if __name__ == '__main__':
    main()
