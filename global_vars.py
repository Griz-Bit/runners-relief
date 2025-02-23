# directory of reference data
CHROMA_PATH = "chroma_db"

# directory of embedded data for retrieval
DATA_DIR = "data"

# prompt template to generate chat response
PROMPT_TEMPLATE_QUERY = """
Identify the injury of the user, not more than one, and give information on its causes and/or remedies in bullet points. Be friendly to the user and use phrases like "it could be" to indicate that you aren't a medical professional. Answer based on the following contextual information:

{context}

---

Here is the previous history of the conversation:

{history}

---

Identify the injury of the user, not more than one, and give information on its causes and/or remedies in bullet points. Be friendly to the user and use phrases like "it could be" to indicate that you aren't a medical professional. Answer based on the above contextual information and the following prompt: {query}

---

If you are unsure between multiple injuries, you can ask clarifying questions to narrow down the possibilities.
If you do not know the answer to any question, simply respond with "I am not sure. This is not something I was trained on."
"""

# prompt template to generate name of injury and its confidence score based on given details
PROMPT_TEMPLATE_DIAGNOSIS = """
Identify the potential injuries of the user, limit it to 2. However, it should be limited to 1 if accuracy is 100 for any injury. Respond in one or two words with only the name of the injury and an accuracy percentage from 0 to 100 in only numbers without the percentage sign for each and a "++" between the name of the injury and the number, with 100 being absolute guarantee. If you choose 100 for any injury, then limit the quantity of injuries to 1. Make sure to add a "--" to seperate each injury if you use more than one, based on the following contextual information:

{context}

---

Here is the previous history of the conversation. Make sure to diagnose injuries based on the latest statement made by the assistant. Make sure to focus particularly on the past 1 or 2 conversations if they are present:

{history}

---

Identify the potential injuries of the user, limit it to 2 but it should be 1 if accuracy is 100 for the first one, and respond in one or two words with only the name of the injury and an accuracy percentage from 0 to 100 in only numbers without the percentage sign for each and a "++" between the name of the injury and the number, with 100 being absolute guarantee. If you choose 100 for any injury, then limit the quantity of injuries to 1. Make sure to add a "--" to seperate each injury if you use more than one, based on the above contextual information and the following prompt: {query}

---

A sample response would be "Stress Fracture ++ 94 -- Shin Splints ++ 83". If you decide that 100 is the relevant score for any injury, limit the quantity to 1. An example of this would be "Runner's Knee ++ 100".

---

If you do not know the answer to any question, simply respond with "Not Sure 0". AND, stress fractures are not the same as shin splints, so make sure to reference the history correctly.
"""