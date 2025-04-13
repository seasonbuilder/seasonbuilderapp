import streamlit as st

def main():
    st.title("Download the Latest Season Builder App")
    st.write("Get the latest version of the Season Builder App on your mobile device using the links below:")

    # Create two columns to display the badges side-by-side.
    col1, col2 = st.columns(2)

    with col1:
        # Apple App Store badge (clickable)
        st.markdown(
            """
            <a href="https://apps.apple.com/us/app/coach-edge/id6505067739" target="_blank">
                <img src="https://developer.apple.com/app-store/marketing/guidelines/images/badge-download-on-the-app-store.svg" 
                     alt="Download on the App Store" style="height: 100px;">
            </a>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Google Play Store badge (clickable)
        st.markdown(
            """
            <a href="https://play.google.com/store/apps/details?id=com.coachedge.android" target="_blank">
                <img src="https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png" 
                     alt="Get it on Google Play" >
            </a>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()