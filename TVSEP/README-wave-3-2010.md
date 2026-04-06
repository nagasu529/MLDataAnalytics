# Data Harmonization: TVSEP Shocks Analysis (Wave 3 - 2010)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source Files:** - `wave-3-shocksclean.dta` (Primary): ข้อมูลปี 2010 ที่ผ่านการทำความสะอาดแล้ว
    - `wave-3-shocksraw.dta`: ข้อมูลดิบสำหรับการ Recheck รายละเอียด
- **Observation Count:** 2,933 แถว (เหตุการณ์)
- **Reference Period:** ประมาณปี 2008 - 2010 (อ้างอิงตาม Questionnaire Version 3.2)

## 2. การจัดการตัวแปรและโครงสร้าง
- **Naming Standard:** ใช้รหัส `_x31xxx` เป็นหลักตามระบบไฟล์ Clean
- **Financial Conversion:** จัดการตัวแปร `_x31005a` (Total Loss) โดยแปลงค่า 'none' เป็น 0 และเปลี่ยน Data Type เป็น Float
- **Consistency:** ปรับค่ารหัส Shock ID ให้ตรงกับกลุ่มมาตรฐาน (Common Grouping) เพื่อใช้เปรียบเทียบกับ Wave 4-8

## 3. กลยุทธ์การรับมือ (Coping Strategy)
- ปี 2010 เก็บข้อมูล Coping 3 ลำดับ (`_x31008`, `_x31009`, `_x31010`)
- ทำการ Flatten ข้อมูลให้เป็น Binary Indicators (0/1) ในหมวดหมู่ Savings, Assets, Borrowing, และ Help เพื่อให้มิติข้อมูลเท่ากับปีอื่นๆ