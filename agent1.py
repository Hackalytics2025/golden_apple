from openai import OpenAI
import json

API_KEYS = "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"  # Replace with your API key

SYSTEM_PROMPT = """You are an API that ONLY returns valid JSON arrays containing Apple events. You must ALWAYS return data in this exact format:

{
    "reasoning": "Brief explanation of data collection process",
    "annotated_events": [
        {
            "event_name": "iPhone 13 Launch",
            "event_date": "2021-09-24",
            "event_type": "Product Launch",
            "source_text": "Description of the event",
            "impact": "Market impact and significance"
        }
    ]
}"""

def generate_events(year_range: str) -> dict:
    """Generate Apple events for a specific year range."""
    try:
        client = OpenAI(api_key=API_KEYS)
        
        user_message = f"""Return a JSON array of every major Apple event from {year_range}, including:
- Every product launch (iPhone, iPad, Mac, Watch versions)
- Every major software release (iOS, macOS versions)
- Major corporate events
- Policy changes
- Market actions

Format the response as valid JSON only. Start with {{ and end with }}."""
        
        print(f"Requesting events for {year_range}...")
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": "I will return a valid JSON object with the events."},
            {"role": "user", "content": "Return the JSON now. Start with { and end with }."}
        ]
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=2000
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
        "2005-2010",
        "2011-2015",
        "2016-2020",
        "2021-2025"
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
    
    final_result = {
        "reasoning": "Events collected in time periods and merged chronologically",
        "annotated_events": all_events
    }
    
    # Save to file
    with open("apple_events.json", "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)
    
    return final_result

if __name__ == "__main__":
    print("Starting event collection...")
    result = collect_events()
    
    if "annotated_events" in result:
        events = result["annotated_events"]
        print(f"\nCollected {len(events)} total events")
        
        if events:
            print("\nFirst 3 events:")
            for event in events[:3]:
                print(f"{event['event_date']}: {event['event_name']}")
            
            print("\nLast 3 events:")
            for event in events[-3:]:
                print(f"{event['event_date']}: {event['event_name']}")
    else:
        print("Failed to collect events")
        print(result)