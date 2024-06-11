from transformers import pipeline, Conversation
import accelerate
import bitsandbytes

chatbot = pipeline(
    "conversational",
    model="BramVanRoy/fietje-2b-chat",
    device_map="auto"
)

start_messages = [
    {"role": "system", "content": "Je bent een robot genaamd Melvin, en je representeert een student op zijn scriptiezitting. De scriptie gaat over een robot, en jij bent het brein."},
    {"role": "user", "content": "Hoi, kan je iets leuks vertellen tegen de aanwezigen op de scriptiezitting?"}
]
conversation = Conversation(start_messages)
conversation = chatbot(conversation)
response = conversation.messages[-1]["content"]
print(response)
    