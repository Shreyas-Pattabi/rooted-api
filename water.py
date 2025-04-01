import asyncio
import aiohttp
from datetime import datetime, timezone, timedelta
import random

API_BASE_URL = "http://127.0.0.1:8000/plants"  # Change this if running elsewhere

async def fetch_all_plants(session):
    """Fetch all plants from the API."""
    async with session.get(f"{API_BASE_URL}/all") as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error fetching plants: {response.status}")
            return []

async def update_plant(session, plant_id, update_data):
    """Update plant fields via PUT request."""
    async with session.put(f"{API_BASE_URL}/{plant_id}", json=update_data) as response:
        if response.status == 200:
            print(f"Updated plant {plant_id}: {update_data}")
        else:
            print(f"Failed to update plant {plant_id}: {response.status}")

def calculate_new_values(plant):
    """Generate realistic new values based on previous values."""
    updated_fields = {}

    # Simulate watering plant
    new_moisture = random.uniform(95.0, 100.0)
    updated_fields["water"] = round(new_moisture, 2)

    return updated_fields

async def simulate_plant_updates():
    """Periodically fetch and update plant data."""
    async with aiohttp.ClientSession() as session:
        plants = await fetch_all_plants(session)
        if not plants:
            print("No plants found. Retrying in 10 seconds...")
        else:
            tasks = []
            for plant in plants:
                update_data = calculate_new_values(plant)
                tasks.append(update_plant(session, plant["id"], update_data))
            
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(simulate_plant_updates())