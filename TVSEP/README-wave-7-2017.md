# Data Harmonization: TVSEP Shocks Analysis (Wave 7 - 2019)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Year:** 2019 (ระลอกก่อนเกิดสถานการณ์โควิด-19)
- **Data System:** Survey Solutions (Modern Era)
- **Source Files:** - `shocks.dta`: ข้อมูลระบุประเภทเหตุการณ์ (Level 1)
    - `shocks_detail.dta`: ข้อมูลความเสียหายและการรับมือ (Level 2)
- **Key Identifiers:** `interview__key` และ `shocks__id`

## 2. โครงสร้างและการจัดการ (Data Structure)
- **Nested Roster:** ข้อมูลถูกเก็บแบบ Roster ซ้อน Roster ต้องทำการ Merge ก่อนใช้งานเพื่อให้ได้ข้อมูลมูลค่าความเสียหาย
- **Variable Transition:** - ไม่ใช้รหัส `_x31xxx` แล้ว 
    - มูลค่าความเสียหายหลักใช้ `v31105a`
    - การรับมือใช้ `v31108a__1` ถึง `v31108a__7`
- **Cleaning:** จัดการค่า 'none' ในคอลัมน์เงินให้เป็น 0.0 ตามมาตรฐานโปรเจกต์

## 3. เป้าหมายการวิเคราะห์ (Analysis Goal)
- ใช้เป็นข้อมูลเปรียบเทียบ (Benchmark) สำหรับสถานะครัวเรือนก่อนเข้าสู่ช่วงวิกฤตเศรษฐกิจจากโควิด-19 (เทียบกับ Wave 9)