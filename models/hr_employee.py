# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_project_id = fields.Many2one('project.project', compute='_compute_attendance_project',
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    attendance_project_task_id = fields.Many2one('project.task', compute='_compute_attendance_project',
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")
    attendance_description = fields.Text(compute='_compute_attendance_project',
        groups="hr_attendance.group_hr_attendance_kiosk,hr_attendance.group_hr_attendance,hr.group_hr_user")

    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_attendance_project(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'
            if attendance_state == 'checked_in':
                employee.attendance_project_id = att.project_id
                employee.attendance_project_task_id = att.project_task_id
                employee.attendance_description = att.description
            else:
                employee.attendance_project_id = False
                employee.attendance_project_task_id = False
                employee.attendance_description = False

    @api.model
    def get_attendance_projects(self, domain):
        projects = self.env['project.project'].search([])
        tasks = projects.mapped('task_ids')
        emp_id = self.search(domain, limit=1)
        return {
            'project_ids': [{'id':x.id, 'name':x.display_name} for x in projects if len(x.task_ids)>0],
            'project_task_ids': [{'id':x.id, 'name':x.display_name, 'project_id':x.project_id.id} for x in tasks],
            'current_project_id': {'id': emp_id.attendance_project_id.id, 'name':emp_id.attendance_project_id.display_name} if emp_id.attendance_project_id and emp_id.attendance_project_id.id in projects.ids else False,
            'current_project_task_id': {'id': emp_id.attendance_project_task_id.id, 'name':emp_id.attendance_project_task_id.display_name} if emp_id.attendance_project_task_id and emp_id.attendance_project_task_id.id in tasks.ids else False,
            'current_description': emp_id.attendance_description or False,
        }


    def _attendance_action_change(self):
        res = super(HrEmployee, self)._attendance_action_change()
        project_id = self.env.context.get('project_id', False)
        project_task_id = self.env.context.get('project_task_id', False)
        attend_description = self.env.context.get('attend_description', False)
        val = {
            'project_id': int(project_id) if project_id else False, 
            'project_task_id': int(project_task_id) if project_task_id else False,
            'description': str(attend_description) if attend_description else False
        }
        res.update(val)
        return res
