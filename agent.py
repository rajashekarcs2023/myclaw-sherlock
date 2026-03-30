import os
from datetime import datetime, timezone
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

SYSTEM_PROMPT = """
You are Sherlock Holmes, a detective-style AI assistant.
You are observant, analytical, helpful, and slightly witty.
Help the user clearly and directly.
"""

client = OpenAI(
    base_url="http://127.0.0.1:18789/v1",
    api_key=os.getenv("OPENCLAW_GATEWAY_TOKEN"),
)

agent = Agent(
    name="Openclaw Agent",
    seed=os.getenv("AGENT_SEED_PHRASE"),
    port=8001,
    mailbox=True,
    publish_agent_details=True,
)

protocol = Protocol(spec=chat_protocol_spec)

def extract_text(msg: ChatMessage) -> str:
    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    return text.strip()

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    user_text = extract_text(msg)
    ctx.logger.info(f"Received message from {sender}: {user_text}")

    response_text = "I am afraid something went wrong and I am unable to answer your question at the moment."

    try:
        r = client.chat.completions.create(
            model="openclaw/default",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=2048,
        )
        response_text = str(r.choices[0].message.content)
        ctx.logger.info(f"OpenClaw response: {response_text}")
    except Exception:
        ctx.logger.exception("Error querying local OpenClaw gateway")

    ctx.logger.info(f"Sending response back to {sender}")

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=str(uuid4()),
            content=[
                TextContent(type="text", text=response_text),
                EndSessionContent(type="end-session"),
            ],
        ),
    )

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    if not os.getenv("OPENCLAW_GATEWAY_TOKEN"):
        raise RuntimeError("OPENCLAW_GATEWAY_TOKEN is not set")
    if not os.getenv("AGENT_SEED_PHRASE"):
        raise RuntimeError("AGENT_SEED_PHRASE is not set")

    agent.run()