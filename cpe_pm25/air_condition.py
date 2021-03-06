def get_air_condition(pm25):
    lower_bound = [0, 25, 37, 50, 90]
    shortcode = [
        "good",
        "normal",
        "medium",
        "affecting",
        "polluted"
    ]
    brief_description = [
        "ดี",
        "ปกติ",
        "ปานกลาง",
        "เริ่มมีผลกระทบต่อสุขภาพ",
        "มีผลกระทบต่อสุขภาพ"
    ]
    description = [
        "คุณภาพอากาศดีมาก เหมาะสำหรับกิจกรรมกลางแจ้งและการท่องเที่ยว",
        "คุณภาพอากาศดี สามารถทำกิจกรรมกลางแจ้งและการท่องเที่ยวได้ตามปกติ",
        "ผู้ที่ต้องดูแลสุขภาพ หากมีอาการเบื้องต้น ควรลดระยะเวลาการทำกิจกรรมกลางแจ้ง",
        "ควรเฝ้าระวังสุขภาพ หากมีอาการเบื้องต้นควรงดกิจกรรมกลางแจ้ง ใช้อุปกรณ์ป้องกันหากจำเป็น",
        "ทุกคนควรหลีกเลี่ยงกิจกรรมกลางแจ้ง หลีกเลี่ยงพื้นที่ที่มีมลพิษทางอากาศสูง และใช้อุปกรณ์ป้องกันตนเองหากมีความจำเป็น"
    ]
    condition = [pm25 > i for i in lower_bound]
    i = condition.count(True) - 1
    return {
        "shortcode": shortcode[i],
        "brief_description": brief_description[i],
        "description": description[i]
    }
