# Data Harmonization: TVSEP Shocks Analysis (Wave 5 - 2013)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source Files:** - `wave-5-2013-shocksclean.dta` (Primary): ผ่านการตรวจสอบคุณภาพแล้ว
    - `wave-5-2013-shocksraw.dta`: ข้อมูลดิบสำหรับอ้างอิง Text
- **Observation Count:** 2,114 แถว (เหตุการณ์)
- **Reference Period:** เมษายน 2012 - มีนาคม 2013

## 2. การจัดการตัวแปรและโครงสร้าง
- **Prefix:** ใช้ `_x31xxx` สำหรับไฟล์ Clean
- **Financial Conversion:** จัดการตัวแปร `_x31005a` (Total Loss) โดยแปลง 'none' เป็น 0 และจัดการค่าว่าง Stata (-9, -99)
- **Harmonization:** ปรับชื่อกลุ่มให้เป็นมาตรฐานเดียวกับปี 2017 และ 2022 เพื่อให้สามารถทำ Long-term Panel Analysis ได้

## 3. กลยุทธ์การรับมือ (Coping Strategy)
- ปี 2013 เก็บข้อมูล Coping 3 ลำดับ (`_x31008`, `_x31009`, `_x31010`) 
- ดำเนินการแปลงเป็น Binary Indicators (0/1) เพื่อให้มิติข้อมูลเท่ากับ Wave ล่าสุด