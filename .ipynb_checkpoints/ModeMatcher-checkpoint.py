import streamlit as st
from Lens_Solve import *


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
defaults = {
    'lenses': [],
    's0': None,
    'r0': None,
    'lam0': None,
    'sF': None,
    'rF': None,
    'd0min': None,
    'd0max': None,
    'd1min': None,
    'd1max': None,
    'd2min': None,
    'd2max': None,
    'max_dtot': None,
    'opened': False,
    'modes': None,
    'setups': None,
    # --- state for the "Open Setup" + "Explore Adjustments" flow ---
    'setup_opened': False,   # True once a valid setup has been opened
    'setup_lens1': None,
    'setup_lens2': None,
    'setup_single': False,
    'n0': 0,                 # number of +/- increments applied to d0
    'n1': 0,                 # number of +/- increments applied to d1
    'n2': 0,                 # number of +/- increments applied to d2
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.header('Welcome to Mode Matcher!')


col = st.columns(2)
with col[0]:
    st.image('parameters.jpg', use_column_width=True)
with col[1]:
    st.image('notes.jpg', use_column_width=True)
st.image('diagram.jpg', caption="Example diagram")


st.header("Enter Available Lenses")
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


if st.button("Save All"):
    try:
        st.session_state.opened = False
        st.session_state.setup_opened = False  # invalidate any previously opened setup
        st.session_state.s0 = float(s0_str) if s0_str else None
        st.session_state.r0 = float(r0_str) if r0_str else 10**10
        st.session_state.lam0 = float(lam0_str) if lam0_str else None
        st.session_state.sF = float(sF_str) if sF_str else None
        st.session_state.rF = float(rF_str) if rF_str else 10**10
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
        bounds = [(d0min, d0max), (d1min, d1max), (d2min, d2max)]
        modes, setups = lens_solve(sF, lenses, s0, lam0, r0=r0, rF=rF, bounds=bounds, max_dtot=max_dtot)
        st.session_state.modes = modes
        st.session_state.setups = setups
        st.session_state.opened = True
        st.session_state.setup_opened = False  # a fresh solve invalidates any previously opened setup
    else:
        st.write("Please ensure all required inputs (s0, lam0, sF, and lenses) are provided.")


if st.session_state.opened:
    lenses = st.session_state.lenses
    s0 = st.session_state.s0
    r0 = st.session_state.r0
    lam0 = st.session_state.lam0
    sF = st.session_state.sF
    rF = st.session_state.rF
    modes = st.session_state.modes
    setups = st.session_state.setups

    st.header("Modes:")
    st.write("Indexing - [lens1, lens2]")
    st.dataframe(modes)

    st.header("Setups:")
    st.write("Formatting - (d0,d1,d2)")
    st.dataframe(setups)

    st.header("Open Setup:")
    lens1_str = st.text_input("Lens 1:")
    lens2_str = st.text_input("Lens 2 (Leave blank for single lens setups):")

    if st.button('Open Setup'):
        validInput = True
        single = False
        try:
            lens1 = float(lens1_str)
            lens2 = float(lens2_str) if lens2_str else None

            if lens1 not in lenses:
                raise ValueError
            if lens2 and (lens2 not in lenses):
                raise ValueError

        except ValueError:
            st.write("Please provide a valid lens")
            validInput = False

        if validInput:
            single = lens2 is None

            # Persist the chosen setup so it survives reruns triggered by the
            # adjustment buttons below. Reset the increment counters whenever
            # a *new* setup is opened.
            st.session_state.setup_opened = True
            st.session_state.setup_lens1 = lens1
            st.session_state.setup_lens2 = lens2
            st.session_state.setup_single = single
            st.session_state.a0 = 0
            st.session_state.a1 = 0
            st.session_state.a2 = 0

    # ------------------------------------------------------------------
    # Everything below runs on EVERY rerun (not just the one immediately
    # after "Open Setup" is clicked) as long as a setup has been opened.
    # This is what lets the +/- adjustment buttons update the plot
    # without the rest of the section disappearing.
    # ------------------------------------------------------------------
    if st.session_state.setup_opened:
        lens1 = st.session_state.setup_lens1
        lens2 = st.session_state.setup_lens2
        single = st.session_state.setup_single

        if single:
            st_open_setup(lens1, modes, setups, s0, lam0, r0=r0)
        else:
            st_open_setup((lens1, lens2), modes, setups, s0, lam0, r0=r0)

        st.header('Explore Adjustments')

        incr_str = st.text_input(
            "Increment:", value="0.01", key="increment_str"
        )
        try:
            incr = float(incr_str)
        except ValueError:
            st.write("Invalid increment value — using 0.01 instead.")
            incr = 0.01

        

        if not single:
            bcol = st.columns(3)
            with bcol[0]:
                if st.button('d0 +'):
                    st.session_state.a0 += incr
                if st.button('d0 -'):
                    st.session_state.a0 -= incr
            with bcol[1]:
                if st.button('d1 +'):
                    st.session_state.a1 += incr
                if st.button('d1 -'):
                    st.session_state.a1 -= incr
            with bcol[2]:
                if st.button('d2 +'):
                    st.session_state.a2 += incr
                if st.button('d2 -'):
                    st.session_state.a2 -= incr

            adjustments = [
                st.session_state.a0,
                st.session_state.a1,
                st.session_state.a2,
            ]

            

            st_open_adjusted_setup(
                (lens1, lens2), setups, s0, lam0, adjustments, sF, rF=rF, r0=r0
            )

        else:
            bcol = st.columns(2)
            with bcol[0]:
                if st.button('d0 +'):
                    st.session_state.a0 += incr
                if st.button('d0 -'):
                    st.session_state.a0 -= incr
            with bcol[1]:
                if st.button('d1 +'):
                    st.session_state.a1 += incr
                if st.button('d1 -'):
                    st.session_state.a1 -= incr

            adjustments = [
                st.session_state.a0,
                st.session_state.a1,
            ]

            st_open_adjusted_setup(
                lens1, setups, s0, lam0, adjustments, sF, rF=rF, r0=r0
            )