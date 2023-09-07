import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas as pd  
import re
import random


def get_gsheet():
  scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  # Create a connection object.
  credentials = service_account.Credentials.from_service_account_info(
      st.secrets["gcp_service_account"],
      scopes=[
          "https://www.googleapis.com/auth/spreadsheets",'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'
      ],
  )
  client = gspread.authorize(credentials)

  # 작업자별 누적 작업량이 기록된 시트 이름
  sheet_name = 'jail_break'

  # 작업자별 누적 작업량 시트 불러오기
  sheet = client.open(sheet_name).worksheet('시트1')

  # 데이터 읽어오기
  data = sheet.get_all_records()

  #미배분 파일 가져오기 (파일명 - key)
  df = pd.DataFrame(data)

  return sheet, df

sheet, df = get_gsheet()


# jail break 예시
jb_prompt_ls = df['prompt'].to_list()

# prompt 입력
prompt = st.text_input('Instruction을 입력하세요', '')
if st.button('변환'):
    st.write(re.sub('<<replace>>',prompt,random.choice(jb_prompt_ls)))

# 변경하기 버튼


# (1)'작업 유형'을 기준으로 묶은 뒤, 전체 개수
# '작업자' 값이 ''인 개수, 작업 종료일?

# for work_type in ['글나누기', '바꿔쓰기', '줄여쓰기', '요약하기']:
#   st.write(f'**{work_type}**', '남은 작업량:', len(df.loc[(df['작업 유형'] == work_type) & (df['작업자'] == '')]))