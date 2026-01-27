import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

MAP_PATH = "assets/서울월드컵경기장.jpg"
PHOTO_ZONE = "assets/포토존.jpg"

st.set_page_config(
    page_title="WELCOME to FC서울 (2번 출입구)",
    layout="wide",
)

def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded = f.read()
    import base64
    encoded_bg = base64.b64encode(encoded).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_bg}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#set_background("assets/배경.png")

KST = ZoneInfo("Asia/Seoul")

CONFIG = {
    "match": {
        "home": "FC서울",
        "away": "상대팀",
        "date": "2026-04-23",
        "kickoff": "05:30",
        "venue": "서울월드컵경기장(상암)",
    },


    "score_max": 7,

    "watch_points": [
        "이기는 팀이 우승에 가까워지는, 사실상의 결승전.",
        "전반 시작 후 첫 10분, 서울이 얼마나 적극적으로 공을 되찾으려 드는지 주목해 보세요.",
        "송민규가 공을 갖지 않을 때의 위치를 살펴보세요.",
    ],


    "chants": [
        {"title": "우리의 서울", "lyrics": "서울 우리의 서울 너와 나 함께 오늘을 기억할 거야\n서울 우리의 서울 언제나 우리 내일을 노래할 거야\n서울 서울 서울 서울\n수많은 밤을 보내며 너와 나 지쳐갈 때면\n우린 때로 끝을 바라겠지만   그 어둠 속에서\n아파했던 맘은 언젠가는 다 희미해질 거야\n메마른 밤의 끝에서 조금은 힘들겠지만\n똑같은 어젠 오지 않을 거라고\n나의 손을 잡아 이 밤을 열고\n밝은 빛을 찾아   우린 나아갈 거야 함께\n서울 우리의 서울 너와 나 함께 오늘을 기억할 거야\n서울 우리의 서울 언제나 우리 내일을 노래할 거야\n서울 서울 서울 서울\n아침을 맞이하고서 너와 나 마주볼 때면\n슬픔 가득한 기억도 있겠지만\n그 시간 속에서 너와 나 함께면\n두려움은 없을 것만 같아 우린\n서울 우리의 서울 너와 나 함께 오늘을 기억할 거야\n서울 우리의 서울 언제나 우리 내일을 노래할 거야\n서울 서울 서울 서울\n서울 우리의 서울 너와 나 함께 오늘을 기억할 거야\n서울 우리의 서울 언제나 우리 내일을 노래할 거야\n서울 우리의 서울 너와 나 함께 오늘을 기억할 거야\n서울 우리의 서울 언제나 우리 내일을 노래할 거야\n서울 서울 서울 서울"},
        {"title": "FC서울의 승리를", "lyrics": "|: FC서울의 승리를\nFC서울의 승리를\nFC서울 오늘 승리하리라\nFC서울의 승리를\nFC서울 알레오 (서울)\nFC서울 알레오 (서울)\nFC서울 알레알레오\nFC서울 알레오 (서울) :|\n|: 알레 알레 알레오 알레오 (서울)\n알레 알레 알레오 알레오 (서울)\n알레 알레 알레오 알레 알레 알레오\n알레 알레 알레오 알레오 (서울) :|"},
    ],
    "chants_link": "https://www.instagram.com/fcseoul/",

    "key_players": [
        {"name": "송민규", "role": "(공격수)", "one_liner": "빠른 침투과 현란한 드리블"},
        {"name": "김진수", "role": "(수비수)", "one_liner": "노련한 수비와 날카로운 크로스"},
        {"name": "강현무", "role": "(골키퍼)", "one_liner": "뛰어난 반사신경과 안정적인 수비"},
    ],


    "halftime_short": {
        "question": "하프타임 퀴즈",
        "max_chars": 10,
    },

    "impressive_players": ["송민규", "문선민", "정승원", "조영욱"],

    "mom_candidates": ["송민규", "문선민", "정승원", "조영욱"],
}


DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

