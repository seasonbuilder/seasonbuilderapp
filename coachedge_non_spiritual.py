import streamlit as st

def main():
    st.title("Download the Latest Season Builder App")
    st.write("Get the latest version of the Season Builder App on your mobile device using the links below:")

    # Create two columns to display the badges side-by-side.
    col1, col2 = st.columns(2)

    with col1:
        # Apple App Store badge (clickable) with specified width and height.
        st.markdown(
            """
            <a href="https://apps.apple.com/us/app/coach-edge/id6505067739" target="_blank">
                <img src="https://developer.apple.com/app-store/marketing/guidelines/images/badge-download-on-the-app-store.svg" 
                     alt="Download on the App Store" style="width: 180px; height: 60px;">
            </a>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Google Play Store badge (clickable) with specified width and height.
        st.markdown(
            """
            <a href="https://play.google.com/store/apps/details?id=com.coachedge.android" target="_blank">
                <img src="https://storage.googleapis.com/pe-portal-consumer-prod-wagtail-static/images/googleplay-badge-01-getit.max-1920x1070.format-webp.webp?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=wagtail%40pe-portal-consumer-prod.iam.gserviceaccount.com%2F20250413%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250413T150714Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=02b01e69b92cee3c2510b3de98fb9044765c785c971f06d486c272bb973057d5896ffe82b098147e72e57fcc5126019e4e3c367184f3a002a326722361d5b2f8a88496f0ced3e15208a369f5989e1e9f9a221d6be49526c97c92af586e72d776eca8f851f985ceacacbc4cff2d9455bdcc37ec9dc2704c4e0e2e7ebe8bc724c2a37a701216ed3f82615a0d3630c5545962bdd3a69f64481bfc3cd1bed92f5da344c8e07983d86c18d0ab7ba09b8304bca985a1e985834a7b2d40f2aea66df9bd89456f1b7570074028b5f0de5443d027fd2fff9c22b628c8d0d40451be0a83bcc4fc3fa76dc2545457d6df8145ce1e63b14d5d166100194584f08553dca7295f" 
                     alt="Get it on Google Play" style="width: 180px; height: 80px;">
            </a>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()