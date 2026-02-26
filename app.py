import streamlit as st
import pandas as pd
import random

# --- CẤU HÌNH GIAO DIỆN SIÊU TO ---
st.set_page_config(page_title="Học Tiếng Nga Pro", layout="centered")

st.markdown("""
    <style>
    /* Làm cho toàn bộ văn bản trong app to lên */
    html, body, [class*="st-"] {
        font-size: 24px !important;
    }
    /* Tiêu đề chính */
    .main-title {
        font-size: 45px !important;
        color: #1a237e;
        text-align: center;
        font-weight: bold;
        margin-bottom: 30px;
    }
    /* Khung hiển thị từ tiếng Việt */
    .viet-box {
        background-color: #fff3e0;
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #ff9800;
        text-align: center;
        margin-bottom: 20px;
    }
    .viet-word {
        font-size: 55px !important;
        color: #d84315;
        font-weight: bold;
    }
    /* Ô nhập liệu */
    .stTextInput input {
        font-size: 35px !important;
        height: 70px !important;
        text-align: center;
    }
    /* Nút bấm */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 25px !important;
        background-color: #2e7d32 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🇷🇺 ÔN TẬP TIẾNG NGA</p>', unsafe_allow_html=True)

# --- XỬ LÝ DỮ LIỆU ---
uploaded_file = st.file_uploader("📂 Bấm vào đây để nạp file Excel/CSV", type=["xlsx", "csv"])

if uploaded_file:
    if 'data' not in st.session_state:
        try:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
            st.session_state.data = df.values.tolist()
            random.shuffle(st.session_state.data)
            st.session_state.idx = 0
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")

    if 'data' in st.session_state and st.session_state.idx < len(st.session_state.data):
        row = st.session_state.data[st.session_state.idx]
        nga_target = str(row[0]).strip()
        viet_target = str(row[1]).strip()
        cau_mau = str(row[2]).strip() if len(row) > 2 and str(row[2]) != 'nan' else ""

        # Hiển thị từ tiếng Việt
        st.markdown(f'<div class="viet-box"><p>DỊCH SANG TIẾNG NGA:</p><p class="viet-word">{viet_target.upper()}</p></div>', unsafe_allow_html=True)

        # Nhập liệu
        user_input = st.text_input("GÕ TIẾNG NGA VÀO ĐÂY:", key=f"input_{st.session_state.idx}").strip()

        if user_input:
            if user_input.lower() == nga_target.lower():
                st.balloons()
                st.success(f"✅ CHÍNH XÁC: {nga_target.upper()}")
                if cau_mau:
                    st.info(f"📝 VÍ DỤ: {cau_mau}")
                else:
                    st.info(f"📝 CÂU MẪU: Наш {nga_target.lower()} готов.")
                
                if st.button("TIẾP THEO ➡️"):
                    st.session_state.idx += 1
                    st.rerun()
            else:
                st.error("❌ SAI RỒI, THỬ LẠI!")
                # Gợi ý
                hint = "".join([nga_target[i] if i < len(user_input) and user_input[i].lower() == nga_target[i].lower() else " _ " for i in range(len(nga_target))])
                st.warning(f"GỢI Ý: {hint}")
    elif 'data' in st.session_state:
        st.success("🎉 CHÚC MỪNG! BẠN ĐÃ HOÀN THÀNH BỘ TỪ NÀY.")
        if st.button("HỌC LẠI TỪ ĐẦU"):
            del st.session_state.data
            st.rerun()
else:
    st.info("Vui lòng nạp file Excel từ Zalo của bạn để bắt đầu học.")
