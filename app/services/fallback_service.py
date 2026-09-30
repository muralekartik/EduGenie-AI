def answer_question(question: str, context: str = ""):
    return {
        "answer": (
            f"Machine learning is a branch of Artificial Intelligence "
            f"that enables computers to learn patterns from data and make "
            f"predictions or decisions without being explicitly programmed "
            f"for every task.\n\n"
            f"Your question was: {question}\n\n"
            f"Example: A recommendation system can learn from a user's "
            f"previous activity and suggest movies or products."
        ),
        "source": "EduGenie AI Learning Engine",
    }


def explain_topic(topic: str, level: str = "beginner"):
    return {
        "topic": topic,
        "level": level,
        "explanation": (
            f"{topic} is an important concept. "
            f"It can be understood by learning its basic definition, "
            f"main concepts, and practical applications."
        ),
        "key_points": [
            f"Understand the fundamentals of {topic}.",
            f"Learn the important concepts and terminology.",
            f"Practice {topic} using examples and exercises.",
        ],
        "source": "EduGenie AI Learning Engine",
    }


def summarize_text(text: str, length: str = "medium"):
    words = text.split()

    limits = {
        "short": 30,
        "medium": 60,
        "detailed": 100,
    }

    summary = " ".join(words[:limits.get(length, 60)])

    return {
        "summary": summary,
        "length": length,
        "source": "EduGenie AI Learning Engine",
    }


def generate_quiz(topic: str, difficulty: str = "medium"):
    return {
        "topic": topic,
        "difficulty": difficulty,
        "quiz": [
            {
                "question": f"What is an important part of learning {topic}?",
                "options": [
                    "Understanding fundamentals",
                    "Avoiding practice",
                    "Ignoring examples",
                    "Skipping concepts",
                ],
                "answer": "Understanding fundamentals",
                "explanation": f"Understanding the fundamentals of {topic} builds a strong foundation.",
            },
            {
                "question": f"Which approach helps improve knowledge of {topic}?",
                "options": [
                    "Regular practice",
                    "Never revising",
                    "Avoiding problems",
                    "Ignoring feedback",
                ],
                "answer": "Regular practice",
                "explanation": "Regular practice improves understanding and problem-solving ability.",
            },
            {
                "question": f"What is useful when studying {topic}?",
                "options": [
                    "Practical examples",
                    "Guessing answers",
                    "Skipping basics",
                    "Avoiding questions",
                ],
                "answer": "Practical examples",
                "explanation": "Practical examples help connect theory with real-world applications.",
            },
        ],
        "source": "EduGenie AI Learning Engine",
    }


def get_recommendations(topic: str = ""):
    topic = topic.strip() or "your current subject"

    return {
        "topic": topic,
        "recommendations": [
            {
                "title": "Review the fundamentals",
                "description": f"Revise the core concepts of {topic}.",
                "action": "Review",
            },
            {
                "title": "Practice with examples",
                "description": f"Solve practical problems related to {topic}.",
                "action": "Practice",
            },
            {
                "title": "Test your knowledge",
                "description": f"Take a quiz to evaluate your understanding of {topic}.",
                "action": "Quiz",
            },
        ],
        "source": "EduGenie AI Learning Engine",
    }