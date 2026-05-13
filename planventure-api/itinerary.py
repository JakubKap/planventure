from datetime import datetime
from typing import Optional


def generate_itinerary_template(
    destination: str,
    start_date: str,
    end_date: str
) -> str:
    """Generate a default itinerary template based on trip duration.

    Creates a markdown-formatted itinerary with daily placeholders for
    morning, afternoon, and evening activities.

    Args:
        destination: The trip destination name
        start_date: ISO format start date string (e.g., "2024-07-15T08:00:00Z")
        end_date: ISO format end date string (e.g., "2024-07-22T20:00:00Z")

    Returns:
        Formatted itinerary template as a string with daily structure

    Example:
        >>> itinerary = generate_itinerary_template(
        ...     "Paris, France",
        ...     "2024-07-15T08:00:00Z",
        ...     "2024-07-22T20:00:00Z"
        ... )
        >>> print(itinerary)
        # Paris, France Itinerary
        **Trip Duration:** 7 days
        ...
    """
    try:
        # Parse dates
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))

        # Calculate number of days
        num_days = (end - start).days
        if num_days <= 0:
            num_days = 1

        # Generate template
        lines = [f"# {destination} Itinerary\n"]
        lines.append(f"**Trip Duration:** {num_days} days")
        lines.append(f"**Dates:** {start.strftime('%B %d, %Y')} - {end.strftime('%B %d, %Y')}\n")

        # Create daily placeholders
        for day_num in range(1, num_days + 1):
            if num_days > 1:
                current_date = start + (end - start) * (
                    (day_num - 1) / (num_days - 1)
                )
            else:
                current_date = start

            date_str = current_date.strftime('%B %d')

            lines.append(f"## Day {day_num} - {date_str}")
            lines.append("### Morning")
            lines.append("- Activity or location\n")
            lines.append("### Afternoon")
            lines.append("- Activity or location\n")
            lines.append("### Evening")
            lines.append("- Activity or location\n")

        lines.append("## Notes")
        lines.append("- Add any special notes or important information")
        lines.append("- Include restaurant recommendations")
        lines.append("- Mark unmissable attractions")

        return "\n".join(lines)

    except (ValueError, TypeError, AttributeError):
        # Return a generic template if date parsing fails
        return f"""# {destination} Itinerary

## Day 1
### Morning
- Arrival and check-in

### Afternoon
- Explore local area

### Evening
- Dinner at a local restaurant

## Day 2
### Morning
- Visit main attractions

### Afternoon
- Continue sightseeing

### Evening
- Local experience

## Notes
- Plan your activities
- Add accommodation details
- Include important contacts
- Budget and transportation info"""


def quick_itinerary_template(destination: str, num_days: int = 3) -> str:
    """Generate a quick itinerary template based on number of days.

    Simpler version that doesn't require date parsing.

    Args:
        destination: The trip destination
        num_days: Number of days for the trip (default: 3)

    Returns:
        Simple itinerary template

    Example:
        >>> itinerary = quick_itinerary_template("Barcelona, Spain", 5)
    """
    if num_days <= 0:
        num_days = 1

    lines = [f"# {destination} Itinerary ({num_days} Days)\n"]

    for day_num in range(1, num_days + 1):
        lines.append(f"## Day {day_num}")
        lines.append("### Morning")
        lines.append("- [ ] Activity or location")
        lines.append("### Afternoon")
        lines.append("- [ ] Activity or location")
        lines.append("### Evening")
        lines.append("- [ ] Activity or location\n")

    lines.append("## General Notes")
    lines.append("- Accommodation: ")
    lines.append("- Transportation: ")
    lines.append("- Must-see attractions: ")
    lines.append("- Budget: ")

    return "\n".join(lines)


def default_itinerary_template() -> str:
    """Generate a default itinerary template with placeholder content.

    Creates a basic 3-day itinerary template that can be customized
    for any destination. Includes common sections and placeholders.

    Returns:
        Default itinerary template as a markdown-formatted string

    Example:
        >>> template = default_itinerary_template()
        >>> print(template[:100])
        # Trip Itinerary
        **Destination:** [Enter destination]
        **Trip Duration:** [Enter duration]
    """
    lines = [
        "# Trip Itinerary\n",
        "**Destination:** [Enter destination]",
        "**Trip Duration:** [Enter duration]",
        "**Dates:** [Enter dates]\n",
        "## Day 1 - Arrival Day",
        "### Morning",
        "- [ ] Arrival and check-in at accommodation",
        "- [ ] Settle in and rest if needed\n",
        "### Afternoon",
        "- [ ] Light exploration of local area",
        "- [ ] Visit nearby attractions or markets\n",
        "### Evening",
        "- [ ] Dinner at a local restaurant",
        "- [ ] Evening walk or relax\n",
        "## Day 2 - Main Activities",
        "### Morning",
        "- [ ] Breakfast at accommodation",
        "- [ ] Visit main attraction #1\n",
        "### Afternoon",
        "- [ ] Lunch break",
        "- [ ] Visit main attraction #2\n",
        "### Evening",
        "- [ ] Dinner and local experience",
        "- [ ] Evening entertainment or relaxation\n",
        "## Day 3 - Departure Day",
        "### Morning",
        "- [ ] Final sightseeing or shopping",
        "- [ ] Check out from accommodation\n",
        "### Afternoon",
        "- [ ] Departure activities if time allows",
        "- [ ] Head to airport/train station\n",
        "### Evening",
        "- [ ] Departure\n",
        "## Travel Logistics",
        "- **Transportation:** [Flight/Train/Car details]",
        "- **Accommodation:** [Hotel/Airbnb details]",
        "- **Budget:** [Estimated costs]",
        "- **Documents:** [Passports/Visas/Insurance]",
        "\n## Notes and Tips",
        "- Add any special requirements or preferences",
        "- Include contact information for emergencies",
        "- Note dietary restrictions or accessibility needs",
        "- Add weather considerations and packing tips"
    ]

    return "\n".join(lines)
