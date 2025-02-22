from openai import OpenAI
import json
from dotenv import load_dotenv
import os

API_KEYS = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are an API that searches the entire Internet and returns valid JSON arrays containing both Apple events and major world events. DO NOT HALLUCINATE. Return data in this exact format:

{
    "reasoning": "Brief explanation of data collection process",
    "annotated_events": [
        {
            "event_name": "Event name",
            "event_date": "YYYY-MM",
            "event_type": "Product Launch/Software Release/Policy Change/Market Action/Major Positive World Event/Major Negative World Event/Minor Positive World Event/Minor Negative World Event",
            "category": "Apple/World",
        }
    ]
}"""

def generate_events(year_range: str) -> dict:
    """Generate Apple and world events for a specific year range."""
    try:
        client = OpenAI(api_key=API_KEYS)
        
        user_message = f"""Return a JSON array of Apple events AND major world events from {year_range}, including:

Apple Events:
- Every product launch (including iPhone, iPad, Mac, Watch versions, which should be specified counts. Example: iPhone 13, iPhone 13 Pro, iPad Pro 2022)
- Every major software release (iOS, macOS versions)
- Major corporate events
- Policy changes
- Market actions

World Events:
- Major political events
- Economic milestones
- Natural disasters
- Scientific breakthroughs
- Cultural moments
- Technological advances (non-Apple)

For world events, focus on those that either:
1. Had global significance
2. May have influenced Apple's business or tech industry
3. Represented major shifts in technology or society

Format as valid JSON only. Start with {{ and end with }}."""
        
        print(f"Requesting events for {year_range}...")
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "I will return a valid JSON object with both Apple and world events."},
            {"role": "user", "content": "Return the JSON now. Start with { and end with }."}
        ]
        
        completion = client.chat.completions.create(
            model="gpt-4o",  # Changed from gpt-4o to gpt-4
            messages=messages,
            temperature=0,
            max_tokens=7800
        )
        
        response = completion.choices[0].message.content.strip()
        
        # Remove any markdown formatting
        response = response.replace('```json', '').replace('```', '').strip()
        
        # Ensure response starts with { and ends with }
        if not response.startswith('{'):
            response = '{' + response
        if not response.endswith('}'):
            response = response + '}'
            
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print("Raw Response:", response)
            return {"error": "Failed to parse JSON", "raw_response": response}
            
    except Exception as e:
        print(f"API Error: {e}")
        return {"error": str(e)}

def collect_events():
    """Collect all events in smaller time chunks."""
    time_periods = [
        "2005-2006",
        "2007-2008",
        "2009-2010",
        "2011-2012",
        "2013-2014",
        "2015-2016",
        "2017-2018",
        "2019-2020",
        "2021-2022",
        "2023",
        "2024",
        "2025",
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
    all_events.sort(key=lambda x: x.get("event_date", "9999-99"))
    
    final_result = {
        "reasoning": "Events collected in time periods and merged chronologically, including both Apple and major world events",
        "annotated_events": all_events
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
        apple_events = sum(1 for e in events if e.get("category") == "Apple")
        world_events = sum(1 for e in events if e.get("category") == "World")
        print(f"\nApple Events: {apple_events}")
        print(f"World Events: {world_events}")
        
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