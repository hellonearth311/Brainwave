from util.ollamaWrapper import *

install_deps()
while True:
    # for now just do some prompt shit idk
    prompt = input("prompt: ")
    if prompt == "exit":
        break

    print(run_prompt(prompt))
