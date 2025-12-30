import streamlit as st
import pandas as pd
import re
import io

# ---------------------------------------------------------
# 1. 설정 및 헬퍼 함수
# ---------------------------------------------------------

VALID_TIER_STRING = """
1 1.5 1.8 2 2.5 2.8 3 3.5 3.8 4 4.5 4.8 5 5.5 5.8 6 6.5 6.8 7 7.5 7.8 8 8.5 8.8 9 9.5 9.8 9.9 10 10.8 11 11.8 12 12.8 13 13.8 14 14.8 15 15.8 16 16.8 17 17.8 18 18.8 19 19.8 19.9 20 20.8 21 21.8 22 22.8 23 23.8 24 24.8 25 25.8 26 26.8 27 27.8 28 28.8 29 29.8 29.9 30 30.8 31 31.8 32 32.8 33 33.8 34 34.8 35 35.8 36 36.8 37 37.8 38 38.8 39 39.8 39.9 40 40.8 41 41.8 42 42.8 43 43.8 44 44.8 45 45.8 46 46.8 47 47.8 48 48.8 49 49.8 49.9 50 50.8 51 51.8 52 52.8 53 53.8 54 54.8 55 55.8 56 56.8 57 57.8 58 58.8 59 59.8 59.9 60 60.8 61 61.8 62 62.8 63 63.8 64 64.8 65 65.8 66 66.8 67 67.8 68 68.8 69 69.8 69.9 70 70.8 71 71.8 72 72.8 73 73.8 74 74.8 75 75.8 76 76.8 77 77.8 78 78.8 79 79.8 79.9 80 80.8 81 81.8 82 82.8 83 83.8 84 84.8 85 85.8 86 86.8 87 87.8 88 88.8 89 89.8 89.9 90 90.8 91 91.8 92 92.8 93 93.8 94 94.8 95 95.8 96 96.8 97 97.8 98 98.8 99 99.8 99.9 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 203 208 209 210 213 218 219 220 222 223 228 229 230 233 238 239 240 243 248 249 250 253 258 259 260 263 268 269 270 273 278 279 280 283 288 289 290 293 298 299 300 303 308 309 310 313 318 319 320 323 328 329 330 333 338 339 340 343 348 349 350 353 358 359 360 363 368 369 370 373 378 379 380 383 388 389 390 393 398 399 400 403 408 409 410 413 418 419 420 423 428 429 430 433 438 439 440 443 448 449 450 453 458 459 460 463 468 469 470 473 478 479 480 483 488 489 490 493 498 499 500 508 509 518 519 520 528 529 538 539 548 549 555 558 559 568 569 578 579 588 589 598 599 608 609 618 619 628 629 638 639 648 649 658 659 666 668 669 678 679 688 689 698 699 708 709 718 719 728 729 738 739 748 749 758 759 768 769 777 778 779 788 789 798 799 808 809 818 819 828 829 838 839 848 849 858 859 868 869 878 879 888 889 898 899 908 909 918 919 928 929 938 939 948 949 958 959 968 969 978 979 988 989 998 999 1000 1048 1049 1088 1098 1099 1148 1149 1188 1198 1199 1248 1249 1288 1298 1299 1314 1348 1349 1388 1398 1399 1448 1449 1488 1498 1499 1548 1549 1588 1598 1599 1648 1649 1688 1698 1699 1748 1749 1788 1798 1799 1848 1849 1888 1898 1899 1948 1949 1988 1998 1999 2048 2049 2088 2098 2099 2148 2149 2188 2198 2199 2248 2249 2288 2298 2299 2348 2349 2388 2398 2399 2448 2449 2488 2498 2499 2548 2549 2588 2598 2599 2648 2649 2688 2698 2699 2748 2749 2788 2798 2799 2848 2849 2888 2898 2899 2948 2949 2988 2998 2999 3048 3049 3088 3098 3099 3148 3149 3188 3198 3199 3248 3249 3288 3298 3299 3348 3349 3388 3398 3399 3448 3449 3488 3498 3499 3548 3549 3588 3598 3599 3648 3649 3688 3698 3699 3748 3749 3788 3798 3799 3848 3849 3888 3898 3899 3948 3949 3988 3998 3999 4088 4098 4099 4188 4198 4199 4288 4298 4299 4388 4398 4399 4488 4498 4499 4588 4598 4599 4688 4698 4699 4788 4798 4799 4888 4898 4899 4988 4998 4999 5088 5098 5099 5188 5198 5199 5288 5298 5299 5388 5398 5399 5488 5498 5499 5588 5598 5599 5688 5698 5699 5788 5798 5799 5888 5898 5899 5988 5998 5999 6088 6098 6099 6188 6198 6199 6288 6298 6299 6388 6398 6399 6488 6498 6499 6588 6598 6599 6688 6698 6699 6788 6798 6799 6888 6898 6899 6988 6998 6999 7088 7098 7099 7188 7198 7199 7288 7298 7299 7388 7398 7399 7488 7498 7499
"""

