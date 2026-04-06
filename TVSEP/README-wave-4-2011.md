# Data Harmonization: TVSEP Shocks Analysis (Wave 4 - 2011)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source Files:** - `shocksclean.dta` (Primary): ข้อมูลปี 2011 ที่ผ่านการตรวจสอบแล้ว
    - `shocksraw.dta`: ข้อมูลดิบสำหรับอ้างอิง
- **Observation Count:** 1,223 แถว (เหตุการณ์) *หมายเหตุ: จำนวนครัวเรือนน้อยกว่าปีอื่นตามแผนการเก็บข้อมูล*
- **Reference Period:** พฤษภาคม 2010 - เมษายน 2011

## 2. การจัดการตัวแปรและโครงสร้าง
- **Naming Convention:** ใช้รหัส `_x31xxx` เป็นหลัก
- **Financial Cleaning:** จัดการตัวแปร `_x31005a` (Total Loss) โดยแปลง 'none' เป็น 0 และจัดการรหัสค่าว่าง Stata
- **Panel Ready:** เพิ่มคอลัมน์ `survey_year` เพื่อระบุระลอกของข้อมูล (Wave Identifier)

## 3. กลยุทธ์การรับมือ (Coping Strategy)
- ปี 2011 เก็บข้อมูล Coping 3 ลำดับ (`_x31008`, `_x31009`, `_x31010`) 
- ดำเนินการแปลงเป็น Binary Indicators (0/1) เพื่อให้สามารถเปรียบเทียบพฤติกรรมการรับมือข้ามทศวรรษได้