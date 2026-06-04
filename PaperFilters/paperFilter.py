import mendeley
from mendeley.session import MendeleySession
import pandas as pd

# --- ส่วนที่ 1: ตั้งค่าการเชื่อมต่อ (ใส่ข้อมูลจาก Mendeley Developer ของคุณ) ---
CLIENT_ID = '224289'  # ใส่_CLIENT_ID_ของคุณที่นี่
CLIENT_SECRET = 'H8ZXQshv5bA4MGEF'  # ใส่_CLIENT_SECRET_ของคุณที่นี่

def search_mendeley_open_access(keyword, limit=10):
    try:
        # เริ่มการเชื่อมต่อแบบ Client Credentials (เหมาะสำหรับดึง Catalog สาธารณะ)
        client = mendeley.Mendeley(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        session = client.start_client_credentials_flow().authenticate()

        print(f"กำลังค้นหางานวิจัยหัวข้อ: {keyword}...")
        
        # ค้นหาใน Catalog โดยเน้นเฉพาะ Open Access
        # view='all' จะทำให้ได้ข้อมูลละเอียดรวมถึง Abstract
        search_results = session.catalog.search(
            query=keyword, 
            view='all', 
            limit=limit
        ).iter()

        research_data = []
        for doc in search_results:
            # ตรวจสอบว่าเป็น Open Access หรือไม่ (บางครั้ง API คืนค่ามาผสมกัน)
            # เราสามารถเช็คเงื่อนไขเพิ่มเติมได้ที่นี่
            data = {
                'Title': doc.title,
                'Year': doc.year,
                'Authors': [a.last_name for a in doc.authors] if doc.authors else "N/A",
                'Source': doc.source,
                'Abstract': doc.abstract if hasattr(doc, 'abstract') else "No Abstract",
                'Link': doc.link
            }
            research_data.append(data)

        return pd.DataFrame(research_data)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        return None

# --- ส่วนที่ 3: การใช้งาน ---
# ตัวอย่าง: ค้นหาเรื่องเกี่ยวกับ Low Carbon Community หรือ Climate Change
keyword_to_search = "Low carbon community in Thailand" 
df = search_mendeley_open_access(keyword_to_search, limit=5)

if df is not None and not df.empty:
    print("\n--- ผลการค้นหา ---")
    print(df[['Title', 'Year', 'Authors']])
    # บันทึกเป็นไฟล์ CSV เพื่อนำไปใช้ใน Excel หรือโปรแกรมสถิติ (Stata/SPSS)
    df.to_csv('mendeley_research_results.csv', index=False, encoding='utf-8-sig')
    print("\nบันทึกข้อมูลลงไฟล์ 'mendeley_research_results.csv' เรียบร้อยแล้ว")
else:
    print("ไม่พบข้อมูลที่ตรงกับเงื่อนไข")