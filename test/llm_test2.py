from transformers import pipeline, Conversation
import accelerate
import bitsandbytes

chatbot = pipeline(
    "conversational",
    model="BramVanRoy/fietje-2b-chat",
    device_map="auto"
)

start_messages = [
    {"role": "system", "content": "Je bent een robot genaamd Melvin, en je representeerd Ordina op een ICT-conferentie. Bezoekers gaan tegen je praten, en jij praat terug. Je zinnen moeten ten minste 10 woorden lang zijn."},
    {"role": "user", "content": "Hoi, wie zijn jullie en wat hebben jullie te bieden?"}
]
conversation = Conversation(start_messages)
conversation = chatbot(conversation)
response = conversation.messages[-1]["content"]
print(response)
    