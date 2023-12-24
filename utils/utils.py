from moodtracker.lexicon.lexicon_en import moods_dict
from moodtracker.models.models import User, Mood
from moodtracker.bot import session

happy_sub_moods = ['Playful 😉', 'Content 😌', 'Interested 🤓', 'Proud 🥹', 'Accepted 🤗', 'Powerful 🔋',
                   'Peaceful ☮️', 'Trusting 🤫', 'Optimistic 🍀']
sad_sub_moods = ['Lonely 😪', 'Vulnerable 💔', 'Despair 😩', 'Guilty 🥶', 'Depressed 😞', 'Hurt 🤕']
angry_sub_moods = ['Let Down 😒', 'Humiliated 🫥', 'Bitter 😠', 'Mad 🤬', 'Aggressive 👊', 'Frustrated 😖',
                   'Distant 🧟', 'Critical 🤔']
surprised_sub_moods = ['Startled 😧', 'Confused 🤷🏻\u200d♀️', 'Amazed 😻', 'Excited 🥳']
fearful_sub_moods = ['Scared 🙀', 'Anxious 😰', 'Insecure 😕', 'Weak 🌱', 'Rejected 🪁', 'Threatened 💣']
bad_sub_moods = ['Bored 🥱', 'Busy 📆', 'Stressed 😫', 'Tired 💤']
disgusted_sub_moods = ['Disapproving 😮\u200d💨', 'Disappointed 🫠', 'Awful 🤢', 'Repelled 😤']

# for main_mood, main_data in moods_dict.items():
#     for sub_mood, sub_data in main_data["sub_moods"].items():
#         happy_sub_moods.append(sub_data["label"])
#
# print(happy_sub_moods)


# get or create a user
def get_or_create_user(user_id, username):
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()
    return user
