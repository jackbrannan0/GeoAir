import spacy
import asyncio
from backend.db.models import MapAlerts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os
from backend.nlp.entities import entity_extraction
from backend.geo.geocoder import geocode_location
from backend.nlp.sentiment import analyze_sentiment
load_dotenv()

GEOPOLITICAL_VERBS = {"intercept", "ground", "divert", "resume", "seize", "ban", "restrict", "close", "jamming", "gps", "gnss", "spoofing"}
GEOPOLITICAL_NOUNS = {"airspace", "sanction", "notam", "corridor", "border", "conflict", "missile"}
HIGH_PRIORITY_REGIONS = {
    # Original
    "ukraine", "gaza", "iran", "taiwan", "hormuz",
    # Middle East
    "iraq", "syria", "yemen", "lebanon", "israel", "palestine",
    "saudi_arabia", "turkey", "egypt", "sinai",
    # Eastern Europe
    "russia", "belarus", "moldova", "georgia", "crimea", "donbas",
    # Asia-Pacific
    "north_korea", "south_korea", "china", "south_china_sea",
    "myanmar", "hong_kong", "philippines", "vietnam", "pakistan",
    # Africa
    "sudan", "somalia", "ethiopia", "mali",
    # Americas
    "venezuela", "haiti", "colombia"
}
IGNORE_LOCATIONS = {"us", "united states", "europe", "africa"}
nlp = spacy.load("en_core_web_sm")

engine = create_async_engine(os.getenv("DATABASE_URL"))
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def process_data(db_session: AsyncSession):
    from backend.db.queries import load_db
    events = await load_db(db_session)
    
    if not events:
        print("No text found to process")
        return []

    loop = asyncio.get_running_loop()

    for event in events:
        print(f"\nProcessing Event ID {event.id}: {event.title[:50]}...")
        if not event.description:
            continue

        text_to_analyze = event.description
        doc = await loop.run_in_executor(None, nlp, text_to_analyze)
        
        found_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" and token.lemma_ in GEOPOLITICAL_VERBS]
        found_nouns = [token.text.lower() for token in doc if token.text.lower() in GEOPOLITICAL_NOUNS]
        signal_locations = [token.text.lower() for token in doc if token.text.lower() in HIGH_PRIORITY_REGIONS]
        
        if found_verbs or found_nouns or signal_locations:
            print(f"\n High Signal: {event.title[:50]}...")
            
            extracted = await entity_extraction(doc)
            all_hits = list(set(signal_locations + (extracted or [])))
            
            if all_hits:
                print(f"DEBUG: Found hits for {event.id}: {all_hits}")
                geo_results = await geocode_location(all_hits)
                sentiment_label, sentiment_score = await analyze_sentiment(text_to_analyze)
                print(f"{sentiment_label}: {sentiment_score}")
                print(f"DEBUG: Geocoder returned {len(geo_results)} results: {geo_results}")
                

                for res in geo_results:
                    lat, lon, addr = None, None, "Unknown"

                    if isinstance(res, dict):
                        lat = res.get("lat")
                        lon = res.get("lon")
                        addr = res.get("address", "Unknown")
                    
                    elif isinstance(res, (tuple, list)) and len(res) >= 2:
                        lat = res[0]
                        lon = res[1]
                        addr = res[2] if len(res) > 2 else "Unknown"

                    if lat and lon:
                        new_alert = MapAlerts(
                            raw_event_id=event.id,
                            location_name=addr,
                            latitude=float(lat), 
                            longitude=float(lon),
                            signals={"source": "nlp_pipeline"},
                            sentiment_score=sentiment_score,
                            severity_label="high" if sentiment_label == "negative" else "medium" if sentiment_label == "neutral" else "low"
                        )
                        db_session.add(new_alert)
                        print(f"    Alert Staged: {addr} ({lat}, {lon})")
                    else:
                        print(f"    Result skipped: Could not parse coordinates from {res}")
    
        event.processed = True


    try:
        await db_session.commit()
        print(f"\nPipeline Complete: Processed {len(events)} events.")
    except Exception as e:
        await db_session.rollback()
        print(f"Failed to commit: {e}")
        raise e