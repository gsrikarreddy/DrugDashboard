import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

DRUG_EMOJIS = {
    "Fentanyl": ["💀", "☠️", "⚰️"],
    "Xylazine": ["🐎", "🧪", "💉"],
    "Metonitazene": ["💊", "🧬", "🧪"],
    "Flubromazepam": ["🧪", "🧫", "🧬"],
    "MDMA": ["😵‍💫", "🎉", "🧠"],
    "LSD": ["🎨", "🌈", "🌀"],
    "Morphine": ["💉", "🛌", "🏥"],
    "Oxymorphone": ["🔬", "💊", "🏥"],
    "Gabapentin": ["🧠", "💊", "🛌"],
    "Codeine": ["🍷", "😴", "💊"],
    "Methamphetamine": ["⚡", "🔥", "💥"],
    "Diphenhydramine": ["🛌", "🌙", "💤"],
    "Pentylone": ["💣", "🚀", "🔥"],
    "Hydrocodone": ["🏥", "💊", "😷"]
}   

def generate_fake_data(drug_name):
    today = datetime.today()
    dates = [today - timedelta(weeks=i) for i in range(12)][::-1]
    np.random.seed(hash(drug_name) % 123456)
    values = np.random.randint(50, 250, size=len(dates))
    return pd.DataFrame({'Date': dates, 'Mentions': values})

def generate_dummy_county_mentions(drug_name, count=2000):
    np.random.seed(hash(drug_name) % 100000)
    fips_codes = [f"{i:05d}" for i in np.random.choice(range(1000, 57000), size=count, replace=False)]
    mentions = np.random.randint(100, 1000, size=count)
    return pd.DataFrame({"fips": fips_codes, "Mentions": mentions})

def generate_dummy_posts(drug_name, count=10):
    np.random.seed(hash(drug_name) % 456789)
    sample_users = [f"@user{i}" for i in range(1, count+1)]
    sample_texts = [
        f"{drug_name} saved my life!",
        f"Just tried {drug_name} 😵‍💫",
        f"{drug_name} is trending again...",
        f"Doctors prescribed {drug_name} for me.",
        f"Any alternatives to {drug_name}?",
        f"Crazy side effects from {drug_name}",
        f"People are panic buying {drug_name} now.",
        f"Here’s what I think about {drug_name} 👇",
        f"My experience with {drug_name} wasn’t great.",
        f"{drug_name} is everywhere these days."
    ]
    times = pd.date_range(end=datetime.now(), periods=count).strftime('%Y-%m-%d %H:%M:%S')
    return pd.DataFrame({"User": sample_users, "Time": times, "Post": sample_texts})

def generate_dummy_trending(freq):
    today = datetime.today()
    if freq == 'weekly':
        dates = [today - timedelta(weeks=i) for i in range(12)][::-1]
        top_5_drugs = ["Fentanyl", "Xylazine", "Metonitazene", "Flubromazepam", "MDMA"]
    elif freq == 'monthly':
        dates = [today.replace(day=1) - pd.DateOffset(months=i) for i in range(12)][::-1]
        top_5_drugs = ["LSD", "Morphine", "MDMA", "Oxymorphone", "Gabapentin"]
    elif freq == 'yearly':
        dates = [today.replace(month=1, day=1) - pd.DateOffset(years=i) for i in range(5)][::-1]
        top_5_drugs = ["Codeine", "Methamphetamine", "Diphenhydramine", "Pentylone", "Hydrocodone"]
    else:
        raise ValueError("Invalid frequency")

    data = pd.DataFrame({'Date': dates})
    for drug in top_5_drugs:
        np.random.seed(hash((drug, freq)) % 123456)
        values = np.random.randint(50, 300, size=len(dates))
        data[drug] = values
    return data
