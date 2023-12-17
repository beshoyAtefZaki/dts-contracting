import frappe
from frappe.model.mapper import get_mapped_doc
from frappe import _
@frappe.whitelist()
def add_sales_order_script():
	add_properties()
	return
	try :
		name = "Purchase Order-Form"
		if frappe.db.exists("Client Script",name) :
			doc = frappe.get_doc("Client Script",name)
		else :

			doc = frappe.new_doc("Client Script")
		print("+ from add script")
		print("+ from add script")

		# doc = frappe.new_doc("Client Script")
		doc.dt      = "Purchase Order"
		doc.view    = "Form"
		doc.enabled = 1
		doc.script = """
		
			
		
					  
			frappe.ui.form.on("Purchase Order", {
			refresh(frm) {
				frm.set_query("comparison", function () {
				return {
					filters: {
					tender_status: ["in", ["Approved"]],
					},
				};
				});
				if (frm.doc.docstatus == 1 && frm.doc.is_contracting) {
				frm.add_custom_button(__("Clearence"), function () {
					frappe.model.open_mapped_doc({
					method: "contracting.contracting.doctype.purchase_order.purchase_order.make_clearence_doc",
					frm: frm, //this.frm
					});
				},__("Create"));
				}
			},
			});
	
		
	
		
	
		
	
		"""
		doc.save()
	except :
		pass



	try :
		name = "Sales Order-Form"
		if frappe.db.exists("Client Script",name) :
			doc = frappe.get_doc("Client Script",name)
		else :

			doc = frappe.new_doc("Client Script")
			print("+ from add script")
			doc.dt      = "Sales Order"
			doc.view    = "Form"
			doc.enabled = 1
			doc.script = """
						  
					frappe.ui.form.on('Sales Order', {
					refresh(frm) {
						frm.set_query("comparison", function(){
							return {
								filters : {
									"tender_status": ["in", ["Approved"]]
								}
							};
						});
						if(frm.doc.docstatus==1){
						frm.add_custom_button(__("create Clearence"), function() {
							frappe.model.open_mapped_doc({
						method: "contracting.contracting.add_client_Sccript.make_clearence",
						frm:frm //this.frm
						})
						})
						}
					}
				})
		
			"""
			doc.save()
	except :
		pass





	try:
		name = "Stock Entry-Form"
		if frappe.db.exists("Client Script",name) :
			doc = frappe.get_doc("Client Script",name)
		else :

			doc = frappe.new_doc("Client Script")
		

		print("+ from add script")
		# doc = frappe.new_doc("Client Script")
		doc.dt = "Stock Entry"
		doc.view = "Form"
		doc.enabled = 1
		doc.script = """
			frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
		// your code here
		
		frm.events.set_child_table_fields(frm)
	    frm.events.comparison(frm)
		
	} ,
	set_child_table_fields(frm) {
	    frm.doc.items.forEach((e)=>{
	         var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
            df.hidden =  !frm.doc.against_comparison;
            
	    })
	     
            frm.refresh_field("items")
	} ,
	against_comparison (frm) {
	    frm.events.set_child_table_fields(frm)
	},
	comparison (frm) {
	    
	    frm.doc.items.forEach((e)=>{
	         var df = frappe.meta.get_docfield("Stock Entry Detail","comparison_item", e.name);
	         df.get_query = function() {
						var filters = {
							comparison: frm.doc.comparison || ''
						};

						return {
							query: "contracting.contracting.doctype.stock_entry.stock_entry.get_item_query",
							filters: filters
						};
					}
	

	    })

	},
	
})
		"""
		doc.save()
	except:
		pass




def add_properties():
	try:
		name = "Journal Entry Account-reference_type-options"
		if frappe.db.exists("Property Setter",name) :
			doc = frappe.get_doc("Property Setter",name)
		else :

			doc = frappe.new_doc("Property Setter")

		doc.doc_type  = "Journal Entry Account"
		doc.doctype_or_field = "DocField"
		doc.field_name = "reference_type"
		doc.name = name
		doc.property = "options"
		doc.property_type = "Text"
		doc.value = "\nSales Invoice\nPurchase Invoice\nJournal Entry\nSales Order\nPurchase Order\nExpense Claim\nAsset\nLoan\nPayroll Entry\nEmployee Advance\nExchange Rate Revaluation\nInvoice Discounting\nFees\nPay and Receipt Document\nComparison\nClearance\nTender"

		doc.save()
	except:
		pass



@frappe.whitelist()
def make_clearence(source_name, target_doc=None, ignore_permissions=False,task_name=''):
	def postprocess(source, target):
		set_missing_values(source, target)

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.update({'clearance_type': "Outcoming"})
		target.update({'purchase_taxes_and_charges_template':source.taxes_and_charges})
		target.update({'total_after_tax':source.grand_total})

	def update_item(source, target, source_parent):
		# print(f'\n\n\n===>{source_parent}\n\n')
		# print(f'\n\n\n===>{source_parent}\n\n')
		cost_center = source_parent.cost_center #frappe.db.get_value('Sales Order',source_parent.name,'cost_center')
		print(f'\n\n\n==cost_center=>{cost_center}\n\n')
		target.cost_center  = cost_center

	doclist = get_mapped_doc("Sales Order", source_name, {
		"Sales Order": {
			"doctype": "Clearance",
			"field_map": {
				"project":"project"
			# 	"customer": "customer",
			},
		},
		"Sales Order Item": {
			"doctype": "Clearance Items",
			"field_map": {
				"item_code":"clearance_item",
				"rate":"price",
				"qty":"qty",
				"qty":"current_qty",
				"amount":"total_price",
				"uom":"uom"
			},
			"add_if_empty": True,
			"postprocess":update_item,

		},
		"Sales Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges Clearances",
			"field_map": {
				"charge_type": "charge_type",
				# "account_head": "account_head",
				# "description":"description"
			},
			"add_if_empty": True
		},
	}, target_doc,postprocess, ignore_permissions=ignore_permissions)
	task_doc = frappe.get_doc("Task",task_name)
	for item in task_doc.items:
		for row in doclist.items:
			if item.item_code==row.clearance_item:
				row.current_qty=item.qty

	return doclist







@frappe.whitelist()
def make_task_clearence(source_name, target_doc=None, ignore_permissions=False,):
	task = frappe.get_doc("Task",source_name)
	if not task.sales_order :
		frappe.throw(_("Please Set Sales Order"))
	clearance = make_clearence(task.sales_order, target_doc, ignore_permissions,source_name)
	# print ("clearance111111 => ",clearance.items)
	# items = clearance.items or []
	# clearance.set("items",[])
	# print ("clearance11111111111111111 => ",items)
	# for task_item in task.items :
	# 	item = [x for x in items if x.clearance_item == task_item.item_code]
	# 	if len(item) > 0 :
	# 		item = item[0]
	# 		item.qty = task_item.qty
	# 		item.clearance_state = task_item.state
	# 		clearance.append("items",item)
	print ("clearance 2222222222 => ",clearance.items)
	return clearance


		
