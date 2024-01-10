import streamlit as st
import requests

def download_large_zip_file(url, filename):
    with open(filename, "wb") as file:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_length = response.headers.get("content-length")

        if total_length is None:
            file.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                file.write(data)
                done = int(50 * dl / total_length)
                st.progress(done / 50)

st.title("Download Large Zip File")

url = st.text_input("Enter the URL of the large zip file:")
filename = st.text_input("Enter the desired filename (with extension):")

if st.button("Download"):
    if url and filename:
        try:
            st.text("Downloading...")
            download_large_zip_file(url, filename)
            st.success("Download completed!")
        except Exception as e:
            st.error(f"An error occurred during the download: {e}")
    else:
        st.warning("Please enter both the URL and filename.")