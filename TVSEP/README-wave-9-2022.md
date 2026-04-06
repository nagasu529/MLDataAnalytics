# Data Harmonization: TVSEP Shocks Analysis (Wave 9 - 2022)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Year:** 2022 (Post-COVID Wave)
- **Source Files (ต้องใช้คู่กัน):**
    - `shocks.dta`: ข้อมูลระดับประเภทเหตุการณ์ (Event types)
    - `shocks_detail.dta`: ข้อมูลรายละเอียดความเสียหายและการรับมือ (Loss & Coping)
- **Key Identifiers:** `interview__key` และ `shocks__id`

## 2. ขั้นตอนการจัดการข้อมูล (Workflow)
- **Merging Strategy:** ทำการ Inner Join ระหว่าง Roster 1 (shocks) และ Roster 2 (shocks_detail) เนื่องจากข้อมูลชุดนี้ถูกเก็บแบบ Nested Roster
- **Variable Mapping:** เปลี่ยนชื่อตัวแปรระบบ Survey Solutions ให้เป็นชื่อมาตรฐาน (Standardized Names) เพื่อความสะดวกในการทำ Panel ร่วมกับปี 2007-2017
- **Cleaning:** จัดการค่า 'none' และ 'not yet recovered' ในคอลัมน์ตัวเลขให้พร้อมสำหรับการคำนวณ

## 3. มิติของตัวแปร (Dimensions)
- **Loss Value:** ใช้ตัวแปร `v31105a` เป็นหลักในการวัดมูลค่าความเสียหาย
- **Coping Strategies:** ใช้กลุ่มตัวแปร `v31108a__1` ถึง `v31108a__7` ซึ่งถูกเก็บแบบ Binary มาแล้ว แต่อาจต้องจัดการค่า Missing เพื่อความแม่นยำ