RESP_PATH = os.path.join(DATA_DIR, "responses.csv")
PRED_PATH = os.path.join(DATA_DIR, "predictions.csv")
QUIZ_PATH = os.path.join(DATA_DIR, "halftime.csv")
MOM_PATH = os.path.join(DATA_DIR, "mom.csv")


def now_kst() -> datetime:
    return datetime.now(tz=KST)

def now_kst_str() -> str:
    return now_kst().strftime("%Y-%m-%d %H:%M:%S")

def parse_kickoff_kst(match_cfg: dict) -> datetime:
    dt_str = f"{match_cfg['date']} {match_cfg['kickoff']}:00"
    # timezone-aware KST
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=KST)

def append_row(csv_path: str, row: dict):
    df = pd.DataFrame([row])
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

def load_csv(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    return pd.read_csv(csv_path, encoding="utf-8-sig")


m = CONFIG["match"]
kickoff_dt = parse_kickoff_kst(m)
is_before_kickoff = now_kst() < kickoff_dt

st.title("WELCOME to FC서울 (2번 출입구)")
st.caption(
    f"{m['date']}  |  {m['home']} vs {m['away']}  |  킥오프 {m['kickoff']} (KST)  |  {m['venue']}"
)

with st.container(border=True):
    st.write(f"현재 시각(KST): **{now_kst().strftime('%Y-%m-%d %H:%M:%S')}**")
    st.write(f"킥오프(KST): **{kickoff_dt.strftime('%Y-%m-%d %H:%M:%S')}**")
    if is_before_kickoff:
        st.success("스코어 예측 제출 가능")
    else:
        st.warning("스코어 예측은 **경기 시작 전까지만** 제출 가능합니다.")

st.divider()


with st.container(border=True):
    st.subheader("이용자 확인")
    st.write("스탬프/추첨 집계를 위해 **닉네임 + 휴대폰 뒤 4자리**만 입력해 주세요.")
    colA, colB, colC = st.columns([2, 1, 1])

    with colA:
        nickname = st.text_input("닉네임", placeholder="예: seoul_fan")
    with colB:
        phone4 = st.text_input("휴대폰 뒤 4자리", max_chars=4, placeholder="1234")
    with colC:
        is_new_fan = st.selectbox("신규 팬인가요?", ["신규", "기존"])

    if nickname.strip() == "":
        st.warning("닉네임을 입력하면 참여 기능이 활성화됩니다.")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Red Seoul", "Red Seoul Mission", "Today's Match", "경기장 정보"])

# 탭 1: 오늘의 이벤트

with tab1:
    t_pred, t_half= st.tabs(["경기 전", "하프타임"])

    with t_pred:
        st.subheader("경기 전")

        with st.form("form_prediction"):
            pred = st.radio(
                "결과를 선택하세요 (승/무/패)",
                ["FC서울 승", "무승부", "FC서울 패"],
                horizontal=True,
                disabled=not is_before_kickoff,
            )

            score_opts = ["선택하세요"] + list(range(0, CONFIG["score_max"] + 1))

            st.caption("스코어를 예측하세요.")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                seoul_goals = st.selectbox(
                    "서울 득점",
                    score_opts,
                    index=0,
                    disabled=not is_before_kickoff,
                )
            with col_s2:
                seoul_conceded = st.selectbox(
                    "서울 실점",
                    score_opts,
                    index=0,
                    disabled=not is_before_kickoff,
                )

            if seoul_goals > seoul_conceded:
                auto_pred = "FC서울 승"
            elif seoul_goals == seoul_conceded:
                auto_pred = "무승부"
            else:
                auto_pred = "FC서울 패"

            mom_opts = ["선택하세요"] + CONFIG["mom_candidates"]

            pred_pick = st.selectbox(
                "오늘의 Man of the Match를 예측하세요",
                mom_opts,
                index=0
                )

            pred_goal = st.selectbox(
                "오늘 경기 첫 득점 선수를 예측하세요",
                mom_opts,
                index=0
                )

            submitted = st.form_submit_button(
                "예측 제출",
                
                disabled=not is_before_kickoff
            )    
            

        final_mom = ""

        with st.form("form_cheer"):
            cheer_custom = ""

            comment = st.text_input("FC 서울을 위한 응원 한마디")
            submitted_c = st.form_submit_button("제출")

    with t_half:
        st.subheader("하프타임 퀴즈")

        final_player = ""    

        with st.form("form_halftime"):
            short_q = st.text_input(
                CONFIG["halftime_short"]["question"],
                max_chars=CONFIG["halftime_short"]["max_chars"],
            )


            impressive_custom = ""
            submitted_h = st.form_submit_button("제출")

# 탭 2: 오늘의 정보
with tab2:
    b1, b2, b3 = st.columns([1,1,1],gap="large")
    
    with b1:
        st.subheader("포토존 응원 인증")
        
        if os.path.exists(PHOTO_ZONE):
            img = Image.open(PHOTO_ZONE)
            st.image(img, caption="포토존 위치", use_container_width=True)
        
        with st.container(border=True):
            st.markdown("**포토존**")
            st.write("3번 출입구 옆 마스코트 인형")
        
        with st.form("form_photozone"):
            uploaded_photo = st.file_uploader(
                "응원 포즈 사진을 업로드해주세요",
                type=["jpg", "jpeg", "png"]
                )

            submitted_photo = st.form_submit_button("제출")
    
    with b2:
        st.subheader("FC서울 역사 퀴즈 (단답형)") 
        
        with st.form("form_quiz1"):
            quiz_custom1 = ""

            comment1 = st.text_input("FC서울의 창단년도는?")
            submitted_q1 = st.form_submit_button("제출")
            
    with b3:
        st.subheader("FC서울 역사 퀴즈 (O / X)") 
        
        with st.form("form_quiz2"):
            quiz_custom2 = ""

            comment2 = st.radio(
                "FC서울의 창단년도는 1983년이다.",
                ["O", "X"],
                horizontal=True
                )
            submitted_q2 = st.form_submit_button("제출")            
            
# 탭 2: 오늘의 정보
with tab3:
    c1, c2, c3 = st.columns([1, 1, 1], gap="large")

    with c1:
        st.subheader("오늘의 관전 포인트")
        for wp in CONFIG["watch_points"]:
            with st.container(border=True):
                st.write(wp)

    with c2:
        st.subheader("오늘의 응원가")
        if CONFIG.get("chants_link"):
            st.link_button("응원가 영상/릴스 보기", CONFIG["chants_link"])
        for ch in CONFIG["chants"]:
            with st.container(border=True):
                st.markdown(f"**{ch['title']}**")
                st.text(ch["lyrics"])

    with c3:
        st.subheader("키플레이어 소개")
        for kp in CONFIG["key_players"]:
            with st.container(border=True):
                st.markdown(f"**{kp['name']}**  ·  {kp['role']}")
                st.write(kp["one_liner"])


# 탭 3: 경기장 정보
with tab4:
    left2, right2 = st.columns([1.2, 1], gap="large")
    
    with left2:
        st.subheader("서울월드컵경기장 지도")

        # (1) 구역별 경로 지도 매핑
        ROUTE_MAPS = {
            "구역 1": "assets/routes/2-A.jpg",
            "구역 2": "assets/routes/2-B.jpg",
            "구역 3": "assets/routes/2-C.jpg",
        }

        # (2) 구역 선택 UI
        selected_zone = st.selectbox(
            "출입구 2 기준 목적지를 선택하세요",
            ["전체 지도 보기"] + list(ROUTE_MAPS.keys())
        )
        
        if selected_zone == "전체 지도 보기":
            if os.path.exists(MAP_PATH):
                img = Image.open(MAP_PATH)
                st.image(img, caption="서울월드컵경기장 전체 지도", use_container_width=True)
            else:
                st.warning("전체 지도 이미지가 없습니다. 경로를 확인하세요.")
        else:
            route_img_path = ROUTE_MAPS[selected_zone]
            if os.path.exists(route_img_path):
                img = Image.open(route_img_path)
                st.image(
                    img,
                    caption=f"출입구 2 → {selected_zone}",
                    use_container_width=True
                )
            else:
                st.warning(f"{selected_zone} 경로 지도 이미지가 없습니다.")
    with right2:
        with st.container(border=True):
            st.markdown("**화장실**")
            st.write("2번 출입구 옆")
        with st.container(border=True):
            st.markdown("**편의점**")
            st.write("1번 출입구 옆")

import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def get_gsheet():
    creds_dict = dict(st.secrets["google"])
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)

    spreadsheet_name = st.secrets["sheets"]["spreadsheet_name"]
    worksheet_name = st.secrets["sheets"]["worksheet_name"]

    sh = gc.open(spreadsheet_name)

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows=1000, cols=50)

    return ws

