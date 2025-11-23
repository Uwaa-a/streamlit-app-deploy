import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 手順4-4: 環境変数の読み込み
# ローカルで実行する際は.envファイルからAPIキーを読み込みます
load_dotenv()

# Streamlit Community Cloudの「Secrets」からAPIキーを取得する対応
# (ローカルでは.envが優先され、デプロイ後はSecretsが優先されるようにします)
if not os.getenv("OPENAI_API_KEY"):
    # デプロイ環境などで環境変数がない場合、Streamlitのsecretsを確認
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# ---------------------------------------------------------
# 関数定義: 入力テキストと役割を受け取り、LLMの回答を返す
# ---------------------------------------------------------
def get_llm_response(user_input, role_selection):
    """
    ユーザーの入力と選択された役割に基づいてLLMから回答を取得する関数
    """
    
    # 1. モデルのインスタンス化
    # 安価で高速な gpt-3.5-turbo を使用（必要に応じて gpt-4 等に変更可）
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    # 2. 役割に応じたシステムメッセージの切り替え
    if role_selection == "頼れるベテランエンジニア":
        system_prompt = "あなたは経験豊富なベテランエンジニアです。技術的な用語を適切に使い、簡潔かつ論理的に回答してください。語尾は「だ・である」調で話してください。"
    elif role_selection == "優しいうさぎの先生":
        system_prompt = "あなたは幼稚園の先生をしている優しいうさぎです。難しい言葉は使わず、絵文字を使いながらとても優しく教えてください。語尾は「〜だぴょん」や「〜だよ」としてください。"
    else:
        # デフォルト
        system_prompt = "あなたは役に立つアシスタントです。"

    # 3. メッセージリストの作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    # 4. LLMへの問い合わせと回答の取得
    response = llm.invoke(messages)
    
    return response.content

# ---------------------------------------------------------
# Streamlit UI の構築
# ---------------------------------------------------------

# アプリのタイトル
st.title("🤖 AI専門家チャットアプリ")

# アプリの概要・操作説明
st.markdown("""
### 概要
このアプリでは、AIが異なる専門家になりきってあなたの質問に答えます。
設定によって回答の雰囲気がガラッと変わるのを体験してください。

### 使い方
1. **相談相手（専門家）** をラジオボタンで選んでください。
2. **質問内容** をテキストボックスに入力してEnterキーを押してください。
""")

st.markdown("---") # 区切り線

# ラジオボタンで専門家の種類を選択
expert_role = st.radio(
    "誰に相談しますか？",
    ("頼れるベテランエンジニア", "優しいうさぎの先生")
)

# 入力フォーム
input_text = st.text_input("質問を入力してください", placeholder="例：Pythonって何ですか？")

# 入力があった場合に実行
if input_text:
    # 読み込み中の表示
    with st.spinner("AIが考え中..."):
        # 関数を呼び出して結果を取得
        answer = get_llm_response(input_text, expert_role)
    
    # 結果の表示
    st.success("回答が届きました！")
    st.write(answer)