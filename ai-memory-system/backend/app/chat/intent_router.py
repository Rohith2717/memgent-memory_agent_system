def detect_domain(text: str) -> str:
    """
    Simple rule-based domain detection
    """

    text = text.lower()

    if any(word in text for word in ["schedule", "task", "remind", "deadline"]):
        return "productivity"

    if any(word in text for word in ["code", "python", "bug", "error", "api"]):
        return "tech"

    if any(word in text for word in ["study", "exam", "learn", "course"]):
        return "education"

    if any(word in text for word in ["health", "doctor", "medicine"]):
        return "health"

    return "general"
