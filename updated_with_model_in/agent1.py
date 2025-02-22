from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import glob

load_dotenv()
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
            model="gpt-4",
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

def merge_price_data(events_data, iphone_price_files):
    """
    Merge iPhone price data with events data based on matching dates.
    
    Args:
        events_data (dict): Dictionary containing event data
        iphone_price_files (list): List of iPhone price data JSON files
    
    Returns:
        dict: Merged data with events and prices
    """
    # Load all iPhone price data
    price_data = {}
    for price_file in iphone_price_files:
        with open(price_file, 'r') as f:
            data = json.load(f)
            # Use filename as identifier (e.g., "Apple iPhone 11 128GB")
            model = os.path.splitext(os.path.basename(price_file))[0]
            price_data[model] = data

    # Create a merged version of events with price data
    merged_events = []
    for event in events_data["annotated_events"]:
        event_date = event["event_date"]
        
        # Create a copy of the event
        merged_event = event.copy()
        
        # Add price data for each iPhone model if available for this date
        price_info = {}
        for model, prices in price_data.items():
            if event_date in prices:
                model_data = prices[event_date]
                price_info[model] = {
                    "new": model_data.get("new"),
                    "used": model_data.get("used"),
                    "new_change": model_data.get("new_change"),
                    "used_change": model_data.get("used_change")
                }
        
        if price_info:
            merged_event["price_data"] = price_info
        
        merged_events.append(merged_event)

    return {
        "reasoning": events_data["reasoning"],
        "annotated_events": merged_events
    }

def collect_events():
    """Collect all events and merge with price data."""
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
    
    initial_result = {
        "reasoning": "Events collected in time periods and merged chronologically, including both Apple and major world events",
        "annotated_events": all_events
    }
    
    # Find all iPhone price JSON files
    iphone_price_files = glob.glob("Apple iPhone*.json")
    
    # Merge price data with events
    final_result = merge_price_data(initial_result, iphone_price_files)
    
    # Save to file
    output_file = "apple_world_events_with_prices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)
    
    print(f"\nSaved merged data to {output_file}")
    return final_result

def print_summary(result):
    """Print a summary of collected events with price data."""
    if "annotated_events" in result:
        events = result["annotated_events"]
        print(f"\nCollected {len(events)} total events")
        
        # Count events by category
        apple_events = sum(1 for e in events if e.get("category") == "Apple")
        world_events = sum(1 for e in events if e.get("category") == "World")
        events_with_prices = sum(1 for e in events if "price_data" in e)
        
        print(f"\nApple Events: {apple_events}")
        print(f"World Events: {world_events}")
        print(f"Events with price data: {events_with_prices}")
        
        if events:
            print("\nFirst 3 events:")
            for event in events[:3]:
                print(f"{event['event_date']}: {event['event_name']} ({event['category']})")
                if "price_data" in event:
                    print("  Price data available for models:", ", ".join(event["price_data"].keys()))
            
            print("\nLast 3 events:")
            for event in events[-3:]:
                print(f"{event['event_date']}: {event['event_name']} ({event['category']})")
                if "price_data" in event:
                    print("  Price data available for models:", ", ".join(event["price_data"].keys()))

if __name__ == "__main__":
    print("Starting event collection...")
    result = collect_events()
    print_summary(result)