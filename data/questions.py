MAIN_PROBLEMS = [
    {
        "id": "power_off",
        "label": "لا يعمل الحاسوب",
        "questions": ["q_power_led", "q_fans", "q_power_cable", "q_outlet"],
    },
    {
        "id": "blank_screen",
        "label": "يعمل الحاسوب لكن الشاشة فارغة",
        "questions": ["q_computer_running", "q_screen_blank", "q_post_screen", "q_external_monitor"],
    },
    {
        "id": "boot_problem",
        "label": "لا يُقلع الحاسوب بشكل صحيح",
        "questions": ["q_computer_running", "q_post_screen", "q_os_loading_screen", "q_bsod"],
    },
    {
        "id": "slow",
        "label": "الحاسوب بطيء",
        "questions": ["q_os_load_time", "q_program_launch", "q_disk_nearly_full", "q_disk_activity", "q_startup_programs"],
    },
    {
        "id": "overheating",
        "label": "يسخن الحاسوب أو ينطفئ فجأة",
        "questions": ["q_computer_running", "q_computer_hot", "q_shutdown", "q_fans", "q_vent_blocked", "q_fan_noise"],
    },
    {
        "id": "network",
        "label": "الإنترنت/الشبكة لا تعمل",
        "questions": ["q_wifi_connected", "q_networks_visible", "q_router_reachable", "q_internet", "q_other_devices", "q_ip_address"],
    },
    {
        "id": "storage",
        "label": "مشكلة في التخزين",
        "questions": ["q_disk_nearly_full", "q_disk_activity", "q_disk_errors", "q_files_corrupt"],
    },
    {
        "id": "memory",
        "label": "مشكلة في الذاكرة",
        "questions": ["q_ram_usage", "q_freezes", "q_app_crashes", "q_ram_detected"],
    },
    {
        "id": "peripheral",
        "label": "الملحق/الجهاز الطرفي لا يعمل",
        "questions": ["q_device_detected", "q_device_other_port", "q_device_other_computer", "q_driver"],
    },
]

