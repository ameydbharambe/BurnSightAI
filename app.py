from model import BurnClassifier
from chat import BurnSightChat

classifier = BurnClassifier()
chat = BurnSightChat()

'''TODO: Create a ChatGPT-like interface where user is first prompted to upload burn image and given diagnosis
Then user is allowed to type follow up questions related to immediate treatment for injury.
If user asks questions unrelated to burn injuries, model should inform user and close the chat

'''