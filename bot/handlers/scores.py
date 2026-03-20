"""Handler for /scores command."""


def handle_scores(lab_id: str | None = None) -> str:
    """Handle the /scores command.
    
    Args:
        lab_id: Optional lab identifier to filter scores.
        
    Returns:
        User scores (placeholder for Task 2).
    """
    if lab_id:
        return f"Scores for {lab_id}: 95/100 (placeholder — real data in Task 2)"
    return "Your scores: lab-01: 90, lab-02: 85, lab-03: 92 (placeholder — real data in Task 2)"
