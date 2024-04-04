odoo.define('hr_attendance_project.inherit_my_attendance', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var session = require('web.session');

    MyAttendances.include({
        events: Object.assign({}, MyAttendances.prototype.events, {
            'change select[id="projectSelect"]': '_onChangeProjectSelect',
        }),
        // When change the js project, It will set project task with this project
        _onChangeProjectSelect: function (ev) {
            if (this.$("#projectSelect")[0]) {
                const projectID = this.$("select[name='project_id']").val();
                var selectHtml = '<select class="col-7" name="project_task_id" id="projectTaskSelect">';
                selectHtml += '<option selected="selected" value=""></option>';
                for (const tId of this.projects.project_task_ids) {
                    if (tId.project_id == projectID) {
                        selectHtml += "<option value='" + tId.id + "'" + ">" + tId.name + "</option>";
                    }
                }
                selectHtml += "</select>";
                this.$("#projectTaskSelect").replaceWith(selectHtml);
            }
        },
        // When it start Attendance, collection current attendances data with project, project task and description from backend
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    model: 'hr.employee',
                    method: 'get_attendance_projects',
                    args: [[['user_id', '=', self.getSession().uid]]],
                    context: session.user_context,
                }).then(function (p) {
                    self.projects = p;
                });
            });
        },
        // Just only one function overrided!!. I tried many times without overriding. But it was impossible.
        update_attendance: function () {
            var self = this;
            var context = session.user_context;
            var project_id = this.$("select[name='project_id']").val();
            var project_task_id = this.$("select[name='project_task_id']").val();
            var attend_description = this.$("textarea[id='attend_description']").val();
            context['project_id'] = project_id;
            context['project_task_id'] = project_task_id;
            context['attend_description'] = attend_description;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: context,
            })
                .then(function (result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.displayNotification({ title: result.warning, type: 'danger' });
                    }
                });
        },
        // update_attendance: function () {
        //     var self = this;
        //     // Get the project_id and project_task_id from the select elements
        //     var project_id = this.$("select[name='project_id']").val();
        //     var project_task_id = this.$("select[name='project_task_id']").val();
        //     // Create an object with the updated context values
        //     var updatedContext = {
        //         'project_id': project_id,
        //         'project_task_id': project_task_id,
        //     };
        //     this.env.services.user.updateContext({
        //         'project_id': project_id
        //     });
        //     // Update the user_context by extending it with updatedContext
        //     // session.user_context = Object.assign({}, session.user_context, updatedContext);
        //     // Print the updated session.user_context for verification
        //     // Call the parent update_attendance function
        //     this._super.apply(this, arguments);
        // },
    });
    return MyAttendances;
});
