import re

COMMANDS = {

    "/start": "Start Mood Tracker Journal bot",

    "/help": "See available commands",

    "/log": "Log today's mood",

    "/graph": "View your mood graph",

    }

LEXICON_EN = {
    "/start": "🌈 <b>Welcome to Mood Tracker Journal - Your Personal Mood Tracker!</b>"
              "\n\n"
              "Hey there! I'm here to help you keep track of your moods and emotions. "
              "Whether you're feeling ecstatic, stressed, or somewhere in between, I'm here to listen. 🤖✨\n"
              "\n\n"
              "To get started, tell me how you're feeling today, and I'll log it for you."
              ,

    "/help": "🤖 <b>Mood Tracker Journal - Help Center</b> \n"
             "Welcome to the help center! Here are some commands you can use:\n\n"
             "<b>/start</b> - Start Mood Tracker Journal bot\n"
             "<b>/log</b> - Log your current mood\n"
             "<b>/help</b> - See available commands\n"
             "<b>/graph</b> - View your mood graph\n\n"
             "Remember, I'm here to assist you on your wellness journey. Let's make every mood count! 😊🌈",

    "/log": "Tell me how you're feeling today, and I'll log it for you 🪁",

    "/graph": "View your mood graph 👾",

    "log_button": "Log today's mood 🌙",
    "refuse_button": "I don't want to log my mood today 🌥️",

    "user_refuse": "I understand and respect your wish not to share your mood log today 🦋"
                   "See you tomorrow!",
    "start_day_type": "Let's start by grading your day overall 🫧",

    "specify_emotion": "Choose one of the following shades of emotions to specify how you feel 💫",

    "respond_to_log": "Thank you for logging your emotions 🌈",

    "note_button": "Do you want to add a short note to remember this day? 📓",
    "note_accept": "Leave a short note to describe what happened today 📝",
    "note_refuse": "It's okay not to leave a note! 🌙"

    }

day_types = {
    "excellent": {
        "label": "Excellent! 🎉",
        "quantity": 18
        },

    "good": {
        "label": "Good 😻",
        "quantity": 9
        },

    "normal": {
        "label": "Normal 🤷🏻‍♀️",
        "quantity": 4
        },

    "bad": {
        "label": "Bad 🙅🏻‍♀",
        "quantity": 1
        }
    }