VALID_TIERS = set()
try:
    for x in VALID_TIER_STRING.split():
        VALID_TIERS.add(float(x))
except:
    pass

def clean_price(price_str):
    if pd.isna(price_str): return 0.0
    # 정규식: 숫자와 소수점만 남김
    cleaned = re.sub(r'[^0-9.]', '', str(price_str))
    try: return float(cleaned)
    except: return 0.0

def parse_package_name(name):
    name = str(name).strip()
    match = re.search(r'^(.*?)[\s\-]*(\d+)차$', name)
    if match:
        base_name = match.group(1).strip()
        if base_name.endswith('-'): base_name = base_name[:-1].strip()
        cha = int(match.group(2))
        return base_name, cha
    else:
        # 차수 없으면 1차로 간주
        base_name = name
        if base_name.endswith('-'): base_name = base_name[:-1].strip()
        return base_name, 1

@st.cache_data
def load_and_preprocess(file):
    """
    파일을 읽고 헤더를 찾아 전처리하는 함수 (캐싱 적용)
    """
    try:
        # 1. 파일 전체를 헤더 없이 읽음
        if file.name.endswith('.csv'):
            raw_df = pd.read_csv(file, header=None)
        else:
            xls = pd.ExcelFile(file)
            sheet_name = 'PID' if 'PID' in xls.sheet_names else xls.sheet_names[0]
            raw_df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        
        # 2. 헤더 찾기 (PID, ver 키워드)
        header_idx = 0
        for i in range(min(30, len(raw_df))):
            row_vals = [str(x).strip() for x in raw_df.iloc[i].values]
            if 'PID' in row_vals and 'ver' in row_vals:
                header_idx = i
                break
        
        # 3. 데이터프레임 재구성
        df = raw_df.iloc[header_idx+1:].copy()
        df.columns = [str(x).strip() for x in raw_df.iloc[header_idx]]
        df.reset_index(drop=True, inplace=True)
        
        # 4. 필수 컬럼 확인
        required_cols = ['ver', 'PID', 'iOS', '상품명_商品名(KR)']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            return None, f"필수 컬럼 누락: {missing}"

        # 5. 전처리
        df['price_clean'] = df['iOS'].apply(clean_price)
        parsed = df['상품명_商品名(KR)'].apply(parse_package_name)
        df['base_name'] = [p[0] for p in parsed]
        df['cha'] = [p[1] for p in parsed]
        
        return df, None
        
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# 2. Main App
# ---------------------------------------------------------

