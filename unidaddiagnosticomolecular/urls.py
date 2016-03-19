# coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView

from unidaddiagnosticomolecular.views import IndiceView, BusquedaDiagnosticoMedicoView, BusquedaDiagnosticoPatologoView, BusquedaDiagnosticoUdmView, SalvarDiagnoticoMedicoView, SalvarDiagnoticoPatologoView, SalvarDiagnoticoUdmView, EliminarDiagnosticoView, GenerarReporteView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndiceView.as_view(), name='indice'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page': settings.URL_PREFIX + '/login' }, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^busqueda_diagnostico_medico', BusquedaDiagnosticoMedicoView.as_view(), name='busqueda_diagnostico_medico'),
    url(r'^busqueda_diagnostico_patologo', BusquedaDiagnosticoPatologoView.as_view(), name='busqueda_diagnostico_patologo'),
    url(r'^busqueda_diagnostico_udm', BusquedaDiagnosticoUdmView.as_view(), name='busqueda_diagnostico_udm'),
    url(r'^salvar_diagnostico_medico/(?P<pk>\w+|)$', SalvarDiagnoticoMedicoView.as_view(), name='salvar_diagnostico_medico'),
    url(r'^salvar_diagnostico_patologo/(?P<pk>\w+|)$', SalvarDiagnoticoPatologoView.as_view(), name='salvar_diagnostico_patologo'),
    url(r'^salvar_diagnostico_udm/(?P<pk>\w+|)$', SalvarDiagnoticoUdmView.as_view(), name='salvar_diagnostico_udm'),
	url(r'^eliminar_diagnostico/(?P<pk>\w+|)$', EliminarDiagnosticoView.as_view(), name='eliminar_diagnostico'),
	url(r'^generar_reporte/(?P<pk>\w+|)$', GenerarReporteView.as_view(), name='generar_reporte'),
	url(r'^error_operacional$', TemplateView.as_view(template_name='error_operacional.html')),
    url(r'^plataforma_no_disponible$', TemplateView.as_view(template_name='plataforma_no_disponible.html')),
    url(r'^mantenimiento$', TemplateView.as_view(template_name='mantenimiento.html')),
    url(r'^seguridad$', TemplateView.as_view(template_name='seguridad.html')),
)