import os

from supabase import Client, create_client


def get_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    service_role_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not service_role_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured"
        )
    return create_client(url, service_role_key)


def list_rooms() -> list[dict]:
    return get_client().table("rooms").select("*").order("created_at", desc=True).execute().data


def add_room(name: str, topic: str) -> dict:
    result = (
        get_client()
        .table("rooms")
        .insert({"name": name, "topic": topic, "host": "You"})
        .execute()
    )
    return result.data[0]


def join_room(room_id: int) -> dict | None:
    client = get_client()
    current = client.table("rooms").select("*").eq("id", room_id).maybe_single().execute().data
    if not current:
        return None

    result = (
        client.table("rooms")
        .update({"listeners": current["listeners"] + 1})
        .eq("id", room_id)
        .execute()
    )
    return result.data[0] if result.data else None


def list_messages() -> list[dict]:
    rows = (
        get_client()
        .table("messages")
        .select("*")
        .order("created_at", desc=False)
        .limit(100)
        .execute()
        .data
    )
    return [
        {
            "user": row["user_name"],
            "text": row["text"],
            "time": row["created_at"],
        }
        for row in rows
    ]


def add_message(text: str) -> dict:
    result = (
        get_client()
        .table("messages")
        .insert({"user_name": "You", "text": text})
        .execute()
    )
    row = result.data[0]
    return {"user": row["user_name"], "text": row["text"], "time": row["created_at"]}