from django.contrib import admin
from .models import Linha, Ponto, Motorista, Localizacao
# Register your models here.
admin.site.site_header = "Larangeo Admin"
admin.site.site_title = "Larangeo Admin Portal" 
admin.site.index_title = "Welcome to Larangeo Admin Portal"

admin.site.register(Linha)
admin.site.register(Ponto) 
admin.site.register(Motorista)
admin.site.register(Localizacao)

