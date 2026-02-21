"""Track B Frontend — Parameter Onboarding Wizard"""

import json
import os
import re
import httpx
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(
    page_title="LatSpace — Onboarding Wizard",
    page_icon="🏭",
    layout="wide",
)

STEPS = ["Plant Info", "Assets", "Parameters", "Formulas", "Review & Submit"]
ASSET_TYPES = ["boiler", "turbine", "product", "kiln", "other"]


# -------------------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------------------
def init_state():
    defaults = {
        "step": 1,
        "plant": {},
        "assets": [],
        "selected_params": [],
        "formulas": {},
        "submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
with st.sidebar:
    st.title("🏭 LatSpace AI")
    st.caption("Industrial ESG Platform")
    st.divider()
    st.markdown("### Track B")
    st.markdown("**Onboarding Wizard**")
    st.divider()
    st.markdown("**Progress**")

    for i, name in enumerate(STEPS, 1):
        icon = "✅" if i < st.session_state.step else (
            "▶️" if i == st.session_state.step else "⬜"
        )
        st.markdown(f"{icon} Step {i}: {name}")

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.title("🏭 Plant Onboarding Wizard")
step = st.session_state.step
st.progress(step / len(STEPS), text=f"Step {step} of {len(STEPS)}: {STEPS[step-1]}")
st.divider()

# -------------------------------------------------------------------
# STEP 1
# -------------------------------------------------------------------
if step == 1:
    st.markdown("## 🏗️ Step 1: Plant Information")

    with st.form("plant_form"):
        name = st.text_input("Plant Name *")
        address = st.text_input("Address *")
        email = st.text_input("Manager Email *")
        desc = st.text_area("Description")

        if st.form_submit_button("Next →"):
            if not name or not address or not email:
                st.error("All required fields must be filled.")
            elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                st.error("Invalid email format.")
            else:
                st.session_state.plant = {
                    "name": name.strip(),
                    "description": desc.strip(),
                    "address": address.strip(),
                    "manager_email": email.strip(),
                }
                st.session_state.step = 2
                st.rerun()

# -------------------------------------------------------------------
# STEP 2
# -------------------------------------------------------------------
elif step == 2:
    st.markdown("## ⚙️ Step 2: Assets")

    with st.form("asset_form"):
        a_name = st.text_input("Asset Name *")
        a_display = st.text_input("Display Name *")
        a_type = st.selectbox("Asset Type *", ASSET_TYPES)

        if st.form_submit_button("Add Asset"):
            if not a_name or not a_display:
                st.error("All asset fields required.")
            else:
                st.session_state.assets.append({
                    "name": a_name.strip(),
                    "display_name": a_display.strip(),
                    "type": a_type,
                })
                st.rerun()

    st.divider()

    if st.session_state.assets:
        for a in st.session_state.assets:
            st.write(f"- {a['name']} ({a['type']})")

    if st.button("Next →"):
        if not st.session_state.assets:
            st.error("Add at least one asset.")
        else:
            st.session_state.step = 3
            st.rerun()

# -------------------------------------------------------------------
# STEP 3
# -------------------------------------------------------------------
elif step == 3:
    st.markdown("## 📋 Step 3: Parameters")

    try:
        response = httpx.get(f"{API_BASE}/api/track-b/parameters", timeout=10)
        response.raise_for_status()
        params = response.json()
    except Exception:
        st.error("Backend not running.")
        st.stop()

    for p in params:
        if st.checkbox(p["display_name"], key=p["name"]):
            if p["name"] not in st.session_state.selected_params:
                st.session_state.selected_params.append(p["name"])

    if st.button("Next →"):
        if not st.session_state.selected_params:
            st.error("Select at least one parameter.")
        else:
            st.session_state.step = 4
            st.rerun()

# -------------------------------------------------------------------
# STEP 4
# -------------------------------------------------------------------
elif step == 4:
    st.markdown("## 🔢 Step 4: Formulas")

    for pname in st.session_state.selected_params:
        formula = st.text_input(f"Formula for {pname}", key=f"f_{pname}")
        if formula:
            st.session_state.formulas[pname] = formula

    if st.button("Next →"):
        st.session_state.step = 5
        st.rerun()

# -------------------------------------------------------------------
# STEP 5
# -------------------------------------------------------------------
elif step == 5:
    st.markdown("## ✅ Review & Submit")

    config = {
        "plant": st.session_state.plant,
        "assets": st.session_state.assets,
        "parameters": st.session_state.selected_params,
        "formulas": st.session_state.formulas,
    }

    st.json(config)

    if st.button("Submit"):
        try:
            resp = httpx.post(
                f"{API_BASE}/api/track-b/onboarding",
                json=config,
                timeout=10,
            )
            if resp.status_code == 200:
                st.success("Submitted successfully!")
                st.session_state.submitted = True
            else:
                st.error(resp.text)
        except Exception as e:
            st.error(str(e))

    if st.session_state.submitted:
        if st.button("Start New"):
            st.session_state.clear()
            init_state()
            st.rerun()