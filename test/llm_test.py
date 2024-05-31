import ollama
response = ollama.chat(model="bramvanroy/fietje-2b-chat", messages=[
        {
            "role":"system",
            "content":"Je bent een robot genaamd Melvin, en je representeerd Ordina op een ICT-conferentie. Bezoekers gaan tegen je praten, en jij praat terug. Je zinnen moeten ten minste 10 woorden lang zijn.",
        },
        {
            "role":"user",
            "content":"Hoi, wie zijn jullie en wat hebben jullie te bieden?",
        },
    ])
print(response["message"]["content"])