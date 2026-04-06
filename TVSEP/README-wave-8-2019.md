# Data Harmonization: TVSEP Shocks Analysis (Wave 8 - Special/Interim)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Wave Type:** ระลอกพิเศษ (Interim Survey)
- **Data System:** Survey Solutions
- **Source Files:** - `shocks.dta` และ `shocks_detail.dta` (ตรวจสอบความสอดคล้องกับ Wave 7 และ 9)
- **Key Identifiers:** `interview__key` และ `shocks__id`

## 2. จุดเด่นและข้อควรระวัง (Special Considerations)
- **Sample Size:** จำนวนกลุ่มตัวอย่างอาจแตกต่างจาก Wave หลัก (1, 3, 4, 5, 6, 7, 9) เนื่องจากเป็นการเก็บข้อมูลเฉพาะกิจ
- **Harmonization:** ต้องตรวจสอบรหัส `shocks__id` ว่ามีการเพิ่มหมวดหมู่เฉพาะสำหรับ Wave นี้หรือไม่ (เช่น Shock ที่เกี่ยวกับมาตรการรัฐ)
- **Coping Strategy:** การจัดกลุ่ม Binary Indicators ยังคงยึดตามมาตรฐาน 6 กลุ่มหลัก (Savings, Insurance, Informal Borrowing, Formal Borrowing, Assets, Gov Help)

## 3. การใช้งานใน Panel Data
- ใช้สำหรับเติมเต็มข้อมูลในช่วงรอยต่อ (Transition Period) เพื่อดูความต่อเนื่องของกลยุทธ์การรับมือ (Coping Continuity)