def append_row_gsheet(row: dict):
    ws = get_gsheet()

    values = ws.get_all_values()
    if len(values) == 0:
        headers = list(row.keys())
        ws.append_row(headers)
    else:
        headers = values[0]

    missing = [k for k in row.keys() if k not in headers]
    if missing:
        headers = headers + missing
        ws.delete_rows(1)
        ws.insert_row(headers, 1)

    row_values = [row.get(h, "") for h in headers]
    ws.append_row(row_values, value_input_option="USER_ENTERED")

if "pred_submitted" not in st.session_state:
    st.session_state.pred_submitted = False
    
if submitted and not st.session_state.pred_submitted:    
    append_row_gsheet(
        {
            "ts": now_kst_str(),
            "type": "prediction",
            "nickname": nickname.strip(),
            "phone4": phone4.strip(),
            "new_fan": is_new_fan,
            "승무패 예측": pred,
            "스코어 예측": auto_pred,
            "MOM" : pred_pick,
            "첫 득점자" : pred_goal,
            "match": f"{m['home']} vs {m['away']} ({m['date']})",
            }
        )
    st.session_state.pred_submitted = True
    
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")
    
if submitted_c and not st.session_state.pred_submitted:    
    append_row_gsheet(
        {
            "ts": now_kst_str(),
            "type": "cheer",
            "nickname": nickname.strip(),
            "phone4": phone4.strip(),
            "new_fan": is_new_fan,
            "응원 한마디": comment, 
            "match": f"{m['home']} vs {m['away']} ({m['date']})",
            }
        )
    st.session_state.pred_submitted = True
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")

