import response_driver.response_driver.topics as topics
import response_driver.response_driver.funfacts as funFacts
import response_driver.response_driver.jokes as jokes
import response_driver.response_driver.config as response_config
import os
import sys
import signal
import pika
import random
import librosa
import asyncio
import aio_pika
from invoke import run


async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        response_queue = await channel.declare_queue("response", auto_delete=False)
        
        async def publish(message, routing_key):
            print("Response: message sent! " + message)
            await channel.default_exchange.publish(aio_pika.Message(body=message.encode()), routing_key=routing_key)
            return

        async def think(query):
            foundIntent = await findIntent(query)
            intent = foundIntent["intent"]
            shouldReply = foundIntent["responseWanted"]
            topic = foundIntent["topic"]
            if shouldReply == True:
                response = await respond(intent, topic, query)
                reply = "speak:::" + response
                await publish(reply, "hub")
                if topic != "unknown":
                    return True
                else:
                    return False
            else:
                if intent == "sleep" or intent == "nod" or intent == "shake" or intent == "laugh":
                    reply = "move:::" + intent
                    await publish(reply, "hub")
                    return True
                else:
                    await publish("move:::rest", "hub")
                    await publish("unpause", "hub")
                    print("Ik heb je niet goed verstaan. Probeer het nog eens.")


        def run_command_sync(command):
            run(command, hide=True, warn=True)

        async def findIntent(text):
            """
            This method finds the intent of the user depending on what they said.
            """
            if response_config.responseGenerator != "custom":
                return {"intent": "response", "responseWanted": True, "topic": None}
            if response_config.speechRecognizer != "witAI":
                for tw in response_config.jobTriggerWords:
                    if tw in text:
                        return {"intent": "job", "responseWanted": True, "topic": None}
                for tw in response_config.funFactTriggerWords:
                    if tw in text:
                        return {"intent": "funfact", "responseWanted": True, "topic": None}
                afterOver = text.split("over")
                for tw in response_config.informTriggerWords:
                    if tw in text:
                        for topic in topics.topics:
                            for topicTw in topic["triggerWords"]:
                                if len(afterOver) > 1:
                                    if topicTw in afterOver[1]:
                                        return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                                if topicTw in text:
                                    return {"intent": "inform", "responseWanted": True, "topic":topic["topic"]}
                        return {"intent": "inform", "responseWanted": True, "topic": "unknown"}
                for tw in response_config.jokeTriggerWords:
                    if tw in text:
                        return {"intent": "joke", "responseWanted": True, "topic": None}
                for tw in response_config.laughTriggerWords:
                    if tw in text:
                        return {"intent": "laugh", "responseWanted": False, "topic": None}
                for tw in response_config.nodTriggerWords:
                    if tw in text:
                        return {"intent": "nod", "responseWanted": False, "topic": None}
                for tw in response_config.shakeTriggerWords:
                    if tw in text:
                        return {"intent": "shake", "responseWanted": False, "topic": None}
                for tw in response_config.sleepTriggerWords:
                    if tw in text:
                        return {"intent": "sleep", "responseWanted": False, "topic": None}
                return {"intent": "unknown", "responseWanted": False, "topic": None}
                        
                        
        async def respond(intent, topic, text):
            """This method generates a response, depending on response_config.responseGenerator, which defaults to custom. Most of the alternatives have not been implemented yet."""
            if response_config.responseGenerator == "custom":
                if intent == "job":
                    return "We zijn altijd op zoek naar collegaas, en hoewel ik je zelf niet iets aan kan bieden verwijs ik je graag door naar de mensen die me vandaag hebben meegenomen"
                if intent == "inform":
                    if topic == "unknown":
                        subject = list(text.split(" "))
                        print(subject[-1])
                        return "Ik hoor dat je over " + subject[-1] + " geïnformeerd wil worden, maar ik heb daar geen kennis over."
                    else:
                        return topics.information[topic]
                elif intent == "joke":
                    random.seed(time.time())
                    return random.choice(jokes)
                elif intent == "funfact":
                    random.seed(time.time())
                    fact = random.choice(funFacts)
                    return "Wist je dat " + fact
            else:
                if response_config.responseGenerator == "fietje":
                    command = "echo " + text + " in zinnen van minimaal 10 en maximaal 20 woorden " + " | ollama run bramvanroy/fietje-2b-chat:Q3_K_M > output.txt"
                elif response_config.responseGenerator == "llama":
                    command = "echo " + text + " | ollama run llama3 > output.txt"
                elif response_config.responseGenerator == "geitje":
                    command = "echo " + text + " | ollama run bramvanroy/geitje-7b-ultra-gguf > output.txt"
                await asyncio.to_thread(run_command_sync, command)
                file = file = open("output.txt", "r")
                text = file.read()
                file.close()
                return text

        async def callback(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process(ignore_processed=True):
                await message.ack()
                print("Response: Message received: " + message.body.decode())
                instructions = message.body.decode().split(":::")
                if instructions[0] == "respond":
                    intent = await findIntent(instructions[1])
                    
                    awake = True
                elif instructions[0] == "respondWit":
                    details = instructions[1].split("***")
                    intent = details[0]
                    shouldRespond = details[1]
                    topic = details[2]
                    text = details[3]
                    if shouldRespond != "False":
                        response = await respond(intent, topic, text)
                        reply = "
                        publish
                    

        await response_queue.consume(callback)
        try:
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)