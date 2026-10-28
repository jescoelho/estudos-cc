from strands import Agent

print("A:", Agent().tool_names)
print("B:", Agent(load_tools_from_directory=True).tool_names)
