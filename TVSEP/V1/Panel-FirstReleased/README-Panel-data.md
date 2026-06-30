# Longitudinal Master Panel Dataset: TVSEP Shocks Analysis (2007 - 2024)

## 1. วัตถุประสงค์ (Project Objective)
เอกสารนี้อธิบายการรวมร่างข้อมูลภัยพิบัติและความเปราะบางของครัวเรือน (Household Shocks & Vulnerability) ในลักษณะข้อมูลแผงระยะยาว (Longitudinal/Panel Data) ครอบคลุมระยะเวลาตั้งแต่ปี 2007 ถึงปี 2024 (รวมทั้งสิ้น 10 Wave) เพื่อส่งต่อชุดข้อมูลที่สะอาด ทรงประสิทธิภาพ และ "Lean" ให้ทีม Data Science นำไปทำ Econometric / Regression Modeling ต่อไป

## 2. แหล่งที่มาของข้อมูล (Data Harmonization Scheme)
แผงข้อมูลนี้ประกอบขึ้นจากการดึงตัวแปรสำคัญ (Core Variables) ของแต่ละปีที่ผ่านการคลีนและปรับชื่อคอลัมน์ให้สอดคล้องกันข้ามยุคสมัย (Harmonization) ดังนี้:

- **ยุคตัวแปรดั้งเดิม (Wave 1 - 7 | ปี 2007 - 2017):** ใช้รหัสตัวแปรขึ้นต้นด้วย `_x31...`
- **ยุคตัวแปรสมัยใหม่ (Wave 8 - 10 | ปี 2019 - 2024):** ใช้รหัสตัวแปรขึ้นต้นด้วย `v311...` จากระบบ Survey Solutions

## 3. พิกัดตัวแปรใน Master Panel (Data Dictionary)
ไฟล์ผลลัพธ์สุดท้ายชื่อ `master_panel_shocks_2007_2024.csv` จะถูกจำกัดไว้เฉพาะ **14 ตัวแปรหลัก** เพื่อป้องกันปัญหาไฟล์บวมน้ำ (Data Bloating):

| ชื่อคอลัมน์มาตรฐาน | ประเภทข้อมูล | คำอธิบายความหมาย (Description) |
| :--- | :--- | :--- |
| `interview__key` | String / Object | รหัสประจำตัวแบบสอบถามระบุชุดข้อมูล |
| `hhid` | String / Numeric| รหัสระบุตัวตนครัวเรือน (Household ID) สำหรับทำ Panel Tracking |
| `survey_year` | Integer | ปีคริสต์ศักราชที่ทำการจัดเก็บข้อมูล (2007 - 2024) |
| `shocks_Group` | Categorical | กลุ่มของภัยพิบัติ (`agricultural`, `economics`, `demographic`, `social`, `others`) |
| `impact_3way` | Float / Numeric | มูลค่าความเสียหายรวม (รายได้หาย + จ่ายเพิ่ม + ทรัพย์สินพัง) หน่วยเป็นบาท |
| `impact_2way` | Float / Numeric | มูลค่าความเสียหายหลัก (รายได้หาย + ทรัพย์สินพัง) หน่วยเป็นบาท |
| `recovery_std` | Categorical | ระยะเวลาฟื้นตัวมาตรฐาน (`less than 1 year`, `1 year`, `more than 1 year`, `not yet recovered`) |
| `cons_label` | Categorical | พฤติกรรมการรัดเข็มขัดลดค่าบริโภค (`Yes (Reduced)`, `No (Did not reduce)`) |
| `coping_savings` | Binary (0/1) | ดึงเงินออมมาใช้รับมือหรือไม่ |
| `coping_insurance` | Binary (0/1) | ใช้เงินชดเชยจากประกันภัยหรือไม่ |
| `coping_informal_borrow` | Binary (0/1) | กู้ยืมเงินนอกระบบ/ญาติพี่น้อง/เพื่อนบ้านหรือไม่ |
| `coping_formal_borrow` | Binary (0/1) | กู้ยืมเงินในระบบ (ธนาคารพาณิชย์/ธกส./ออมสิน/กองทุนหมู่บ้าน) หรือไม่ |
| `coping_assets` | Binary (0/1) | ตัดใจขายสินทรัพย์หรือปศุสัตว์หรือไม่ |
| `coping_gov_help` | Binary (0/1) | ได้รับการช่วยเหลือ/เยียวยาจากภาครัฐหรือ NGO หรือไม่ |

## 4. ข้อควรระวังในการนำไปวิเคราะห์ต่อ (Analytical Caveats)
1. **Missing Variables in Early Waves:** ปี 2007 (Wave 1) ข้อมูลมูลค่าเงินจะมาจาก `_x31005n + _x31006n` ซึ่งรูปแบบการสอบถามอาจมีความแตกต่างเหลื่อมล้ำกับสูตร 3-way สองมิติของปีอื่นเล็กน้อย ทีมวิเคราะห์ควรระวังเรื่องค่าเฉลี่ย
2. **Standardized Categories:** ตัวแปรระยะเวลาการฟื้นตัว (`recovery_std`) ถูกปรับแต่งผ่านตรรกะโค้ดให้สอดคล้องกันหมดแล้วข้ามปี ทำให้สามารถนำไปทำแบบจำลองจำพวก Probit / Logit เพื่อหาปัจจัยที่ส่งผลต่อ "อัตราการยังไม่ฟื้นตัว (Probability of not yet recovered)" ได้ทันที
3. **Data Weighting:** หากต้องการขยายผลสถิติในระดับประเทศ (Representative Inferences) ทีมวิเคราะห์ต้องทำการนำรหัส `interview__key` หรือ `hhid` ไปผสาน (Merge) เข้ากับไฟล์ Master Household (V1) ของปีนั้นๆ เพื่อดึงค่าน้ำหนักสถิติ (Survey Weights) มาคำนวณร่วมด้วย