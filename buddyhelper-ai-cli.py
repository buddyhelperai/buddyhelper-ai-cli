import os
import json
import sys
import subprocess
import readline

import openai #main chat

def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def update_config(filename, config):
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

def create_directory(dir_name):
    os.makedirs(dir_name, exist_ok=True)

def write_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def replace_query_command(content, howto):
    # Identifies the line containing the query command
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "response = query_engine.query(" in line:
            # lines[i] = f'response = query_engine.query("{howto}")'
            break
    return '\n'.join(lines)

def main():
    config_file = "helper-tmpl.json"
    config = load_config(config_file)

    while True:
        cmd = input("Enter your command: ")
        cmd_parts = cmd.split()

        if cmd_parts[0] == "create" and cmd_parts[1] in config.keys():
            original_howto = config[cmd_parts[1]]['howto']
            user_input_howto = input(f"Enter 'howto' value (suggestion: {original_howto}): ")
            new_howto = original_howto if user_input_howto.strip() == "" else original_howto + " " + user_input_howto

            original_data = config[cmd_parts[1]]['data']
            user_input_data = input(f"Enter 'data' value (suggestion: {original_data}): ")
            new_data = original_data if user_input_data.strip() == "" else original_data + " " + user_input_data

            name = cmd_parts[2]
            
            config[name] = {
                'howto': new_howto,
                'data': new_data,
                'path': 'tmpl/' + name + '.py'
            }

            dir_name = name + '/data'
            create_directory(dir_name)

            write_file(dir_name + '/data', new_data)
            write_file(dir_name + '/howto', new_howto)

            # Copying and modifying the template main.py file
            with open('tmpl/' + config[cmd_parts[1]]['path'] + '.py', 'r') as f:
                main_py_content = f.read()
            new_main_py_content = replace_query_command(main_py_content, new_howto)
            write_file(name + '/main.py', new_main_py_content)

            update_config(config_file, config)

        elif cmd_parts[0] == "get":
            helper_name = cmd_parts[1]
            if helper_name in config.keys():
                print(f"Details for '{helper_name}':")
                print(f"howto: {config[helper_name]['howto']}")
                print(f"data: {config[helper_name]['data']}")
                print(f"path: {config[helper_name]['path']}")
            else:
                print(f"No details found for '{helper_name}'")

        elif cmd_parts[0] == "use":
            helper_name = cmd_parts[1]
            script_path = helper_name + "/main.py"

            if not os.path.exists(script_path):
                print(f"No main.py found for '{helper_name}'")
                continue

            action = input("Choose an action: (1) view, (2) change, (3) run: ")

            if action == "1": #view
                print(f"Details for '{helper_name}':")
                print(f"howto: {config[helper_name]['howto']}")
                print(f"data: {config[helper_name]['data']}")
                print(f"path: {config[helper_name]['path']}")

            
            elif action == "2": #change
                original_howto = config[helper_name]['howto']
                readline.set_startup_hook(lambda: readline.insert_text(original_howto))
                user_input_howto = input("Enter new 'howto' value: ")
                new_howto = original_howto if user_input_howto.strip() == "" else user_input_howto

                original_data = config[helper_name]['data']
                readline.set_startup_hook(lambda: readline.insert_text(original_data))
                user_input_data = input("Enter new 'data' value: ")
                new_data = original_data if user_input_data.strip() == "" else user_input_data

                readline.set_startup_hook()  # reset the hook

                # Update the config with the new values
                config[helper_name]['howto'] = new_howto
                config[helper_name]['data'] = new_data

                # Save the updated config back to the file
                with open("helper-tmpl.json", "w") as json_file:
                    json.dump(config, json_file, indent=4)

            elif action == "3": #run
                result = subprocess.run(f"cd {helper_name} && python3 main.py", shell=True, capture_output=True, text=True)
                print(result.stdout)

        else:
            with open("config.json") as file:
                config_data = json.load(file)

            openai.api_key = config_data["api_keys"]["open_ai"]
  
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
            ]

            while True:
                user_input = input("User: ")
                if user_input == "chat reset":
                    conversation = [
                        {"role": "system", "content": "You are a helpful assistant."},
                    ]
                    continue

                conversation.append({"role": "user", "content": user_input})

                response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=conversation
                )

                if 'content' in response['choices'][0]['message']:
                    assistant_response = response['choices'][0]['message']['content']
                else:
                    assistant_response = "Error: try again"

                print("Assistant: ", assistant_response)

                conversation.append({"role": "assistant", "content": assistant_response})
                
            print("Command not found.")

if __name__ == "__main__":
    main()
