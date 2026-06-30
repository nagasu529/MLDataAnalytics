# Data Harmonization: TVSEP Shocks Analysis (Wave 2 - 2008 CLEANED)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source File:** `wave-2-shocksclean.dta` (Primary Cleaned File)
- **Status:** แก้ไขใหม่แทนเวอร์ชัน Raw เพื่อความถูกต้องของตัวแปรสถิติ
- **Observation Count:** 3,146 แถว (เหตุการณ์)
- **Reference Period:** พฤษภาคม 2007 - เมษายน 2008

## 2. การจัดการตัวแปรและโครงสร้าง
- **Naming Standard:** ใช้รหัส `_x31xxx` (มาตรฐานไฟล์ Clean ของปี 2008)
- **Financial Cleaning:** - ตัวแปร `_x31005a` (Total Loss)
    - ทำการจัดการค่า 'none' และ Missing codes (-9, -99)
- **Harmonization:** ปรับจูนรหัส Shock ID ให้เข้ากับกลุ่มมาตรฐาน (Agricultural, Demographic, Economics, Social)

## 3. กลยุทธ์การรับมือ (Coping Strategy)
- ปี 2008 เก็บข้อมูลการรับมือ 3 ลำดับ (`_x31008`, `_x31009`, `_x31010`)
- ดำเนินการแปลงจากระบบลำดับเป็น **Binary Indicators** เพื่อให้ข้อมูลมีมิติ "เท่ากับ" ปี 2022

## 🛠 Bug Fix Log (v1.1)
- **Issue:** เกิด `NameError: name 'shock_map_13' is not defined` เนื่องจากรหัสมีการอ้างอิงข้ามปี
- **Fix:** แก้ไขให้ตัวแปร Mapping ทั้งหมดเป็นชื่อเฉพาะของปี 2008 (`shock_map_08`)
- **Verification:** ตรวจสอบความสอดคล้องของชื่อคอลัมน์ `_x31002` และ `_x31005a` เรียบร้อยแล้ว

## 📊 Harmonization Strategy
- **Coping Strategies:** รวมรหัสย่อย 11-31 เข้าเป็น 6 กลุ่มใหญ่ที่เป็นมาตรฐานเดียวกับปี 2022 เพื่อเปรียบเทียบพฤติกรรมการกู้เงินและการใช้เงินออม
- **Loss Value:** จัดการค่า 'none' ให้เป็น 0.0 เพื่อความเสถียรในการทำ Descriptive Statistics