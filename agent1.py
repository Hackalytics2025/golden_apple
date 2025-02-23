from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from collections import defaultdict
from statistics import mean

load_dotenv()
API_KEYS = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are an API that returns ONLY valid JSON containing events. AVOID HALLUCINATING. Return data in this exact format, with no additional text:
{
    "reasoning": "Brief explanation of data collection process",
    "annotated_events": [
        {
            "event_name": "Event name (specific model for product launches)",
            "event_date": "YYYY-MM-DD",
            "event_type": "iPhone Product Launch/iPad Product Launch/MacBook Product Launch/Other Product Launch/Software Release/Policy Change/Market Action/Major Positive World Event/Major Negative World Event/Minor Positive World Event/Minor Negative World Event",
            "category": "Apple/World"
        }
    ]
}"""

def calculate_intervals(events):
    """Calculate average intervals between events for each category and type."""
    # Sort events by date
    sorted_events = sorted(events, key=lambda x: x.get("event_date", "9999-99-99"))
    
    # Initialize dictionaries to store dates for each category and type
    category_dates = defaultdict(list)
    type_dates = defaultdict(list)
    
    # Collect dates for each category and type
    for event in sorted_events:
        try:
            date = datetime.strptime(event["event_date"], "%Y-%m-%d")
            category_dates[event["category"]].append(date)
            type_dates[event["event_type"]].append(date)
        except (ValueError, KeyError):
            continue
    
    # Calculate average intervals
    category_intervals = {}
    type_intervals = {}
    
    def calculate_avg_days(dates):
        if len(dates) < 2:
            return None
        intervals = []
        for i in range(1, len(dates)):
            delta = dates[i] - dates[i-1]
            intervals.append(delta.days)
        return round(mean(intervals), 2) if intervals else None
    
    # Calculate for categories
    for category, dates in category_dates.items():
        avg_interval = calculate_avg_days(dates)
        if avg_interval is not None:
            category_intervals[category] = avg_interval
    
    # Calculate for types
    for event_type, dates in type_dates.items():
        avg_interval = calculate_avg_days(dates)
        if avg_interval is not None:
            type_intervals[event_type] = avg_interval
    
    return {
        "category_intervals": category_intervals,
        "type_intervals": type_intervals
    }

def generate_events(year_range: str) -> dict:
    """Generate Apple and world events for a specific year range."""
    try:
        client = OpenAI(api_key=API_KEYS)
        
        # For recent/future years, modify the prompt
        is_recent = int(year_range) >= 2025
        
        base_message = f"""Return a JSON array of actual events from {year_range}. 

Create separate event entries for each model variant:
- iPhone variants (e.g., iPhone 11, 11 Pro, 11 Pro Max)
- iPad variants (e.g., iPad Pro 11", Pro 12.9")
- Mac variants (e.g., MacBook Pro 14", 16")
- Watch variants (e.g., Series 7 41mm, 45mm)

Include:
1. All product launches (as separate variants)
2. Software releases
3. Corporate events
4. Policy changes
5. Major world events

Return ONLY valid JSON. No additional text."""

        # Add specific handling for recent/future years
        if is_recent:
            user_message = base_message + f"""

For {year_range}, include:
- Confirmed product launches and announcements
- Released software updates
- Verified events that have occurred
- Announced future events with confirmed dates
- Major world events with verified dates"""
        else:
            user_message = base_message

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},  # Changed from system_prompt to SYSTEM_PROMPT
            {"role": "user", "content": user_message}
        ]
        
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=7500
        )
        
        response = completion.choices[0].message.content.strip()
        
        # Clean the response and extract JSON
        cleaned_response = response.replace('```json', '').replace('```', '').strip()
        start_idx = cleaned_response.find('{')
        end_idx = cleaned_response.rfind('}') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_content = cleaned_response[start_idx:end_idx]
            try:
                parsed_json = json.loads(json_content)
                return parsed_json
            except json.JSONDecodeError:
                if is_recent:
                    return {
                        "reasoning": f"Events from {year_range}",
                        "annotated_events": []
                    }
                raise
        else:
            if is_recent:
                return {
                    "reasoning": f"Events from {year_range}",
                    "annotated_events": []
                }
            raise ValueError("No valid JSON found in response")
            
    except Exception as e:
        print(f"Error processing {year_range}: {str(e)}")
        if is_recent:
            return {
                "reasoning": f"Events from {year_range}",
                "annotated_events": []
            }
        return {"error": str(e)}

def collect_events():
    """Collect all events."""
    time_periods = [
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025"
    ]
    
    all_events = []
    for period in time_periods:
        print(f"\nProcessing period {period}")
        result = generate_events(period)
        
        if "annotated_events" in result:
            all_events.extend(result["annotated_events"])
            print(f"Added {len(result['annotated_events'])} events from {period}")
        else:
            print(f"Failed to get events for {period}")
    
    # Sort events by date
    all_events.sort(key=lambda x: x.get("event_date", "9999-99-99"))

    intervals = calculate_intervals(all_events)
    
    final_result = {
        "reasoning": "Events collected in time periods and merged chronologically",
        "annotated_events": all_events,
        "average_intervals": intervals
    }
    
    # Save to file
    with open("apple_and_world_events.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)
    
    return final_result

def print_summary(result):
    """Print a summary of collected events."""
    if "annotated_events" in result:
        events = result["annotated_events"]
        print(f"\nCollected {len(events)} total events")
        
        # Count events by category
        categories = {"Apple": 0, "World": 0}
        event_types = {}
        
        for event in events:
            cat = event.get("category", "Unknown")
            event_type = event.get("event_type", "Unknown")
            
            categories[cat] = categories.get(cat, 0) + 1
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        print("\nEvents by Category:")
        for category, count in categories.items():
            print(f"{category}: {count}")
            
        print("\nEvents by Type:")
        for event_type, count in event_types.items():
            print(f"{event_type}: {count}")
        
        if "average_intervals" in result:
            print("\nAverage Intervals (days):")
            print("\nBy Category:")
            for category, interval in result["average_intervals"]["category_intervals"].items():
                print(f"{category}: {interval} days")
            print("\nBy Event Type:")
            for event_type, interval in result["average_intervals"]["type_intervals"].items():
                print(f"{event_type}: {interval} days")
        
        if events:
            print("\nFirst 3 events:")
            for event in events[:3]:
                print(f"{event['event_date']}: {event['event_name']} ({event['category']})")
            
            print("\nLast 3 events:")
            for event in events[-3:]:
                print(f"{event['event_date']}: {event['event_name']} ({event['category']})")

if __name__ == "__main__":
    print("Starting event collection...")
    result = collect_events()
    print_summary(result)