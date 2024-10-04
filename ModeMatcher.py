import streamlit as st
from Lens_Solve import *


if 'lenses' not in st.session_state:
    st.session_state.lenses = []
if 's0' not in st.session_state:
    st.session_state.s0 = None
if 'r0' not in st.session_state:
    st.session_state.r0 = None
if 'lam0' not in st.session_state:
    st.session_state.lam0 = None
if 'sF' not in st.session_state:
    st.session_state.sF = None
if 'rF' not in st.session_state:
    st.session_state.rF = None
if 'd0min' not in st.session_state:
    st.session_state.d0min = None
if 'd0max' not in st.session_state:
    st.session_state.d0max = None
if 'd1min' not in st.session_state:
    st.session_state.d1min = None
if 'd1max' not in st.session_state:
    st.session_state.d1max = None
if 'd2min' not in st.session_state:
    st.session_state.d2min = None
if 'd2max' not in st.session_state:
    st.session_state.d2max = None
if 'max_dtot' not in st.session_state:
    st.session_state.max_dtot = None

st.image('diagram.jpg', caption="Diagram")

st.header("Enter Available Lenses")
# Lens array input (keeping it as is)
lens_str = st.text_input("Enter lens focal lengths:")
col = st.columns(3)

with col[0]:
    if st.button("Add Lens"):

        lens = None
        if lens_str:
            try:
                lens = float(lens_str)
            except ValueError:
                st.write("Invalid focal length")

        if lens:
            st.session_state.lenses.append(lens)
            st.write(f"Added lens: {lens}")
            st.write("Current lenses:", st.session_state.lenses)
        else:
            st.write("Please enter a valid focal length.")
            st.write("Current lenses:", st.session_state.lenses)

with col[1]:
    if st.button("Clear all"):
        st.session_state.lenses = []
        st.write("All lenses cleared.")

with col[2]:
    if st.button("Done"):
        if st.session_state.lenses:
            st.write("Final list of lenses:", st.session_state.lenses)
        else:
            st.write("No lenses were added.")


# Consolidating inputs and adding a 'Save All' button
st.header("Enter Parameters")
col = st.columns(3)
with col[0]:
    s0_str = st.text_input("Enter s0: ")
with col[1]:
    r0_str = st.text_input("Enter r0: ")
with col[2]:
    lam0_str = st.text_input("Enter lam0: ")

col1, col2 = st.columns(2)

with col1:
    sF_str = st.text_input("Enter desired sF: ")
    d0min_str = st.text_input("Enter minimum d0 ")
    d1min_str = st.text_input("Enter minimum d1: ")
    d2min_str = st.text_input("Enter minimum d2: ")

with col2:
    rF_str = st.text_input("Enter desired rF: ")
    d0max_str = st.text_input("Enter maximum d0: ")
    d1max_str = st.text_input("Enter maximum d1: ")
    d2max_str = st.text_input("Enter maximum d2: ")
max_dtot_str = st.text_input("Enter maximum dtot: ")


# Save All button
if st.button("Save All"):
    try:
        st.session_state.s0 = float(s0_str) if s0_str else None
        st.session_state.r0 = float(r0_str) if r0_str else 10**10  # default to collimated if empty
        st.session_state.lam0 = float(lam0_str) if lam0_str else None
        st.session_state.sF = float(sF_str) if sF_str else None
        st.session_state.rF = float(rF_str) if rF_str else 10**10  # default to collimated if empty
        st.session_state.d0min = float(d0min_str) if d0min_str else 0
        st.session_state.d0max = float(d0max_str) if d0max_str else None
        st.session_state.d1min = float(d1min_str) if d1min_str else 0
        st.session_state.d1max = float(d1max_str) if d1max_str else None
        st.session_state.d2min = float(d2min_str) if d2min_str else 0
        st.session_state.d2max = float(d2max_str) if d2max_str else None
        st.session_state.max_dtot = float(max_dtot_str) if max_dtot_str else None
        st.write("All inputs saved successfully.")
    except ValueError:
        st.write("Please check your inputs for valid numerical values.")

# Solve button
if st.button("Solve!"):
    lenses = st.session_state.lenses
    s0 = st.session_state.s0
    r0 = st.session_state.r0
    lam0 = st.session_state.lam0
    sF = st.session_state.sF
    rF = st.session_state.rF
    d0min = st.session_state.d0min
    d0max = st.session_state.d0max
    d1min = st.session_state.d1min
    d1max = st.session_state.d1max
    d2min = st.session_state.d2min
    d2max = st.session_state.d2max
    max_dtot = st.session_state.max_dtot

    if s0 and lam0 and sF and lenses:
        st.write("Solving...")
        bounds = [(d0min, d0max), (d1min, d1max), (d2min, d2max)]
        modes, setups = lens_solve(sF, lenses, s0, lam0, r0=r0, rF=rF, bounds=bounds, max_dtot=max_dtot)
        st.dataframe(modes)
        st.dataframe(setups)
    else:
        st.write("Please ensure all required inputs (s0, lam0, sF, and lenses) are provided.")
