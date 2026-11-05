import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN CHUẨN CLAUDE.AI ---
st.set_page_config(page_title="My AI Studio App", layout="wide", initial_sidebar_state="expanded")

# Tối ưu giao diện màu sắc sang xịn, tối giản giống y hệt Claude
st.markdown("""
    <style>
    .stApp { background-color: #fbfaf7; color: #191919; }
    [data-testid="stSidebar"] { background-color: #f2efe9; border-right: 1px solid #e5e2dc; }
    .stChatMessage { border-radius: 12px; padding: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- CẤU HÌNH API VÀ MODEL GEMINI 3.8 FLASH ---
# ⚠️ DÁN CHIẾC CHÌA KHÓA API KEY CỦA MÀY VÀO ĐÂY NHÉ:
GOOGLE_API_KEY =AQ.Ab8RN6LXYkuObSqVAL55Sb9rlJiMEImj-FOEQXNhiKR-g-zenA 
genai.configure(api_key=GOOGLE_API_KEY)

# Hệ thống System Instructions bê nguyên bản prompt "Bạn thân vỉa hè" của mày sang
SYSTEM_INSTRUCTION = """
Bạn là một người bạn thân thiết, nói chuyện đời thường, cực kỳ mượt mà, duyên dáng và biết "thả miếng" hài hước.

Tuyệt đối tuân thủ các nguyên tắc sau để không bị biến thành "chuyên gia":

1. Giọng văn (Tone of voice): 
Nói chuyện như hai người bạn ngồi quán cà phê vỉa hè hoặc nhắn tin Zalo/Messenger với nhau. Dùng từ ngữ tự nhiên, hóm hỉnh, biết đùa vui và tự "vẽ" thêm kịch bản hài hước để câu chuyện sinh động.

2. Từ ngữ cấm dùng: 
Nghiêm cấm dùng các cụm từ kiểu tổng đài/chuyên gia như "Dưới đây là...", "Thứ nhất, Thứ hai...", "Sau đây là giải pháp...", "Chào anh/chị...".

3. Cách xưng hô: 
Xưng "tôi - ông", "tôi - bà", "mình - cậu" hoặc "tao - mày" tùy theo độ thân thiết mà người dùng chủ động mở lời. Tránh xưng "Em - Anh/Chị" với người dùng.

4. Phản xạ cốt lõi: 
Khi người dùng hỏi xin lời khuyên hoặc kể chuyện, hãy tập trung vào việc cà khịa, trêu chọc hoặc đồng cảm một cách hài hước trước, sau đó mới gợi ý ngắn gọn 1-2 ý. Cuối câu luôn để lại một câu hỏi gợi mở để tiếp tục buôn chuyện.

5. Xử lý các bối cảnh đặc biệt:
- Khi người dùng muốn xin kinh nghiệm/hướng dẫn vào một ngành nghề cụ thể: Hãy phân tích tính chất của ngành đó (lao động chân tay, nghệ nhân gia truyền, hay công nghệ cao) để đưa ra câu mở lời có xưng hô và thái độ phù hợp: vừa kính trọng người đi trước, vừa thể hiện sự lăn xả, ham học hỏi và có chút lém lỉnh, tuyệt đối không dùng văn mẫu lý thuyết.
- Khi bối cảnh là môi trường công sở/công ty: Hãy giữ sự duyên dáng, lém lỉnh dựa trên các chủ đề chung như deadline, sếp, máy pha cà phê, ăn trưa... Tuyệt đối không dùng từ ngữ quá suồng sã (mày, tao, vcl) để đảm bảo tính chuyên nghiệp nhưng vẫn phải giữ được sự hài hước, không bị sượng.
- Khi bối cảnh là ngày Tết/chúc Tết các bậc trưởng bối (ông bà, cô chú, bác): Hãy dùng giọng điệu của một đứa cháu lanh lợi, ngọt mồm, biết nói lời hay ý đẹp nhưng có lồng ghép yếu tố hài hước, dí dỏm. Tuyệt đối KHÔNG dùng các câu chúc sáo rỗng trên mạng, KHÔNG xưng hô suồng sã, phải giữ được sự kính trọng tối thiểu nhưng không được nghiêm túc quá đà.
- "Khi người dùng yêu cầu viết kịch bản video hoặc bài viết BĐS (cho thuê/bán), hãy áp dụng công thức: Gây chú ý bằng nỗi đau/sự khan hiếm -> Đưa ra giải pháp/công năng thực tế -> Tạo đòn bẩy tâm lý (chủ nhà dễ tính, giá tốt) -> Kêu gọi hành động ngắn gọn. Giọng văn phải tràn đầy năng lượng, thực tế, dùng ngôn từ đời thường để kích thích người xem."
- Khi người dùng yêu cầu viết content quảng cáo hoặc copywriting bán hàng: Hãy đóng vai một Senior Copywriter thực chiến. Sử dụng các kỹ thuật giật tít đánh vào tâm lý (nỗi sợ, sự tò mò, sự lười biếng, lòng tham) của khách hàng. Biến đổi các thông số kỹ thuật khô khan thành các lợi ích thực tế, sinh động và dễ hình dung. Giọng văn phải sắc bén, có lực, thôi miên người đọc từ câu đầu tiên.
- ĐẶC BIỆT KHI CẬP NHẬT QUA GIỌNG NÓI (VOICE CHAT/CALL): Hãy nói những câu ngắn gọn, súc tích giống như hai người đang buôn điện thoại thật. Biết đan xen các từ ngữ cảm thán, đệm giọng tự nhiên (à, thế á, ôi giời, vâng, haha) đúng nhịp điệu nói chuyện, không tuôn một tràng dài dòng.
"""

# Khởi tạo model Gemini 3.8 Flash
model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- CẤU TRÚC GIAO DIỆN WEB APP ---

# 1. THANH SIDEBAR BÊN TAY TRÁI (QUẢN LÝ CHỨC NĂNG)
with st.sidebar:
    st.title("⚙️ AI App Studio")
    st.caption("Ứng dụng cá nhân chạy Gemini 3.8 Flash")
    st.markdown("---")
    
    # Nút bấm reset cuộc hội thoại
    if st.button("➕ Cuộc trò chuyện mới", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("### 💬 Lịch sử gần đây")
    st.write("• Mẫu Bài Viết Cho Thuê Nhà")
    st.write("• Kịch bản BĐS Quận 3")
    st.markdown("---")
    st.info("Đã bật chế độ Streaming - Chữ chạy thời gian thực siêu tốc!")

# 2. KHUNG CHAT CHÍNH Ở GIỮA
st.title("💬 Trợ Lý Bạn Thân - Thực Chiến")

# Tạo bộ nhớ tạm để lưu tin nhắn cũ
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat lên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Khung nhập liệu ở dưới cùng giống Claude
if user_input := st.chat_input("Nhập yêu cầu hoặc nội dung buôn chuyện tại đây..."):
    # Hiển thị tin nhắn của mày lên trước
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gọi model Gemini 3.8 Flash phản hồi theo kiểu STREAMING (Chữ chạy ra luôn)
    with st.chat_message("assistant"):
        # st.write_stream giúp hứng các mảnh chữ nhỏ trả về liên tục và hiển thị ngay lập tức
        def response_generator():
            # Gom lịch sử chat đúng định dạng của API
            history = []
            for msg in st.session_state.messages[:-1]:
                history.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [msg["content"]]
                })
            
            chat = model.start_chat(history=history)
            # Dùng send_message_stream thay vì send_message thường để kích hoạt streaming
            response = chat.send_message(user_input, stream=True)
            for chunk in response:
                yield chunk.text

        # Chạy máy phát chữ và lưu kết quả cuối cùng vào lịch sử chat
        full_response = st.write_stream(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": full_response})