if submitted_h and not st.session_state.pred_submitted:
    append_row_gsheet(
    {
        "ts": now_kst_str(),
        "type": "halftime",
        "nickname": nickname.strip(),
        "phone4": phone4.strip(),
        "new_fan": is_new_fan,
        "하프타임 퀴즈 답안": short_q.strip(),
        "match": f"{m['home']} vs {m['away']} ({m['date']})",
    }
    )
    st.session_state.pred_submitted = True
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")

if submitted_photo and not st.session_state.pred_submitted:
    append_row_gsheet(
    {
        "ts": now_kst_str(),
        "type": "photozone",
        "nickname": nickname.strip(),
        "phone4": phone4.strip(),
        "new_fan": is_new_fan,
        "사진": uploaded_photo,
        "match": f"{m['home']} vs {m['away']} ({m['date']})",
    }
    )
    st.session_state.pred_submitted = True
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")
    
if submitted_q1 and not st.session_state.pred_submitted:
    append_row_gsheet(
    {
        "ts": now_kst_str(),
        "type": "quiz1",
        "nickname": nickname.strip(),
        "phone4": phone4.strip(),
        "new_fan": is_new_fan,
        "퀴즈 답안1": comment1.strip(),
        "match": f"{m['home']} vs {m['away']} ({m['date']})",
    }
    )
    st.session_state.pred_submitted = True
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")
    
if submitted_q2 and not st.session_state.pred_submitted:
    append_row_gsheet(
    {
        "ts": now_kst_str(),
        "type": "quiz2",
        "nickname": nickname.strip(),
        "phone4": phone4.strip(),
        "new_fan": is_new_fan,
        "퀴즈 답안2": comment2,
        "match": f"{m['home']} vs {m['away']} ({m['date']})",
    }
    )
    st.session_state.pred_submitted = True
    st.success(
        "🔴⚫ **RED SEOUL!**\n\n"
        "성공적으로 제출되었습니다")