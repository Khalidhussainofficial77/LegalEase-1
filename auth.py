import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def sign_up(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            supabase.table("profiles").insert({
                "id": str(res.user.id),
                "email": email,
                "plan": "free",
                "analyses_used": 0
            }).execute()
            return True, "Account created! Please check your email to verify."
        return False, "Signup failed. Try again."
    except Exception as e:
        return False, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            st.session_state.user = res.user
            st.session_state.email = res.user.email
            profile = supabase.table("profiles").select("*").eq("id", str(res.user.id)).execute()
            if profile.data:
                st.session_state.plan = profile.data[0]["plan"]
                st.session_state.analyses_used = profile.data[0]["analyses_used"]
            return True, "Login successful!"
        return False, "Invalid email or password."
    except Exception as e:
        return False, str(e)

def sign_out():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.session_state.email = None
    st.session_state.plan = "free"
    st.session_state.analyses_used = 0

def get_analyses_remaining():
    plan = st.session_state.get("plan", "free")
    if plan == "pro" or plan == "business":
        return 999
    used = st.session_state.get("analyses_used", 0)
    return max(0, 3 - used)

def increment_analyses():
    if not st.session_state.get("user"):
        return
    user_id = str(st.session_state.user.id)
    used = st.session_state.get("analyses_used", 0) + 1
    st.session_state.analyses_used = used
    supabase.table("profiles").update({"analyses_used": used}).eq("id", user_id).execute()
