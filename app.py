import streamlit as st
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="AES-256-GCM File Security",
    page_icon="🔐",
    layout="wide"
)

# ==========================================================
# SESSION STATE
# ==========================================================
if "page" not in st.session_state:
    st.session_state.page = "Encrypt File"

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

/* ==========================================================
   GLOBAL STYLES
========================================================== */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #f4f7fb !important;
    color: #1f2937 !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #1f2937;
}

/* ==========================================================
   HEADER
========================================================== */
.main-title {
    background: linear-gradient(90deg, #102a43, #176b87);
    color: #ffffff !important;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 20px;
}

.main-title h1,
.main-title p {
    color: #ffffff !important;
}

.main-title h1 {
    margin-bottom: 8px;
}

.main-title p {
    margin: 5px;
}

/* ==========================================================
   SECTION HEADINGS
========================================================== */
.section-heading {
    font-size: 28px;
    font-weight: 700;
    color: #102a43 !important;
    margin-top: 15px;
    margin-bottom: 15px;
}

/* ==========================================================
   SUMMARY CARDS
========================================================== */
.info-card {
    background: #ffffff !important;
    border: 1px solid #dce5ee;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    margin-bottom: 10px;
}

.info-card h3 {
    color: #176b87 !important;
    margin: 0;
}

.info-card p {
    color: #526477 !important;
    margin-bottom: 0;
}

/* ==========================================================
   FILE UPLOADER LABELS
========================================================== */
.stApp [data-testid="stFileUploader"] {
    color: #1f2937 !important;
}

.stApp [data-testid="stFileUploader"] label,
.stApp [data-testid="stFileUploader"] label *,
.stApp [data-testid="stFileUploader"] label p {
    color: #1f2937 !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* ==========================================================
   UPLOAD DROP ZONE
========================================================== */
.stApp [data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1px dashed #b8c5d3 !important;
    border-radius: 9px !important;
    box-shadow: none !important;
}

.stApp [data-testid="stFileUploaderDropzone"] > div {
    background-color: transparent !important;
}

.stApp [data-testid="stFileUploaderDropzoneInstructions"],
.stApp [data-testid="stFileUploaderDropzoneInstructions"] * {
    color: #1f2937 !important;
    -webkit-text-fill-color: #1f2937 !important;
}


/* UPLOADED FILE CHIP: BLUE BACKGROUND + WHITE TEXT */
.stApp [data-testid="stFileUploaderFile"] {
    background-color: #176b87 !important;
    color: #ffffff !important;
    border: 1px solid #176b87 !important;
    border-radius: 8px !important;
}

.stApp [data-testid="stFileUploaderFile"] div,
.stApp [data-testid="stFileUploaderFile"] p,
.stApp [data-testid="stFileUploaderFile"] span,
.stApp [data-testid="stFileUploaderFile"] small,
.stApp [data-testid="stFileUploaderFile"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* KEEP REMOVE-FILE BUTTON TRANSPARENT */
.stApp [data-testid="stFileUploaderFile"] button {
    background-color: transparent !important;
    border: none !important;
}

.stApp [data-testid="stFileUploaderFile"] button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


/* ==========================================================
   NAVIGATION AND ACTION BUTTONS
========================================================== */
.stApp div[data-testid="stButton"] > button {
    background: #176b87 !important;
    background-color: #176b87 !important;
    color: #ffffff !important;
    border: 1px solid #176b87 !important;
    border-radius: 8px !important;
}

.stApp div[data-testid="stButton"] > button p,
.stApp div[data-testid="stButton"] > button span,
.stApp div[data-testid="stButton"] > button svg {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stApp div[data-testid="stButton"] > button:hover {
    background: #102a43 !important;
    border-color: #102a43 !important;
}

/* Primary buttons */
.stApp div[data-testid="stButton"] > button[kind="primary"] {
    background: #102a43 !important;
    color: #ffffff !important;
}

/* ==========================================================
   DOWNLOAD BUTTONS
========================================================== */
.stApp div[data-testid="stDownloadButton"] > button {
    background: #176b87 !important;
    background-color: #176b87 !important;
    color: #ffffff !important;
    border: 1px solid #176b87 !important;
    border-radius: 8px !important;
}

.stApp div[data-testid="stDownloadButton"] > button *,
.stApp div[data-testid="stDownloadButton"] > button p,
.stApp div[data-testid="stDownloadButton"] > button span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ==========================================================
   ALERTS
========================================================== */
.stApp [data-testid="stAlert"] {
    border-radius: 8px !important;
}

.stApp [data-testid="stAlert"] p,
.stApp [data-testid="stAlert"] div,
.stApp [data-testid="stAlert"] span {
    color: #1f2937 !important;
    -webkit-text-fill-color: #1f2937 !important;
}

/* ==========================================================
   RADIO BUTTONS AND INPUTS
========================================================== */
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stRadio"] label p {
    color: #1f2937 !important;
}

.stApp input,
.stApp textarea {
    color: #1f2937 !important;
}

/* ==========================================================
   SECURITY INFORMATION
========================================================== */
.security-note {
    background: #eaf4ff !important;
    color: #102a43 !important;
    padding: 14px 16px;
    margin-top: 12px;
    border-left: 5px solid #176b87;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.6;
}

.security-note strong,
.security-note span {
    color: #102a43 !important;
}

/* ==========================================================
   FOOTER
========================================================== */
.custom-footer {
    background: #102a43 !important;
    color: #ffffff !important;
    padding: 18px;
    margin-top: 15px;
    text-align: center;
    border-radius: 10px;
    font-size: 14px;
    width: 100%;
    box-sizing: border-box;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================
st.markdown("""
<div class="main-title">
    <h1>🔐 AES-256-GCM File Security Dashboard</h1>
    <p>CRYPTOGRAPHY AND NETWORK SECURITY (CNS)</p>
    <p>Project by Impana P</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# NAVIGATION
# ==========================================================
nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    if st.button("🔒 Encrypt File", use_container_width=True):
        st.session_state.page = "Encrypt File"

with nav2:
    if st.button("🔓 Decrypt File", use_container_width=True):
        st.session_state.page = "Decrypt File"

with nav3:
    if st.button("🛡️ Security Test", use_container_width=True):
        st.session_state.page = "Security Test"

with nav4:
    if st.button("ℹ️ About AES", use_container_width=True):
        st.session_state.page = "About AES"

st.divider()

# ==========================================================
# SUMMARY CARDS
# ==========================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="info-card">
        <h3>AES</h3>
        <p>Encryption Algorithm</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card">
        <h3>256 Bits</h3>
        <p>Key Length</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-card">
        <h3>GCM</h3>
        <p>Encryption Mode</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="info-card">
        <h3>Authenticated</h3>
        <p>Integrity Protection</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# 1. ENCRYPT FILE
# ==========================================================
if st.session_state.page == "Encrypt File":

    st.markdown(
        '<div class="section-heading">🔒 Encrypt Your File</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a file to encrypt it using AES-256-GCM. "
        "Download the encrypted file and its keys."
    )

    uploaded_file = st.file_uploader(
        "Choose a file to encrypt",
        key="encrypt_upload"
    )

    if st.button(
        "🔐 Encrypt File",
        type="primary",
        use_container_width=True,
        key="encrypt_button"
    ):
        if uploaded_file is None:
            st.warning("Please upload a file first.")

        else:
            file_data = uploaded_file.getvalue()

            # Generate a fresh 256-bit key and 12-byte nonce
            key = AESGCM.generate_key(bit_length=256)
            nonce = os.urandom(12)

            # Encrypt using AES-256-GCM
            ciphertext = AESGCM(key).encrypt(
                nonce,
                file_data,
                None
            )

            # Format: nonce + ciphertext + authentication tag
            encrypted_data = nonce + ciphertext

            # Generate an intentionally incorrect demonstration key
            tampered_key = bytearray(key)
            tampered_key[0] ^= 1
            tampered_key = bytes(tampered_key)

            # Save results in session state
            st.session_state.enc_result = encrypted_data
            st.session_state.enc_key = key
            st.session_state.tampered_key = tampered_key
            st.session_state.enc_name = uploaded_file.name

            st.success("File encrypted successfully!")

            st.info(
                "Download the encrypted file and original key. "
                "Keep the original key secret and safe."
            )

    # Display downloads after encryption
    if "enc_result" in st.session_state:

        st.subheader("📥 Download Your Files")

        original_name = st.session_state.enc_name
        encrypted_name = original_name + ".enc"

        d1, d2, d3 = st.columns(3)

        with d1:
            st.download_button(
                "⬇️ Encrypted File",
                data=st.session_state.enc_result,
                file_name=encrypted_name,
                mime="application/octet-stream",
                use_container_width=True,
                key="download_encrypted"
            )

        with d2:
            st.download_button(
                "🔑 Original Key",
                data=st.session_state.enc_key,
                file_name="aes_key.key",
                mime="application/octet-stream",
                use_container_width=True,
                key="download_original_key"
            )

        with d3:
            st.download_button(
                "🧪 Tampered Key",
                data=st.session_state.tampered_key,
                file_name="tampered_key.key",
                mime="application/octet-stream",
                use_container_width=True,
                key="download_tampered_key"
            )

        st.markdown("""
        <div class="security-note">
            <strong>🛡️ Security Testing Note</strong><br>
            <span>
                The tampered key is intentionally incorrect and is used
                only to demonstrate authentication failure.
            </span>
        </div>
        """, unsafe_allow_html=True)


# ==========================================================
# 2. DECRYPT FILE
# ==========================================================
elif st.session_state.page == "Decrypt File":

    st.markdown(
        '<div class="section-heading">🔓 Decrypt Your File</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload the encrypted .enc file and its matching "
        "original aes_key.key file."
    )

    encrypted_upload = st.file_uploader(
        "Upload encrypted .enc file",
        key="decrypt_file"
    )

    key_upload = st.file_uploader(
        "Upload original .key file",
        key="decrypt_key"
    )

    if st.button(
        "🔓 Decrypt File",
        type="primary",
        use_container_width=True,
        key="decrypt_button"
    ):
        if encrypted_upload is None or key_upload is None:
            st.warning(
                "Please upload both the encrypted file and the key."
            )

        else:
            encrypted_data = encrypted_upload.getvalue()
            key = key_upload.getvalue()

            if len(key) != 32:
                st.error(
                    "Invalid key. An AES-256 key must be exactly 32 bytes."
                )

            elif len(encrypted_data) < 28:
                st.error(
                    "The encrypted file is invalid or incomplete."
                )

            else:
                nonce = encrypted_data[:12]
                ciphertext = encrypted_data[12:]

                try:
                    decrypted_data = AESGCM(key).decrypt(
                        nonce,
                        ciphertext,
                        None
                    )

                    st.success(
                        "Decryption successful! Authentication verified."
                    )

                    original_name = encrypted_upload.name

                    if original_name.endswith(".enc"):
                        output_name = original_name[:-4]
                    else:
                        output_name = "decrypted_file"

                    st.download_button(
                        "⬇️ Download Decrypted File",
                        data=decrypted_data,
                        file_name=output_name,
                        mime="application/octet-stream",
                        use_container_width=True,
                        key="download_decrypted"
                    )

                except Exception:
                    st.error(
                        "Decryption failed! The key may be incorrect, "
                        "or the encrypted file may have been modified."
                    )


# ==========================================================
# 3. SECURITY TEST
# ==========================================================
elif st.session_state.page == "Security Test":

    st.markdown(
        '<div class="section-heading">🛡️ Security Test</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Demonstrate that AES-GCM rejects an incorrect key "
        "and detects modified ciphertext."
    )

    test_type = st.radio(
        "Select a security test",
        [
            "Check key authentication",
            "Check ciphertext tampering"
        ],
        horizontal=True,
        key="security_test_type"
    )

    test_file = st.file_uploader(
        "Upload the original encrypted .enc file",
        key="security_test_file"
    )

    # ------------------------------------------------------
    # TEST A: KEY AUTHENTICATION
    # ------------------------------------------------------
    if test_type == "Check key authentication":

        original_key_file = st.file_uploader(
            "Upload original aes_key.key",
            type=["key"],
            key="test_original_key"
        )

        tampered_key_file = st.file_uploader(
            "Upload tampered_key.key",
            type=["key"],
            key="test_tampered_key"
        )

        if st.button(
            "🧪 Compare Both Keys",
            type="primary",
            use_container_width=True,
            key="compare_keys"
        ):
            if (
                test_file is None
                or original_key_file is None
                or tampered_key_file is None
            ):
                st.warning(
                    "Upload the encrypted file and both key files."
                )

            else:
                data = test_file.getvalue()
                original_key = original_key_file.getvalue()
                tampered_key = tampered_key_file.getvalue()

                if len(data) < 28:
                    st.error("The encrypted file is invalid.")

                elif (
                    len(original_key) != 32
                    or len(tampered_key) != 32
                ):
                    st.error(
                        "Both AES-256 keys must be exactly 32 bytes."
                    )

                elif original_key == tampered_key:
                    st.error(
                        "The keys are identical. Upload the correct "
                        "original and tampered key files."
                    )

                else:
                    nonce = data[:12]
                    ciphertext = data[12:]

                    original_valid = False

                    # Check original key
                    try:
                        AESGCM(original_key).decrypt(
                            nonce,
                            ciphertext,
                            None
                        )
                        original_valid = True

                        st.success(
                            "✅ ORIGINAL KEY: PASS — "
                            "authentication succeeded."
                        )

                    except Exception:
                        st.error(
                            "❌ ORIGINAL KEY: FAIL — use the key "
                            "that belongs to this encrypted file."
                        )

                    # Check tampered key only after original passes
                    if original_valid:
                        try:
                            AESGCM(tampered_key).decrypt(
                                nonce,
                                ciphertext,
                                None
                            )

                            st.error(
                                "⚠️ TAMPERED KEY: UNEXPECTED PASS — "
                                "check the uploaded files."
                            )

                        except Exception:
                            st.success(
                                "✅ TAMPERED KEY: REJECTED — "
                                "authentication failed as expected."
                            )


    # ------------------------------------------------------
    # TEST B: CIPHERTEXT TAMPERING
    # ------------------------------------------------------
    else:

        key_file = st.file_uploader(
            "Upload the ORIGINAL aes_key.key",
            type=["key"],
            key="ciphertext_test_key"
        )

        if st.button(
            "🧪 Test Ciphertext Integrity",
            type="primary",
            use_container_width=True,
            key="ciphertext_test_button"
        ):
            if test_file is None or key_file is None:
                st.warning(
                    "Upload the encrypted file and its original key."
                )

            else:
                data = test_file.getvalue()
                key = key_file.getvalue()

                if len(key) != 32:
                    st.error(
                        "Invalid AES-256 key. It must be 32 bytes."
                    )

                elif len(data) < 28:
                    st.error("The encrypted file is invalid.")

                else:
                    nonce = data[:12]
                    ciphertext = data[12:]

                    # Validate original file first
                    try:
                        AESGCM(key).decrypt(
                            nonce,
                            ciphertext,
                            None
                        )

                    except Exception:
                        st.error(
                            "Original file authentication failed. "
                            "Use the matching original key."
                        )

                    else:
                        st.success(
                            "✅ ORIGINAL FILE: PASS — "
                            "authentication succeeded."
                        )

                        # Flip one bit of the ciphertext
                        modified = bytearray(ciphertext)
                        modified[0] ^= 1

                        try:
                            AESGCM(key).decrypt(
                                nonce,
                                bytes(modified),
                                None
                            )

                            st.error(
                                "❌ TAMPERING TEST: FAIL — "
                                "modified data was accepted."
                            )

                        except Exception:
                            st.success(
                                "✅ TAMPERING TEST: PASS — "
                                "modified ciphertext was rejected."
                            )


# ==========================================================
# 4. ABOUT AES
# ==========================================================
elif st.session_state.page == "About AES":

    st.markdown(
        '<div class="section-heading">ℹ️ About AES-256-GCM</div>',
        unsafe_allow_html=True
    )

    st.subheader("What is AES?")

    st.write(
        "AES (Advanced Encryption Standard) is a symmetric "
        "encryption algorithm. The same secret key is used "
        "for encryption and decryption."
    )

    st.subheader("Why AES-256?")

    st.write(
        "AES-256 uses a 256-bit secret key, providing a large "
        "key space and strong protection when implemented correctly."
    )

    st.subheader("What is GCM?")

    st.write(
        "GCM stands for Galois/Counter Mode. It provides "
        "confidentiality and authentication, helping detect "
        "incorrect keys and modified encrypted data."
    )

    st.subheader("How this project works")

    st.markdown("""
    1. Upload a file.
    2. Generate a random 256-bit AES key and a 12-byte nonce.
    3. Encrypt the file using AES-GCM.
    4. Download the encrypted file and the original key.
    5. Test authentication using a deliberately modified key.
    6. Modify ciphertext to demonstrate tamper detection.
    7. Decrypt the original file using its matching key.
    """)

    st.warning(
        "Keep the original key secret and separate from the encrypted "
        "file. Anyone with the original key can decrypt the file."
    )


# ==========================================================
# FOOTER
# ==========================================================
st.divider()

st.markdown("""
<div class="custom-footer">
    Cryptography and Network Security Project |
    AES-256-GCM | Developed by Impana P
</div>
""", unsafe_allow_html=True)