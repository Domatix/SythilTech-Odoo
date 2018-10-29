from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _name = "res.config.settings"
    _inherit = 'res.config.settings'

    close_ticket_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket')]", string="(OBSOLETE)Close Ticket Email Template")
    change_user_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket')]", string="Change User Email Template")
    staff_reply_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket.compose')]", string="Staff Reply Email Template")
    email_default_category_id = fields.Many2one('website.support.ticket.categories', string="Email Default Category")
    max_ticket_attachments = fields.Integer(string="Max Ticket Attachments")
    max_ticket_attachment_filesize = fields.Integer(string="Max Ticket Attachment Filesize (KB)")
    allow_user_signup = fields.Boolean(string="Allow User Signup")
    auto_send_survey = fields.Boolean(string="Auto Send Survey")
    business_hours_id = fields.Many2one('resource.calendar', string="Business Hours")
    google_recaptcha_active = fields.Boolean(string="Google reCAPTCHA Active")
    google_captcha_client_key = fields.Char(string="reCAPTCHA Client Key")
    google_captcha_secret_key = fields.Char(string="reCAPTCHA Secret Key")
    allow_website_priority_set = fields.Selection([("partner","Partner Only"), ("everyone","Everyone")], string="Allow Website Priority Set", help="Cusomters can set the priority of a ticket when submitting via the website form\nPartner Only = logged in user")
    sla_active = fields.Boolean(string="SLA Active")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.default'].set('res.config.settings', 'auto_send_survey', self.auto_send_survey)
        self.env['ir.default'].set('res.config.settings', 'allow_user_signup', self.allow_user_signup)
        self.env['ir.default'].set('res.config.settings', 'change_user_email_template_id', self.change_user_email_template_id.id)
        self.env['ir.default'].set('res.config.settings', 'close_ticket_email_template_id', self.close_ticket_email_template_id.id)
        self.env['ir.default'].set('res.config.settings', 'email_default_category_id', self.email_default_category_id.id)
        self.env['ir.default'].set('res.config.settings', 'staff_reply_email_template_id', self.staff_reply_email_template_id.id)
        self.env['ir.default'].set('res.config.settings', 'max_ticket_attachments', self.max_ticket_attachments)
        self.env['ir.default'].set('res.config.settings', 'max_ticket_attachment_filesize', self.max_ticket_attachment_filesize)
        self.env['ir.default'].set('res.config.settings', 'business_hours_id', self.business_hours_id.id)
        self.env['ir.default'].set('res.config.settings', 'google_recaptcha_active', self.google_recaptcha_active)
        self.env['ir.default'].set('res.config.settings', 'google_captcha_client_key', self.google_captcha_client_key)
        self.env['ir.default'].set('res.config.settings', 'google_captcha_secret_key', self.google_captcha_secret_key)
        self.env['ir.default'].set('res.config.settings', 'allow_website_priority_set', self.allow_website_priority_set)
        self.env['ir.default'].set('res.config.settings', 'sla_active', self.sla_active)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            auto_send_survey=self.env['ir.default'].get('res.config.settings', 'auto_send_survey'),
            allow_user_signup=self.env['ir.default'].get('res.config.settings', 'allow_user_signup'),
            change_user_email_template_id=self.env['ir.default'].get('res.config.settings', 'change_user_email_template_id'),
            close_ticket_email_template_id=self.env['ir.default'].get('res.config.settings', 'close_ticket_email_template_id'),
            email_default_category_id=self.env['ir.default'].get('res.config.settings', 'email_default_category_id'),
            staff_reply_email_template_id=self.env['ir.default'].get('res.config.settings', 'staff_reply_email_template_id'),
            max_ticket_attachments=self.env['ir.default'].get('res.config.settings', 'max_ticket_attachments'),
            max_ticket_attachment_filesize=self.env['ir.default'].get('res.config.settings', 'max_ticket_attachment_filesize'),
            business_hours_id=self.env['ir.default'].get('res.config.settings', 'business_hours_id'),
            allow_website_priority_set=self.env['ir.default'].get('res.config.settings', 'allow_website_priority_set'),
            sla_active=self.env['ir.default'].get('res.config.settings', 'sla_active')
        )
        return res
