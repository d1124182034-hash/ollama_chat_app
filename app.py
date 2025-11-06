# import streamlit as st
# from ollama import Client

# # ---------------- Streamlit 設定 ----------------
# st.set_page_config(page_title="Ollama Cloud Chat", page_icon="🤖")
# st.title("💬 Chat with Ollama Cloud Model")

# # ---------------- Ollama Cloud Client ----------------
# api_key = st.secrets.get("OLLAMA_API_KEY", "")
# if not api_key:
#     st.error("⚠️ OLLAMA_API_KEY 未設定，請先在 Streamlit Secrets 填入 API Key")
#     st.stop()

# client = Client(
#     host="https://ollama.com",
#     headers={'Authorization': f'Bearer {api_key}'}
# )

# # ---------------- 聊天訊息紀錄 ----------------
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # ---------------- 使用者輸入 callback ----------------
# def send_message():
#     user_input = st.session_state["input"]
#     if not user_input.strip():
#         return

#     # 加入使用者訊息
#     st.session_state["messages"].append({"role": "user", "content": user_input})

#     # 呼叫 Ollama 雲端模型
#     assistant_response = ""
#     for part in client.chat("gpt-oss:120b-cloud", messages=st.session_state["messages"], stream=True):
#         assistant_response += part["message"]["content"]

#     # 加入助理訊息
#     st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

#     # 清空輸入欄
#     st.session_state["input"] = ""

# # ---------------- 顯示聊天訊息 ----------------
# for msg in st.session_state["messages"]:
#     role = "You" if msg["role"] == "user" else "Ollama"
#     st.write(f"**{role}:** {msg['content']}")

# # ---------------- 輸入欄位 ----------------
# st.text_input("輸入訊息...", key="input", on_change=send_message)

# # ---------------- 清除聊天歷史 ----------------
# if st.button("清除聊天紀錄"):
#     st.session_state["messages"] = []









# import streamlit as st
# import json
# import os
# from ollama import chat  # 使用 Ollama Python SDK

# USER_FILE = "users.json"

# # ---------- 使用者資料 ----------
# def load_users():
#     if os.path.exists(USER_FILE):
#         with open(USER_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_users(users):
#     with open(USER_FILE, "w") as f:
#         json.dump(users, f, indent=4)

# # ---------- 登入頁 ----------
# def login(users):
#     st.header("🔑 使用者登入")
#     username = st.text_input("帳號")
#     password = st.text_input("密碼", type="password")

#     if st.button("登入"):
#         if username in users and users[username]["password"] == password:
#             st.session_state["user"] = username
#             st.success(f"歡迎回來，{username}！")
#             st.rerun()  # 自動切換到 Ollama 聊天畫面
#         else:
#             st.error("帳號或密碼錯誤")

# # ---------- 註冊頁 ----------
# def register(users):
#     st.header("🧩 創建帳號")
#     new_user = st.text_input("新帳號")
#     new_pass = st.text_input("新密碼", type="password")
#     confirm = st.text_input("確認密碼", type="password")

#     if st.button("註冊"):
#         if new_user in users:
#             st.warning("此帳號已存在")
#         elif new_pass != confirm:
#             st.warning("兩次密碼不一致")
#         elif len(new_user) == 0 or len(new_pass) == 0:
#             st.warning("帳號或密碼不可為空")
#         else:
#             users[new_user] = {"password": new_pass}
#             save_users(users)
#             st.success("註冊成功！請回登入頁面")

# # ---------- Ollama 聊天頁 ----------
# def ollama_chat():
#     st.title("🤖 Chat with Llama 3 (via Ollama)")
#     st.sidebar.success(f"已登入帳號：{st.session_state['user']}")

#     # 登出按鈕
#     if st.sidebar.button("登出"):
#         st.session_state.pop("user")
#         st.session_state.pop("messages", None)
#         st.rerun()