moods_dict = {
    # happy
    "happy": {
        "label": "Happy 🥳",
        "description": "Feeling joy and celebration.",
        "sub_moods": {
            # Sub-emotions related to happiness
            "playful": {
                "label": "Playful 😉",
                "description": "In a light-hearted and fun mood.",
                },
            "content": {
                "label": "Content 😌",
                "description": "Feeling satisfied and at ease.",
                },
            "interested": {
                "label": "Interested 🤓",
                "description": "Curious and engaged in something.",
                },
            "proud": {
                "label": "Proud 🥹",
                "description": "Feeling a sense of achievement or accomplishment.",
                },
            "accepted": {
                "label": "Accepted 🤗",
                "description": "Feeling acknowledged and welcomed.",
                },
            "powerful": {
                "label": "Powerful 🔋",
                "description": "Feeling strong and capable.",
                },
            "peaceful": {
                "label": "Peaceful ☮️",
                "description": "Tranquil and calm.",
                },
            "trusting": {
                "label": "Trusting 🤫",
                "description": "Having confidence in others.",
                },
            "optimistic": {
                "label": "Optimistic 🍀",
                "description": "Having a positive outlook on the future.",
                },
            },

        },
    # sad
    "sad": {
        "label": "Sad 😢",
        "description": "Feeling sorrow or unhappiness.",
        "sub_moods": {
            # Sub-emotions related to sadness
            "lonely": {
                "label": "Lonely 😪",
                "description": "Feeling isolated and without companionship.",
                },
            "vulnerable": {
                "label": "Vulnerable 💔",
                "description": "Feeling exposed or susceptible to harm.",
                },
            "despair": {
                "label": "Despair 😩",
                "description": "Experiencing a sense of hopelessness.",
                },
            "guilty": {
                "label": "Guilty 🥶",
                "description": "Feeling responsible for wrongdoing.",
                },
            "depressed": {
                "label": "Depressed 😞",
                "description": "Experiencing a persistent low mood.",
                },
            "hurt": {
                "label": "Hurt 🤕",
                "description": "Feeling emotionally or physically wounded.",
                },
            },

        },
    # angry
    "angry": {
        "label": "Angry 😡",
        "description": "Feeling strong displeasure or hostility.",
        "sub_moods": {
            # Sub-emotions related to anger
            "let_down": {
                "label": "Let Down 😒",
                "description": "Feeling disappointed or betrayed.",
                },
            "humiliated": {
                "label": "Humiliated 🫥",
                "description": "Feeling embarrassed and degraded.",
                },
            "bitter": {
                "label": "Bitter 😠",
                "description": "Feeling resentment or indignation.",
                },
            "mad": {
                "label": "Mad 🤬",
                "description": "Feeling extremely angry or furious.",
                },
            "aggressive": {
                "label": "Aggressive 👊",
                "description": "Inclined to act with hostility.",
                },
            "frustrated": {
                "label": "Frustrated 😖",
                "description": "Feeling thwarted or discouraged.",
                },
            "distant": {
                "label": "Distant 🧟",
                "description": "Emotionally withdrawn or aloof.",
                },
            "critical": {
                "label": "Critical 🤔",
                "description": "Expressing disapproval or judgment.",
                },
            },

        },
    # surprised
    "surprised": {
        "label": "Surprised 😮",
        "description": "Caught off guard or amazed.",
        "sub_moods": {
            # Sub-emotions related to surprise
            "startled": {
                "label": "Startled 😧",
                "description": "Sudden and involuntary reaction.",
                },
            "confused": {
                "label": "Confused 🤷🏻‍♀️",
                "description": "Feeling bewildered or unclear.",
                },
            "amazed": {
                "label": "Amazed 😻",
                "description": "Feeling wonder and astonishment.",
                },
            "excited": {
                "label": "Excited 🥳",
                "description": "Eager and enthusiastic anticipation.",
                },
            },

        },
    # fearful
    "fearful": {
        "label": "Fearful 😨",
        "description": "Feeling afraid or anxious.",
        "sub_moods": {
            # Sub-emotions related to fear
            "scared": {
                "label": "Scared 🙀",
                "description": "Experiencing fear or terror.",
                },
            "anxious": {
                "label": "Anxious 😰",
                "description": "Feeling unease or nervousness.",
                },
            "insecure": {
                "label": "Insecure 😕",
                "description": "Lacking confidence or assurance.",
                },
            "weak": {
                "label": "Weak 🌱",
                "description": "Lacking strength or resilience.",
                },
            "rejected": {
                "label": "Rejected 🪁",
                "description": "Feeling dismissed or excluded.",
                },
            "threatened": {
                "label": "Threatened 💣",
                "description": "Feeling in danger or at risk.",
                },
            },

        },
    # bad
    "bad": {
        "label": "Bad 👎",
        "description": "Negative overall feeling or situation.",
        "sub_moods": {
            # Sub-emotions related to feeling bad
            "bored": {
                "label": "Bored 🥱",
                "description": "Feeling uninterested or weary.",
                },
            "busy": {
                "label": "Busy 📆",
                "description": "Engaged in multiple tasks or activities.",
                },
            "stressed": {
                "label": "Stressed 😫",
                "description": "Feeling overwhelmed or tense.",
                },
            "tired": {
                "label": "Tired 💤",
                "description": "Experiencing fatigue or exhaustion.",
                },
            },
        },

    # disgusted
    "disgusted": {
        "label": "Disgusted 😬",
        "description": "Feeling strong aversion or revulsion.",
        "sub_moods": {
            # Sub-emotions related to disgust
            "disapproving": {
                "label": "Disapproving 😮‍💨",
                "description": "Expressing disapproval or disfavor.",
                },
            "disappointed": {
                "label": "Disappointed 🫠",
                "description": "Feeling let down or unsatisfied.",
                },
            "awful": {
                "label": "Awful 🤢",
                "description": "Extremely unpleasant or repulsive.",
                },
            "repelled": {
                "label": "Repelled 😤",
                "description": "Strongly pushed away or disgusted.",
                },
            },
        },


        }
