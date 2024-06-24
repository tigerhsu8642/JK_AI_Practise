# -*- coding: UTF-8 -*-
import time
import itertools
from dotenv import load_dotenv
from typing import Iterator, Optional
from data_types import TextMsg, ImageMsg, TextMsgList, MsgList, filter_text_msg
load_dotenv()

from api import get_characterglm_response
import streamlit as st

# 初始化
if "history_a" not in st.session_state:
    st.session_state["history_a"] = []

if "history_b" not in st.session_state:
    st.session_state["history_b"] = []

with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

def output_stream_response(response_stream: Iterator[str], placeholder):
    content = ""
    for content in itertools.accumulate(response_stream):
        placeholder.markdown(content)
    return content

def characterglm_example():
    character_metaA = {
        "user_info": "",
        "bot_info": "刘备，字玄德，蜀汉开国皇帝，三国时期著名的政治家、军事家。他出身贫寒，却志向远大，以复兴汉室为己任。在三国群雄逐鹿的乱世中，刘备以仁德著称，被誉为“仁德之君”。他性格谦和，礼贤下士，广结善缘，深受部下和百姓的爱戴。",
        "user_name": "用户",
        "bot_name": "刘备"
    }

    character_metaB = {
        "user_info": "",
        "bot_info": "诸葛亮，字孔明，号卧龙，徐州琅琊阳都人，三国时期蜀汉丞相，杰出的政治家、军事家、外交家。一个智慧超群、忠诚坚定、深谋远虑、清高淡泊、勤勉谨慎的卧龙先生，他的形象成为了后世敬仰的楷模。",
        "user_name": "用户",
        "bot_name": "诸葛亮"
    }

    st.session_state["history_a"].append(TextMsg({"role": "assistant", "content": "孔明先生，备闻先生之大才，如饥似渴。三次登山拜访，今日终于得以相见，实乃备之幸事。"}))
    st.session_state["history_a"].append(TextMsg({"role": "user", "content": "刘皇叔过誉了，亮不过是一介村夫，何劳皇叔如此屈尊。亮闻皇叔三次登山，不畏艰辛，可见皇叔之诚心，亮在此谢过。"}))

    st.session_state["history_b"].append(TextMsg({"role": "user", "content": "孔明先生，备闻先生之大才，如饥似渴。三次登山拜访，今日终于得以相见，实乃备之幸事。"}))
    st.session_state["history_b"].append(TextMsg({"role": "assistant", "content": "刘皇叔过誉了，亮不过是一介村夫，何劳皇叔如此屈尊。亮闻皇叔三次登山，不畏艰辛，可见皇叔之诚心，亮在此谢过。"}))

    for i in range(5):
        response_stream = get_characterglm_response(filter_text_msg(st.session_state["history_a"]), character_metaA)
        bot_response = output_stream_response(response_stream, message_placeholder)
        if not bot_response:
            print("生成出错")
            st.session_state["history_a"].pop()
        else:
            st.session_state["history_a"].append(TextMsg({"role": "assistant", "content": bot_response}))
            st.session_state["history_b"].append(TextMsg({"role": "user", "content": bot_response}))

        response_stream = get_characterglm_response(filter_text_msg(st.session_state["history_b"]), character_metaB)
        bot_response = output_stream_response(response_stream, message_placeholder)
        if not bot_response:
            print("生成出错")
            st.session_state["history_b"].pop()
        else:
            st.session_state["history_a"].append(TextMsg({"role": "user", "content": bot_response}))
            st.session_state["history_b"].append(TextMsg({"role": "assistant", "content": bot_response}))


    # 展示对话历史
    for msg in st.session_state["history_a"]:
        if msg["role"] == "assistant":
            with st.chat_message(name="user", avatar="user"):
                print("刘备：" + msg["content"])
        elif msg["role"] == "user":
            with st.chat_message(name="assistant", avatar="assistant"):
                print("孔明：" + msg["content"])
        else:
            raise Exception("Invalid role")


if __name__ == "__main__":
    characterglm_example()
