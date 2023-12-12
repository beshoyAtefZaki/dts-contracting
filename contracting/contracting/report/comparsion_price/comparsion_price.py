# Copyright (c) 2023, Dynamic Technology and contributors
# For license information, please see license.txt

# Copyright (c) 2023, Dynamic Technology and contributors
# For license information, please see license.txt

import frappe
import itertools 
from frappe import _

def execute(filters=None):
	columns = get_columns(filters) or []
	conditions = get_conditions(filters) or []
	data = get_data(conditions) or []
	return columns, data


def get_conditions(filters):
	cond = "1=1 " 
	if len(filters):
		if filters.get('from_date'):
			cond += " AND `tabComparison`.creation >= date('%s') "%(filters.get('from_date'))
		if filters.get('to_date'):
			cond += " AND `tabComparison`.creation <= '%s' "%(filters.get('to_date'))
	return cond
		

def get_columns(filters):
	columns = [
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 160,
		},
		{
			"label": _("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": 160,
		},
		{
			"label": _("Tender"),
			"fieldname": "tender",
			"fieldtype": "Link",
			"options": "Tender",
			"width": 160,
		},
		{
			"label": _("Comparison"),
			"fieldname": "comparison",
			"fieldtype": "Link",
			"options": "Comparison",
			"width": 160,
		},
		{
			"label": _("Sales Order"),
			"fieldname": "so",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 160,
		},
		{
			"label": _("Clearance"),
			"fieldname": "clearance",
			"fieldtype": "Link",
			"options": "Clearance",
			"width": 160,
		},
		
		
	]
	return columns

def get_data(conditions):
	sql = f"""
		SELECT `tabComparison`.project
		,`tabComparison`.customer
		,`tabComparison`.tender
		,`tabComparison`.name as comparison
		FROM `tabComparison`
		LEFT JOIN `tabSales Order` 
		ON 
	"""
	frappe.errprint(sql)
	data = frappe.db.sql(sql,as_dict=1)
	return data or []



