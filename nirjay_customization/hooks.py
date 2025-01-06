app_name = "nirjay_customization"
app_title = "Nirjay Customization"
app_publisher = "Hybrowlabs Technologies"
app_description = "Purchase Order and Item Master customization."
app_email = "umar@hybrowlabs.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nirjay_customization/css/nirjay_customization.css"
# app_include_js = "/assets/nirjay_customization/js/nirjay_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/nirjay_customization/css/nirjay_customization.css"
# web_include_js = "/assets/nirjay_customization/js/nirjay_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nirjay_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Purchase Order" : "public/purchase_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "nirjay_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "nirjay_customization.utils.jinja_methods",
# 	"filters": "nirjay_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "nirjay_customization.install.before_install"
# after_install = "nirjay_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nirjay_customization.uninstall.before_uninstall"
# after_uninstall = "nirjay_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "nirjay_customization.utils.before_app_install"
# after_app_install = "nirjay_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "nirjay_customization.utils.before_app_uninstall"
# after_app_uninstall = "nirjay_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nirjay_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Purchase Order": {
# 		"before_save": "nirjay_customization.override.purchase_order.before_save",
#         "validate": "nirjay_customization.override.purchase_order.validate",
# 	}
# }

doc_events = {
    "Purchase Order": {
        "before_save": "nirjay_customization.override.purchase_order.before_save",
        "validate": "nirjay_customization.override.purchase_order.validate",
    },
    "Delivery Note": {
        "on_submit": "nirjay_customization.override.delivery_note.create_stock_entry",
    },
}




# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"nirjay_customization.tasks.all"
# 	],
# 	"daily": [
# 		"nirjay_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"nirjay_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nirjay_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"nirjay_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "nirjay_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "nirjay_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nirjay_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["nirjay_customization.utils.before_request"]
# after_request = ["nirjay_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["nirjay_customization.utils.before_job"]
# after_job = ["nirjay_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nirjay_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Custom Field", "filters": [
        [
            "name", "in", [
                "Item-custom_pack",
                "Purchase Order Item-custom_qty_in_pcs",
                "Purchase Order Item-custom_rate_per_pcs",
                "Purchase Order-custom_freight__insurance_",
                "Item-custom_basic_duty_rate_",
                "Purchase Order Item-custom_basic_duty_rate",
                "Purchase Order Item-custom_pack",
                "Purchase Order Item-custom_igst_assessable_value",
                "Purchase Order-custom_total_igst_assessable_value",
                "Purchase Invoice-custom_expense_against_purchase_order",
                "Purchase Invoice-custom_is_expense",
            ]
        ]
    ]}]



override_doctype_dashboards = {
    "Multi Purchase Order": "nirjay_customization.override.multi_purchase_order_dashboard.get_dashboard_data",
}

