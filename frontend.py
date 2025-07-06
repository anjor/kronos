#!/usr/bin/env python3
"""Streamlit frontend for Kronos calendar management"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

API_BASE = "http://localhost:8000/api"

st.set_page_config(
    page_title="Kronos Calendar Manager",
    page_icon="📅",
    layout="wide"
)

def api_request(method, endpoint, data=None):
    """Make API request to Kronos backend"""
    try:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Kronos API. Make sure the server is running on localhost:8000")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_users():
    """Get all users"""
    return api_request("GET", "/users/")

def create_user(email, name, timezone="UTC"):
    """Create a new user"""
    return api_request("POST", "/users/", {
        "email": email,
        "name": name,
        "timezone": timezone
    })

def get_calendars(user_id):
    """Get calendars for a user"""
    return api_request("GET", f"/calendars/?user_id={user_id}")

def create_calendar(user_id, provider, provider_calendar_id, name, description="", is_primary=False):
    """Create a new calendar"""
    return api_request("POST", "/calendars/", {
        "user_id": user_id,
        "provider": provider,
        "provider_calendar_id": provider_calendar_id,
        "name": name,
        "description": description,
        "is_primary": is_primary
    })

def get_events(user_id):
    """Get events for a user"""
    return api_request("GET", f"/events/?user_id={user_id}")

def sync_to_master(user_id, create_busy_blocks=True):
    """Sync all calendars to master calendar"""
    return api_request("POST", f"/sync/sync-to-master/{user_id}?create_busy_blocks={create_busy_blocks}")

def create_master_calendar(user_id):
    """Create master calendar for user"""
    return api_request("POST", f"/sync/master-calendar?user_id={user_id}")

# Main app
st.title("📅 Kronos Calendar Manager")
st.markdown("Unified calendar management for freelancers")

# Sidebar for user selection
st.sidebar.header("User Management")

# Get users
users = get_users()
if users:
    user_options = {f"{user['name']} ({user['email']})": user for user in users}
    selected_user_display = st.sidebar.selectbox(
        "Select User",
        ["Create New User..."] + list(user_options.keys())
    )
    
    if selected_user_display == "Create New User...":
        with st.sidebar.expander("Create New User", expanded=True):
            new_email = st.text_input("Email")
            new_name = st.text_input("Name")
            new_timezone = st.selectbox("Timezone", [
                "UTC", "America/New_York", "America/Los_Angeles", 
                "Europe/London", "Europe/Paris", "Asia/Tokyo"
            ])
            
            if st.button("Create User"):
                if new_email and new_name:
                    result = create_user(new_email, new_name, new_timezone)
                    if result:
                        st.success(f"Created user: {new_name}")
                        st.rerun()
                else:
                    st.error("Please fill in all fields")
        
        selected_user = None
    else:
        selected_user = user_options[selected_user_display]
else:
    st.sidebar.info("No users found. Create one to get started.")
    with st.sidebar.expander("Create First User", expanded=True):
        new_email = st.text_input("Email")
        new_name = st.text_input("Name")
        new_timezone = st.selectbox("Timezone", [
            "UTC", "America/New_York", "America/Los_Angeles", 
            "Europe/London", "Europe/Paris", "Asia/Tokyo"
        ])
        
        if st.button("Create User"):
            if new_email and new_name:
                result = create_user(new_email, new_name, new_timezone)
                if result:
                    st.success(f"Created user: {new_name}")
                    st.rerun()
            else:
                st.error("Please fill in all fields")
    
    selected_user = None

if selected_user:
    user_id = selected_user["id"]
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📅 Calendars", "🔄 Sync", "📋 Events"])
    
    with tab1:
        st.header(f"Dashboard for {selected_user['name']}")
        
        col1, col2, col3 = st.columns(3)
        
        # Get calendar count
        calendars = get_calendars(user_id) or []
        master_calendars = [c for c in calendars if c.get('is_master', False)]
        source_calendars = [c for c in calendars if not c.get('is_master', False)]
        
        with col1:
            st.metric("Total Calendars", len(calendars))
        
        with col2:
            st.metric("Source Calendars", len(source_calendars))
        
        with col3:
            st.metric("Master Calendars", len(master_calendars))
        
        # Calendar status
        if calendars:
            st.subheader("Calendar Overview")
            calendar_df = pd.DataFrame([{
                "Name": cal["name"],
                "Provider": cal["provider"],
                "Type": "Master" if cal.get("is_master") else "Source",
                "Active": "✅" if cal["is_active"] else "❌",
                "Primary": "⭐" if cal.get("is_primary") else ""
            } for cal in calendars])
            st.dataframe(calendar_df, use_container_width=True)
        else:
            st.info("No calendars connected yet. Go to the Calendars tab to add some!")
    
    with tab2:
        st.header("Calendar Management")
        
        # Show existing calendars
        calendars = get_calendars(user_id) or []
        if calendars:
            st.subheader("Connected Calendars")
            for cal in calendars:
                with st.expander(f"{cal['name']} ({cal['provider']})", expanded=False):
                    st.write(f"**Provider ID:** {cal['provider_calendar_id']}")
                    st.write(f"**Description:** {cal.get('description', 'None')}")
                    st.write(f"**Type:** {'Master Calendar' if cal.get('is_master') else 'Source Calendar'}")
                    st.write(f"**Active:** {'Yes' if cal['is_active'] else 'No'}")
                    st.write(f"**Primary:** {'Yes' if cal.get('is_primary') else 'No'}")
        
        st.subheader("Add New Calendar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cal_name = st.text_input("Calendar Name")
            cal_provider = st.selectbox("Provider", ["google", "outlook", "apple"])
            cal_provider_id = st.text_input("Provider Calendar ID")
        
        with col2:
            cal_description = st.text_area("Description (optional)")
            cal_is_primary = st.checkbox("Set as primary calendar")
        
        if st.button("Add Calendar"):
            if cal_name and cal_provider_id:
                result = create_calendar(
                    user_id, cal_provider, cal_provider_id, 
                    cal_name, cal_description, cal_is_primary
                )
                if result:
                    st.success(f"Added calendar: {cal_name}")
                    st.rerun()
            else:
                st.error("Please fill in required fields")
        
        # Master calendar management
        st.subheader("Master Calendar")
        if not master_calendars:
            st.warning("No master calendar found!")
            if st.button("Create Master Calendar"):
                result = create_master_calendar(user_id)
                if result:
                    st.success("Master calendar created!")
                    st.rerun()
        else:
            st.success("Master calendar is set up ✅")
    
    with tab3:
        st.header("Calendar Synchronization")
        
        # Sync controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sync to Master")
            create_busy = st.checkbox("Create busy blocks on source calendars", value=True)
            
            if st.button("🔄 Sync All Calendars", type="primary"):
                with st.spinner("Syncing calendars..."):
                    result = sync_to_master(user_id, create_busy)
                    if result:
                        st.success(f"Sync completed! {result}")
                    else:
                        st.error("Sync failed")
        
        with col2:
            st.subheader("Sync Status")
            if calendars:
                sync_status = []
                for cal in calendars:
                    sync_status.append({
                        "Calendar": cal["name"],
                        "Last Sync": "Not implemented yet",
                        "Status": "Active" if cal["is_active"] else "Inactive"
                    })
                st.dataframe(pd.DataFrame(sync_status), use_container_width=True)
        
        # Sync history placeholder
        st.subheader("Recent Sync Activity")
        st.info("Sync history tracking coming soon...")
    
    with tab4:
        st.header("Events Overview")
        
        # Get events
        events = get_events(user_id) or []
        
        if events:
            st.subheader(f"All Events ({len(events)} total)")
            
            # Convert to DataFrame for better display
            events_df = pd.DataFrame([{
                "Title": event["title"],
                "Start": event["start_time"],
                "End": event["end_time"],
                "Calendar": event.get("calendar_id", "Unknown"),
                "Type": event.get("event_type", "event")
            } for event in events])
            
            st.dataframe(events_df, use_container_width=True)
            
            # Event type breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                event_types = events_df["Type"].value_counts()
                st.subheader("Event Types")
                st.bar_chart(event_types)
            
            with col2:
                st.subheader("Upcoming Events")
                now = datetime.now()
                upcoming = [e for e in events if datetime.fromisoformat(e["start_time"].replace("Z", "+00:00")) > now]
                st.metric("Next 7 Days", len(upcoming))
        else:
            st.info("No events found. Sync your calendars to see events here!")

else:
    st.info("👈 Select or create a user to get started!")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit for Kronos Calendar Management")