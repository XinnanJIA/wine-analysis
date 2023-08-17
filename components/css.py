import streamlit as sl

css = f"""
    <style>
        section[data-testid='stSidebar']{{
            width: 240px;
        }}
        div[class='block-container css-z5fcl4 e1g8pov64']{{
            padding-right: 1.5rem;
            padding-left: 1.5rem;
        }}
        hr{{
            margin-top: 1em;
            margin-bottom: 1em;
        }}
        div[data-testid='stToolbar']{{
            display: none !important;
        }}
        footer{{
            display: none !important;
        }}
        div[data-testid='block-container']{{
            padding-top: 0rem;
        }}
        header{{
            display: none !important;
        }}
    </style>
"""
