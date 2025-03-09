import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)



if st.session_state['authentication_status']:
    with st.sidebar:
        st.markdown(f'## ようこそ！ *{st.session_state["name"]}さん*')
        authenticator.logout('Logout', 'sidebar')
        st.divider()
    try:
        email_of_registered_user, \
        username_of_registered_user, \
        name_of_registered_user = authenticator.register_user(pre_authorized=config['pre-authorized']['emails'])
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)


    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
        
else:
    st.warning("**ログイン画面からログインしてください**")