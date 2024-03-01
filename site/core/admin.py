from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    site_header = "FDA.IF"
    site_title = 'FDA.if'
    index_title = 'FDA.if'

admin_site = CustomAdminSite(name='myadmin')