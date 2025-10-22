from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <html>
    <head>
        <title>🚗 MotoristaPower - Sistema de Frota</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { color: #2c3e50; }
            a { color: #3498db; text-decoration: none; margin: 0 10px; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>🚗 MotoristaPower - Sistema de Frota</h1>
        <p>✅ Site está funcionando perfeitamente no Railway!</p>
        <div>
            <a href="/admin/">Painel Admin</a> | 
            <a href="/drivers/">Gestão de Motoristas</a>
        </div>
        <p><small>Deploy realizado com sucesso! 🎉</small></p>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drivers/', include('drivers.urls')),
    path('', home, name='home'),
]