QUESTIONS = {
    "q_power_led": {
        "text": "عند الضغط على زر الطاقة، هل يضيء مؤشر الطاقة؟",
        "yes_fact": "power_led_on",
        "no_fact": "power_led_off",
    },
    "q_fans": {
        "text": "عند تشغيل الحاسوب، هل تدور المروحات (أو تسمع صوت هدير الجهاز)؟",
        "yes_fact": "fans_running",
        "no_fact": "fans_not_running",
    },
    "q_power_cable": {
        "text": "هل كابل الطاقة موصول بإحكام بالحاسوب وبمقبس الحائط معاً؟",
        "yes_fact": "power_cable_ok",
        "no_fact": "power_cable_loose",
    },
    "q_outlet": {
        "text": "هل يزود مقبس الحائط الأجهزة الأخرى بالكهرباء بشكل صحيح؟",
        "yes_fact": "outlet_power_ok",
        "no_fact": "outlet_power_fails",
    },
    "q_computer_running": {
        "text": "هل يعمل الحاسوب ويستمر في العمل (الأضواء والمروحات نشطة)؟",
        "yes_fact": "computer_running",
        "no_fact": "computer_not_running",
    },
    "q_screen_blank": {
        "text": "هل الشاشة فارغة تماماً (لا توجد أي صورة)؟",
        "yes_fact": "screen_blank",
        "no_fact": "screen_has_image",
    },
    "q_post_screen": {
        "text": "عند بدء التشغيل، هل ترى شعار الشركة المصنعة أو شاشة BIOS لفترة وجيزة؟",
        "yes_fact": "post_screen_visible",
        "no_fact": "post_screen_blank",
    },
    "q_external_monitor": {
        "text": "إذا وصّلت شاشة خارجية، فهل تعرض صورة؟",
        "yes_fact": "external_monitor_works",
        "no_fact": "external_monitor_blank",
        "laptop_only": True,
    },
    "q_os_loading_screen": {
        "text": "بعد شاشة الشعار، هل تظهر شاشة تحميل نظام التشغيل (مثل شعار Windows)؟",
        "yes_fact": "os_loading_screen_visible",
        "no_fact": "os_loading_screen_absent",
    },
    "q_bsod": {
        "text": "هل يعرض الحاسوب شاشة خطأ زرقاء أو سوداء أثناء بدء التشغيل؟",
        "yes_fact": "bsod_occurs",
        "no_fact": "no_bsod",
    },
    "q_os_load_time": {
        "text": "هل يستغرق نظام التشغيل وقتاً طويلاً في بدء التشغيل؟",
        "yes_fact": "os_loads_slowly",
        "no_fact": "os_loads_normal",
    },
    "q_program_launch": {
        "text": "هل تستغرق البرامج وقتاً طويلاً لفتحها؟",
        "yes_fact": "programs_launch_slowly",
        "no_fact": "programs_launch_normal",
    },
    "q_disk_nearly_full": {
        "text": "هل القرص الصلب ممتلئ تقريباً؟",
        "yes_fact": "disk_nearly_full",
        "no_fact": "disk_has_space",
    },
    "q_startup_programs": {
        "text": "هل تبدأ العديد من البرامج تلقائياً عند تشغيل الحاسوب؟",
        "yes_fact": "many_startup_programs",
        "no_fact": "few_startup_programs",
    },
    "q_computer_hot": {
        "text": "هل يسخن الحاسوب بشكل غير طبيعي؟",
        "yes_fact": "computer_hot",
        "no_fact": "computer_cool",
    },
    "q_shutdown": {
        "text": "هل ينطفئ الحاسوب فجأة من تلقاء نفسه؟",
        "yes_fact": "shuts_down_unexpectedly",
        "no_fact": "shuts_down_normally",
    },
    "q_vent_blocked": {
        "text": "هل فتحات التهوية مسدودة أو مغطاة؟",
        "yes_fact": "vents_blocked",
        "no_fact": "vents_clear",
    },
    "q_fan_noise": {
        "text": "هل مروحة التبريد صاخبة بشكل غير طبيعي؟",
        "yes_fact": "fan_unusually_noisy",
        "no_fact": "fan_quiet_normal",
    },
    "q_wifi_connected": {
        "text": "هل الحاسوب متصل بشبكة Wi-Fi؟",
        "yes_fact": "wifi_connected",
        "no_fact": "wifi_disconnected",
    },
    "q_networks_visible": {
        "text": "هل يجد الحاسوب أي شبكات Wi-Fi متاحة؟",
        "yes_fact": "wifi_shows_networks",
        "no_fact": "wifi_no_networks",
    },
    "q_router_reachable": {
        "text": "هل يمكن للحاسوب الاتصال بجهاز التوجيه (الشبكة المحلية)؟",
        "yes_fact": "router_reachable",
        "no_fact": "router_unreachable",
    },
    "q_internet": {
        "text": "هل يمكنك فتح المواقع أو الوصول إلى الإنترنت؟",
        "yes_fact": "internet_reachable",
        "no_fact": "internet_unreachable",
    },
    "q_other_devices": {
        "text": "هل الأجهزة الأخرى على نفس الشبكة بلا وصول للإنترنت أيضاً؟",
        "yes_fact": "other_devices_offline",
        "no_fact": "other_devices_online",
    },
    "q_ip_address": {
        "text": "هل يحصل الحاسوب على عنوان IP صالح (لا يبدأ بـ 169.254)؟",
        "yes_fact": "ip_address_assigned",
        "no_fact": "ip_address_missing",
    },
    "q_disk_activity": {
        "text": "هل القرص مشغول باستمرار بنشاط مرتفع (100%) لفترات طويلة؟",
        "yes_fact": "disk_activity_high",
        "no_fact": "disk_activity_normal",
    },
    "q_disk_errors": {
        "text": "هل يبلغ النظام عن أخطاء في القرص؟",
        "yes_fact": "disk_errors_reported",
        "no_fact": "disk_errors_absent",
    },
    "q_files_corrupt": {
        "text": "هل هناك ملفات مفقودة أو تالفة؟",
        "yes_fact": "files_missing_corrupt",
        "no_fact": "files_intact",
    },
    "q_ram_usage": {
        "text": "هل استخدام الذاكرة قريب من 100% حتى مع فتح برامج قليلة؟",
        "yes_fact": "ram_usage_high",
        "no_fact": "ram_usage_normal",
    },
    "q_freezes": {
        "text": "هل يتجمد النظام أو يصبح بلا استجابة؟",
        "yes_fact": "system_freezes",
        "no_fact": "system_responsive",
    },
    "q_app_crashes": {
        "text": "هل تتعطل التطبيقات بشكل متكرر؟",
        "yes_fact": "frequent_app_crashes",
        "no_fact": "apps_stable",
    },
    "q_ram_detected": {
        "text": "هل يعرض النظام كل الذاكرة المثبتة؟",
        "yes_fact": "ram_sticks_detected",
        "no_fact": "ram_sticks_missing",
    },
    "q_device_detected": {
        "text": "هل يكتشف نظام التشغيل الجهاز؟",
        "yes_fact": "device_detected",
        "no_fact": "device_not_detected",
    },
    "q_device_other_port": {
        "text": "هل يعمل الجهاز عند توصيله بمنفذ مختلف؟",
        "yes_fact": "device_works_in_another_port",
        "no_fact": "device_fails_any_port",
    },
    "q_device_other_computer": {
        "text": "هل يعمل الجهاز عند توصيله بحاسوب آخر؟",
        "yes_fact": "device_works_on_other_computer",
        "no_fact": "device_fails_other_computer",
    },
    "q_driver": {
        "text": "هل يعرض النظام تحذيراً بشأن برنامج تشغيل الجهاز؟",
        "yes_fact": "driver_issue",
        "no_fact": "drivers_installed",
    },
}