def main():
    st.set_page_config(page_title="PID 자동 검수기", layout="wide")
    
    st.title("📋 PID 데이터 자동 검수기")
    st.markdown("엑셀/CSV 파일을 업로드하면 **가격(Tier), 명칭, 차수 누락, 가격 변동**을 자동으로 검사합니다.")

    uploaded_file = st.file_uploader("PID 파일 업로드 (.xlsx, .csv)", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        df, error_msg = load_and_preprocess(uploaded_file)
        
        if error_msg:
            st.error(error_msg)
        else:
            st.success("파일 로드 성공!")
            
            # 버전 선택
            unique_vers = [str(v) for v in df['ver'].dropna().unique()]
            unique_vers_sorted = sorted(unique_vers, reverse=True)
            
            target_ver = st.selectbox("검수 대상 버전 선택", unique_vers_sorted, index=0)
            
            if st.button("검수 시작", type="primary"):
                # 검수 로직 실행
                df['ver_str'] = df['ver'].astype(str)
                target_df = df[df['ver_str'] == target_ver].copy()
                history_df = df[df['ver_str'] != target_ver].copy()

                if target_df.empty:
                    st.warning("선택한 버전의 데이터가 없습니다.")
                else:
                    # 이번 버전 배치 매핑
                    current_batch_map = {}
                    for idx, row in target_df.iterrows():
                        bn = row['base_name']
                        if bn not in current_batch_map: current_batch_map[bn] = set()
                        current_batch_map[bn].add(row['cha'])

                    issues = []
                    
                    progress_bar = st.progress(0)
                    total_rows = len(target_df)
                    
                    for i, (idx, row) in enumerate(target_df.iterrows()):
                        # 진행률 표시
                        progress_bar.progress((i + 1) / total_rows)
                        
                        pid = row['PID']
                        name_kr = row['상품명_商品名(KR)']
                        price = row['price_clean']
                        base_name = row['base_name']
                        current_cha = row['cha']

                        # 1. Tier Check
                        if price > 0 and price not in VALID_TIERS:
                            issues.append({
                                "PID": pid, "패키지명": name_kr, 
                                "오류 유형": "가격 정책 오류(Tier)", 
                                "상세 내용": f"{price} (허용 리스트 없음)", 
                                "비고": "가격 확인 필요"
                            })

                        # 2. Naming Check
                        if '-' in str(name_kr):
                            issues.append({
                                "PID": pid, "패키지명": name_kr, 
                                "오류 유형": "명칭 포맷 경고", 
                                "상세 내용": "하이픈(-) 포함됨", 
                                "비고": "삭제 권장"
                            })

                        # 3. History Check
                        prev_items = history_df[history_df['base_name'] == base_name]
                        if not prev_items.empty:
                            # 차수 체크
                            max_prev_cha = prev_items['cha'].max()
                            if current_cha > max_prev_cha + 1:
                                missing_chas = set(range(max_prev_cha + 1, current_cha))
                                existing_chas_in_batch = current_batch_map.get(base_name, set())
                                real_missing = missing_chas - existing_chas_in_batch
                                
                                if real_missing:
                                    missing_str = ",".join(map(str, sorted(list(real_missing))))
                                    issues.append({
                                        "PID": pid, "패키지명": name_kr, 
                                        "오류 유형": "기수(차수) 건너뜀", 
                                        "상세 내용": f"현재 {current_cha}차 (과거 Max {max_prev_cha}차)", 
                                        "비고": f"누락된 차수: {missing_str}차"
                                    })
                            
                            # 가격 변동 체크
                            prev_prices = prev_items['price_clean'].unique()
                            if price not in prev_prices:
                                issues.append({
                                    "PID": pid, "패키지명": name_kr, 
                                    "오류 유형": "가격 변경됨", 
                                    "상세 내용": f"현재 {price} (과거: {prev_prices})", 
                                    "비고": "의도 여부 확인"
                                })
                    
                    progress_bar.empty()

                    # 결과 출력
                    if issues:
                        st.error(f"총 {len(issues)}건의 문제점이 발견되었습니다.")
                        res_df = pd.DataFrame(issues)
                        st.dataframe(res_df, use_container_width=True)
                        
                        # CSV 다운로드 버튼
                        csv = res_df.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="결과 CSV 다운로드",
                            data=csv,
                            file_name=f"PID_검수결과_{target_ver}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.balloons()
                        st.success("🎉 완벽합니다! 발견된 문제점이 없습니다.")

if __name__ == "__main__":
    main()
