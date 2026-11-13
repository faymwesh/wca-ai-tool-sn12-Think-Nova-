
# memory.py
# Stores conversation history for the current session.

def create_memory(system_prompt):
    return [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


def add_message(memory, role, content):
    memory.append({
        "role": role,
        "content": content
    })
