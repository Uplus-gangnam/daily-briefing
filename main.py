import os
import smtplib
import urllib.request
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 1. 자산 데이터베이스 수집 (구글 스프레드시트 CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FDjG-ASlGbZcflRiCE6CBXeoHyzcy6R0l2uaXEv0Es8/gviz/tq?tqx=out:csv"
response = urllib.request.urlopen(SHEET_URL)
lines = [line.decode('utf-8') for line in response.readlines()]
reader = csv.reader(lines)

portfolio_data = ""
total_asset = 0

# 구글 시트를 한 줄씩 읽으며 HTML 표 데이터로 변환하는 핵심 로직
for i, row in enumerate(reader):
    if i == 0 or len(row) < 2: continue # 헤더 제외
    ticker = row[0].strip()
    amount = row[1].strip()
    
    # 임시 가격 매칭 알고리즘 (추후 금융 API와 유기적 결합)
    price = 150000 if ticker == "SK하이닉스" else 15
    dummy_change = "▲ 2.5%" if i % 2 == 0 else "▼ 1.1%"
    eval_value = int(amount) * price
    total_asset += eval_value
    
    portfolio_data += f"""
    <tr>
        <td><strong>{ticker}</strong></td>
        <td>{amount}</td>
        <td>{price:,}원</td>
        <td>{eval_value:,}원</td>
        <td><span style="color:{'#dc2626' if '▲' in dummy_change else '#2563eb'}; font-weight:bold;">{dummy_change}</span></td>
    </tr>
    """

# 2. 고품격 아웃룩 최적화 이메일 본문 조립 (HTML 편지지가 여기에 탑재됩니다)
html_body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0; padding:0; font-family:Arial, sans-serif; background-color:#f4f6f9;">
    <table width="100%" background="#f4f6f9" style="padding:20px 0;">
        <tr>
            <td align="center">
                <table width="600" bgcolor="#ffffff" style="border-radius:8px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                    <tr>
                        <td bgcolor="#0f172a" style="padding:25px; text-align:center; color:#ffffff;">
                            <h1 style="margin:0; font-size:20px;">일일 자산 분석 및 경제 마켓 브리핑</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:25px;">
                            <div style="font-size:15px; font-weight:bold; color:#0f172a; border-left:4px solid #3b82f6; padding-left:10px; margin-bottom:15px;">💰 나의 자산 현황 추이</div>
                            <div style="background-color:#f8fafc; border:1px solid #e2e8f0; padding:15px; border-radius:6px; margin-bottom:20px;">
                                <span style="color:#64748b; font-size:13px;">현재 총 자산 평가액</span><br>
                                <span style="font-size:22px; font-weight:bold; color:#1e293b;">{total_asset:,} 원</span>
                            </div>
                            <div style="font-size:15px; font-weight:bold; color:#0f172a; border-left:4px solid #3b82f6; padding-left:10px; margin-bottom:15px;">📊 보유 종목 상태 분석</div>
                            <table width="100%" style="border-collapse:collapse; font-size:13px;">
                                <tr bgcolor="#f8fafc" style="color:#64748b;"><th style="padding:10px; text-align:left;">종목명</th><th style="padding:10px; text-align:left;">보유량</th><th style="padding:10px; text-align:left;">현재가</th><th style="padding:10px; text-align:left;">평가금액</th><th style="padding:10px; text-align:left;">전일대비</th></tr>
                                {portfolio_data}
                            </table>
                            <div style="font-size:15px; font-weight:bold; color:#0f172a; border-left:4px solid #3b82f6; padding-left:10px; margin:25px 0 15px 0;">📰 주요 경제 이슈 및 키워드 사전</div>
                            <div style="background-color:#f8fafc; border:1px solid #e2e8f0; padding:15px; border-radius:6px;">
                                <div style="font-size:14px; font-weight:bold; color:#1e293b;">1. 미-이란 긴장 고조, 중동발 공급망 불안에 유가 급등 우려</div>
                                <div style="font-size:13px; color:#475569; margin:6px 0 10px 0;">미국과 이란 간의 군사적 대립이 격화되면서 원유 주요 수송로인 호르무즈 해협의 봉쇄 가능성이 제기되었습니다. 이로 인해 국제 유가가 장중 5% 이상 급등하며 글로벌 인플레이션 압력을 다시 자극하고 있습니다.</div>
                                <div style="background-color:#f0fdf4; border-left:3px solid #22c55e; padding:10px; font-size:12px; color:#166534;">
                                    <strong>💡 키워드 사전: 호르무즈 해협</strong><br>페르시아만과 오만만을 잇는 좁은 해협으로, 전 세계 해상 원유 수송량의 약 20%가 통과하는 핵심 요충지입니다.
                                </div>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# 3. 네이버 SMTP 서버를 이용해 수신자 메일로 자동 발송 처리
msg = MIMEMultipart('alternative')
msg['Subject'] = "[일일 브리핑] 100% 완전 자동화 자산 분석 보고서"
msg['From'] = "wowkang11@naver.com"
msg['To'] = "wowkang11@naver.com"
msg.attach(MIMEText(html_body, 'html'))

server = smtplib.SMTP_SSL('smtp.naver.com', 465)
server.login("wowkang11", os.environ["NAVER_PASSWORD"])
server.sendmail("wowkang11@naver.com", "wowkang11@naver.com", msg.as_string())
server.quit()
print("메일 발송 완료!")
