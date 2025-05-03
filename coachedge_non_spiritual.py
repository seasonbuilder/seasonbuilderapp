import streamlit as st

def main():
    st.title("Download the Latest Season Builder App")
    st.write("Get the latest version of the Season Builder App on your mobile device using the links below:")

    # Create two columns to display the links side-by-side.
    col1, col2 = st.columns(2)

    with col1:
        # Hyperlinked text for the Apple App Store
        st.markdown("[Download on the App Store](https://apps.apple.com/us/app/coach-edge/id6505067739)")
    
    with col2:
        # Hyperlinked text for the Google Play Store
        st.markdown("[Get it on Google Play](https://play.google.com/store/apps/details?id=com.coachedge.android)")

if __name__ == "__main__":
    main()                                                             