#     # 建立聊天歷史
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # 顯示聊天記錄
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # 使用者輸入
#     if prompt := st.chat_input("輸入訊息..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # 呼叫 Ollama
#         try:
#             response = chat(
#                 model="llama3:latest",
#                 messages=st.session_state.messages,
#                 stream=False
#             )
#             assistant_msg = response["message"]["content"]
#         except Exception as e:
#             assistant_msg = f"⚠️ Ollama 錯誤：{e}"

#         # 顯示 AI 回覆
#         st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
#         with st.chat_message("assistant"):
#             st.write(assistant_msg)

# # ---------- 主程式 ----------
# def main():
#     st.set_page_config(page_title="登入 + Ollama 聊天", page_icon="🤖")
#     users = load_users()

#     if "user" in st.session_state:
#         ollama_chat()
#     else:
#         st.title("🐍 Streamlit 登入系統")
#         menu = ["登入", "註冊"]
#         choice = st.sidebar.selectbox("選單", menu)
#         if choice == "登入":
#             login(users)
#         else:
#             register(users)

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import os
from ollama import Client  # 或 from ollama import chat，看你使用哪個

# ---------------- 設定 ----------------
st.set_page_config(page_title="Ollama Cloud Chat", page_icon="🤖")
USER_FILE = "users.json"

# ---------------- 使用者資料 ----------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------------- 登入 ----------------
def login(users):
    st.header("🔑 使用者登入")
    username = st.text_input("帳號", key="login_user")
    password = st.text_input("密碼", type="password", key="login_pass")

    if st.button("登入"):
        if username in users and users[username]["password"] == password:
            st.session_state["user"] = username
            st.success(f"歡迎回來，{username}！")
            st.rerun()
        else:
            st.error("帳號或密碼錯誤")

# ---------------- 註冊 ----------------
def register(users):
    st.header("🧩 創建帳號")
    new_user = st.text_input("新帳號", key="reg_user")
    new_pass = st.text_input("新密碼", type="password", key="reg_pass")
    confirm = st.text_input("確認密碼", type="password", key="reg_confirm")

    if st.button("註冊"):
        if new_user in users:
            st.warning("此帳號已存在")
        elif new_pass != confirm:
            st.warning("兩次密碼不一致")
        elif len(new_user) == 0 or len(new_pass) == 0:
            st.warning("帳號或密碼不可為空")
        else:
            users[new_user] = {"password": new_pass}
            save_users(users)
            st.success("註冊成功！請回登入頁面")

# ---------------- Ollama 聊天 ----------------
def ollama_chat():
    st.title("💬 Chat with Ollama Cloud Model")
    st.sidebar.success(f"已登入帳號：{st.session_state['user']}")

    # 登出
    if st.sidebar.button("登出"):
        st.session_state.pop("user")
        st.session_state.pop("messages", None)
        st.rerun()

    # 取得 API Key
    api_key = st.secrets.get("OLLAMA_API_KEY", "")
    if not api_key:
        st.error("⚠️ OLLAMA_API_KEY 未設定")
        st.stop()

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': f'Bearer {api_key}'}
    )

    # 聊天歷史
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 顯示聊天紀錄
    for msg in st.session_state["messages"]:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.write(msg["content"])

    # 使用者輸入 (改成 st.chat_input)
    if prompt := st.chat_input("輸入訊息..."):
        # 加入使用者訊息
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # 呼叫 Ollama
        assistant_response = ""
        try:
            for part in client.chat("gpt-oss:120b-cloud", messages=st.session_state["messages"], stream=True):
                assistant_response += part["message"]["content"]
        except Exception as e:
            assistant_response = f"⚠️ Ollama 錯誤：{e}"

        # 顯示 AI 回覆
        st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.write(assistant_response)

    # 清除聊天歷史
    if st.button("清除聊天紀錄"):
        st.session_state["messages"] = []

# ---------------- 主程式 ----------------
def main():
    users = load_users()
    if "user" in st.session_state:
        ollama_chat()
    else:
        st.title("🐍 Streamlit 登入系統")
        menu = ["登入", "註冊"]
        choice = st.sidebar.selectbox("選單", menu)
        if choice == "登入":
            login(users)
        else:
            register(users)

if __name__ == "__main__":
    main()
