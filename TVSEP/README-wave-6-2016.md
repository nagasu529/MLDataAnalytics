# TVSEP Shock Data Harmonization Project

## 📌 Project Strategy
โปรเจกต์นี้ใช้วิธีแยกการประมวลผลข้อมูล (Preprocessing) รายปี (Wave-by-Wave) เพื่อความสะดวกในการตรวจสอบ (Tracking) และควบคุมคุณภาพข้อมูลก่อนที่จะนำมารวมกันเป็น Panel Data ในขั้นตอนสุดท้าย

## 📂 Data Inventory (Wave 6 - 2017)
- **Primary File:** `shocksclean.dta` (แนะนำ) เนื่องจากผ่านการจัดการ Outliers และ Re-coding จากทีมวิจัยแล้ว
- **Reference File:** `shocksraw.dta` ใช้สำหรับอ้างอิงคำอธิบายเชิงคุณภาพ (Text Descriptions)
- **Key Identifiers:** `hhid` (Household ID) และ `uniqeshckId` (Event ID)

## 🛠 Transformation Logic (ทำให้มิติเท่ากัน)
เพื่อให้ข้อมูลปี 2017 เทียบเคียงกับปี 2022 ได้ เราได้ดำเนินการดังนี้:
1. **Financial Cast:** แปลงค่า 'none' เป็น 0 และจัดการค่าว่าง Stata (-9, -99) ให้เป็น NaN
2. **Standardized Grouping:** จัดกลุ่ม Shock จากรหัส `_x31002` เข้าสู่ 4 กลุ่มหลัก: `agricultural`, `demographic`, `economics`, และ `social`
3. **Coping Strategy Reconstruction:** เจาะลึกตัวแปร `_x31008` (Coping 1), `_x31009` (Coping 2), และ `_x31010` (Coping 3) เพื่อแปลงจากระบบลำดับ (Sequences) ให้เป็นระบบตัวบ่งชี้ (Binary Indicators: Yes/No) เหมือนปี 2022

## ⚠️ Notes for Future Waves
- ตรวจสอบรหัส Shock ID ทุกครั้งผ่าน Questionnaire PDF เนื่องจากบางปีอาจมีการเพิ่มรหัสใหม่
- การ Merge ระหว่างปี 2017 และ 2022 ต้องใช้ Master ID ที่เป็นระบบเดียวกัน