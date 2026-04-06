# Data Harmonization: TVSEP Shocks Analysis (Wave 1 - 2007 Baseline)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source File:** `wave-1-shocksclean.dta` (Baseline Year)
- **Observation Count:** 2,916 แถว (เหตุการณ์)
- **Reference Period:** พฤษภาคม 2549 - เมษายน 2550
- **สถานะ:** ข้อมูลปีฐานที่เป็นจุดเริ่มต้นของชุดข้อมูล Panel ทั้งหมด

## 2. การจัดการตัวแปร (Variable Mapping)
- **Shock Type:** ใช้รหัส `_x31002` (เทียบเท่า `shocks__id` ในปี 2022)
- **Financial Mapping:** - `_x31005`: มูลค่าความเสียหายรวม (Total Value of Loss)
    - มีการจัดการค่า 'none' และรหัส Stata Missing (-9, -99) ให้เป็นมาตรฐานเดียวกับ Wave อื่นๆ
- **Coping Strategy:** เจาะลึกตัวแปร `_x31008` ถึง `_x31010` เพื่อทำ Binary Indicators

## 3. การเพิ่มประสิทธิภาพ (Optimization)
- กำหนด dtypes เป็น `category` สำหรับตัวแปรเชิงคุณภาพเพื่อลดการใช้ Memory
- ใช้ Vectorized operations ในการ Map กลุ่ม Shock เพื่อความรวดเร็ว