# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError
from odoo.tools import consteq

class CustomerPortal(CustomerPortal):

    def _get_website_support_ticket_domain(self):
        partner = request.env.user.partner_id
        domain = [
            '|',
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('partner_id', '=', partner.id)
        ]
        return domain

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        # partner = request.env.user.partner_id
        ticket_count = request.env['website.support.ticket'].search_count(
            self._get_website_support_ticket_domain())
        values['ticket_count'] = ticket_count
        return values

    def _website_support_ticket_check_access(self, ticket_id, access_token=None):
        ticket = request.env['website.support.ticket'].browse([ticket_id])
        ticket_sudo = ticket.sudo()
        try:
            ticket.check_access_rights('read')
            ticket.check_access_rule('read')
        except AccessError:
            if not access_token or not consteq(ticket_sudo.access_token, access_token):
                raise
        return ticket_sudo

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tickets(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        # partner = request.env.user.partner_id
        WebsiteSupportTicket = request.env['website.support.ticket']

        domain = self._get_website_support_ticket_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'subject': {'label': _('Subject'), 'order': 'subject'},
            'state': {'label': _('State'), 'order': 'state'},
            'update': {'label': _('Last State Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {'all': {'label': _('All'), 'domain': []}}
        for state in request.env['website.support.ticket.stage'].search([]):
            searchbar_filters.update({
                str(state.id): {'label': state.name, 'domain': [('state', '=', state.id)]}
            })

        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        ticket_count = WebsiteSupportTicket.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tickets",
            url_args={},
            total=ticket_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        tickets = WebsiteSupportTicket.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        values.update({
            'date': date_begin,
            'tickets': tickets,
            'page_name': 'ticket',
            'pager': pager,
            # 'archive_groups': archive_groups,
            'default_url': '/my/tickets',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
        })
        return request.render("website_support.portal_my_tickets", values)

    @http.route(['/my/tickets/<int:ticket_id>'], type='http', auth="public", website=True)
    def portal_my_ticket_page(self, ticket_id=None, access_token=None, **kw):
        try:
            ticket_sudo = self._website_support_ticket_check_access(ticket_id, access_token)
        except AccessError:
            return request.redirect('/my')
        values = self._ticket_get_page_view_values(ticket_sudo, access_token, **kw)
        return request.render("website_support.portal_ticket_page", values)

    def _ticket_get_page_view_values(self, ticket, access_token, **kwargs):
        values = {
            'page_name': 'ticket',
            'ticket': ticket,
        }

        if access_token:
            values['no_breadcrumbs'] = True
            values['access_token'] = access_token
        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):
            values['success'] = kwargs['success']

        return values
